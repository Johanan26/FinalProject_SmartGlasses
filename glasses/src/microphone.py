import threading
import queue
import time
from typing import Callable, Optional, Union, List

import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel


class RazeListener:
    """
    Always-listening mic capture + utterance-based transcription.
    Wake phrase: "hey raze" -> start buffering subsequent speech.
    When an end condition is met, pushes the FULL buffered text to command_queue.

    Also supports pushing strings into the same queue from other threads via put_external().
    """

    def __init__(
        self,
        model_size: str = "base",
        compute_type: str = "int8",
        device: Optional[Union[int, str]] = None,
        fs: int = 16000,
        channels: int = 1,
        frame_ms: int = 30,
        speech_rms_threshold: float = 0.012,
        min_speech_seconds: float = 0.25,
        silence_end_seconds: float = 0.6,
        preroll_seconds: float = 0.4,
        max_utterance_seconds: float = 15.0,
        beam_size: int = 5,
        language: Optional[str] = "en",  # set "en" for speed if only English
        on_transcript: Optional[Callable[[str], None]] = None,

        # Wake / session control
        wake_phrase: str = "hey raze",
        end_phrases: Optional[List[str]] = None,  # e.g. ["stop raze", "thanks raze"]
        inactivity_end_seconds: float = 3.0,       # end session if no new utterances for X seconds
    ):
        # Whisper/audio settings
        self.model = WhisperModel(model_size, compute_type=compute_type)
        self.device = device
        self.fs = fs
        self.channels = channels
        self.dtype = "float32"

        self.frame_ms = frame_ms
        self.frame_samples = int(self.fs * self.frame_ms / 1000)

        self.speech_rms_threshold = speech_rms_threshold
        self.min_speech_seconds = min_speech_seconds
        self.silence_end_seconds = silence_end_seconds
        self.preroll_seconds = preroll_seconds
        self.max_utterance_seconds = max_utterance_seconds

        self.beam_size = beam_size
        self.language = language
        self.on_transcript = on_transcript

        # Wake/session settings
        self.wake_phrase = wake_phrase.lower().strip()
        self.end_phrases = [p.lower().strip() for p in (end_phrases or ["stop raze", "thanks raze"])]
        self.inactivity_end_seconds = inactivity_end_seconds

        # Queues
        self._audio_q: "queue.Queue[np.ndarray]" = queue.Queue()

        # This is the queue you asked for: other threads can push into it too.
        self.command_queue: "queue.Queue[str]" = queue.Queue()

        # Threading
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

        # Session/buffer state (protected by lock)
        self._lock = threading.Lock()
        self._active = False
        self._buffer_parts: List[str] = []
        self._last_active_time = 0.0

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        # unblock queue.get
        self._audio_q.put(np.zeros((self.frame_samples, self.channels), dtype=np.float32))
        if self._thread:
            self._thread.join(timeout=2.0)

    def get_command(self, timeout: Optional[float] = None) -> Optional[str]:
        """Other threads/main can pull finalized buffered commands from here."""
        try:
            return self.command_queue.get(timeout=timeout)
        except queue.Empty:
            return None

    def put_external(self, text: str) -> None:
        """
        Push strings into the SAME queue from other threads.
        This is thread-safe because queue.Queue is thread-safe.
        """
        if text and text.strip():
            self.command_queue.put(text.strip())

    def is_active(self) -> bool:
        """Whether we are currently buffering after 'hey raze'."""
        with self._lock:
            return self._active

    def _audio_callback(self, indata, frames, time_info, status) -> None:
        if status:
            pass
        self._audio_q.put(indata.copy())

    @staticmethod
    def _rms(x: np.ndarray) -> float:
        x = x.reshape(-1)
        return float(np.sqrt(np.mean(x * x) + 1e-12))

    @staticmethod
    def _concat_audio(chunks: List[np.ndarray]) -> np.ndarray:
        if not chunks:
            return np.zeros((0,), dtype=np.float32)
        x = np.concatenate([c.reshape(-1) for c in chunks], axis=0)
        return x.astype(np.float32)

    def _emit_transcript(self, text: str) -> None:
        if self.on_transcript:
            try:
                self.on_transcript(text)
            except Exception:
                pass

    def _start_session(self, initial_text_after_wake: str = "") -> None:
        with self._lock:
            self._active = True
            self._buffer_parts = []
            self._last_active_time = time.time()
            if initial_text_after_wake.strip():
                self._buffer_parts.append(initial_text_after_wake.strip())

    def _append_to_buffer(self, text: str) -> None:
        with self._lock:
            if not self._active:
                return
            self._buffer_parts.append(text.strip())
            self._last_active_time = time.time()

    def _finalize_session(self) -> None:
        with self._lock:
            if not self._active:
                return
            full = " ".join(p for p in self._buffer_parts if p).strip()
            self._active = False
            self._buffer_parts = []
            self._last_active_time = 0.0

        if full:
            self.command_queue.put(full)

    def _check_inactivity_end(self) -> None:
        with self._lock:
            if not self._active:
                return
            last = self._last_active_time

        if last and (time.time() - last) >= self.inactivity_end_seconds:
            self._finalize_session()

    def _run_loop(self) -> None:
        preroll_max_frames = int(self.preroll_seconds * 1000 / self.frame_ms)
        silence_end_frames = int(self.silence_end_seconds * 1000 / self.frame_ms)
        min_speech_frames = int(self.min_speech_seconds * 1000 / self.frame_ms)
        max_utt_frames = int(self.max_utterance_seconds * 1000 / self.frame_ms)

        preroll: List[np.ndarray] = []
        utterance: List[np.ndarray] = []

        in_speech = False
        silence_count = 0
        speech_frames = 0

        with sd.InputStream(
            samplerate=self.fs,
            channels=self.channels,
            dtype=self.dtype,
            blocksize=self.frame_samples,
            callback=self._audio_callback,
            device=self.device,
        ):
            while not self._stop_event.is_set():
                # End active session if user goes quiet for too long
                self._check_inactivity_end()

                try:
                    chunk = self._audio_q.get(timeout=0.2)
                except queue.Empty:
                    continue

                if self._stop_event.is_set():
                    break

                level = self._rms(chunk)

                preroll.append(chunk)
                if len(preroll) > preroll_max_frames:
                    preroll.pop(0)

                if not in_speech:
                    if level >= self.speech_rms_threshold:
                        in_speech = True
                        silence_count = 0
                        speech_frames = 0
                        utterance = preroll.copy()
                else:
                    utterance.append(chunk)

                    if level >= self.speech_rms_threshold:
                        silence_count = 0
                        speech_frames += 1
                    else:
                        silence_count += 1

                    ended_by_silence = (silence_count >= silence_end_frames and speech_frames >= min_speech_frames)
                    ended_by_maxlen = (len(utterance) >= max_utt_frames)

                    if ended_by_silence or ended_by_maxlen:
                        audio = self._concat_audio(utterance)

                        segments, _info = self.model.transcribe(
                            audio,
                            language=self.language,
                            beam_size=self.beam_size,
                            vad_filter=False,
                        )

                        text = "".join(seg.text for seg in segments).strip()
                        if text:
                            self._emit_transcript(text)
                            self._handle_text(text)

                        # reset utterance collection
                        in_speech = False
                        utterance = []
                        silence_count = 0
                        speech_frames = 0

            # If stopping while active, finalize what we have
            self._finalize_session()

    def _handle_text(self, text: str) -> None:
        """
        State machine:
        - If idle: look for wake phrase -> start session.
        - If active: append utterance; if end phrase -> finalize.
        """
        low = text.lower().strip()

        # If idle, detect wake phrase
        if not self.is_active():
            if self.wake_phrase in low:
                # Keep anything after the wake phrase in the same utterance
                idx = low.find(self.wake_phrase)
                after = text[idx + len(self.wake_phrase):].strip(" ,.!?").strip()
                self._start_session(initial_text_after_wake=after)
            return

        # If active, check end phrases
        for p in self.end_phrases:
            if p in low:
                # Remove everything from end phrase onwards (optional)
                cut = low.find(p)
                kept = text[:cut].strip(" ,.!?").strip()
                if kept:
                    self._append_to_buffer(kept)
                self._finalize_session()
                return

        # Otherwise, just append whole utterance
        self._append_to_buffer(text)