import { useNavigate } from "react-router-dom";
import { useEffect, useState, useRef } from "react";
import axios from "axios";
import ChatMessage from "../components/ChatMessage";
import LoadingBubble from "../components/LoadingBubble";
import ChatInput from "../components/ChatInput";

interface AIQuestionItem {
  _id: { $oid: string } | string;
  user_id: number;
  question: string;
  answer: string;
}

const BASE = `http://${import.meta.env.VITE_BACKEND_URL}`;

export default function Ai_questions() {
  const navigate = useNavigate();
  const [questions, setQuestions] = useState<AIQuestionItem[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  const fetchQuestions = async () => {
    try {
      const res = await axios.get(`${BASE}/get_questions`);
      setQuestions(res.data.questions);
    } catch (e) {
      console.error("Failed to fetch questions:", e);
    }
  };

  useEffect(() => {
    fetchQuestions();
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [questions, loading]);

  const handleAsk = async () => {
    const trimmed = input.trim();
    if (!trimmed || loading) return;

    setLoading(true);
    setError(null);
    setInput("");

    try {
      await axios.post(`${BASE}/ask_question`, { data: trimmed });
      await fetchQuestions();
    } catch (e) {
      console.error("Failed to ask question:", e);
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col">
      <div className="relative flex items-center justify-center px-4 py-4 border-b border-gray-700 bg-gray-900 sticky top-0 z-10">
        <button
          className="flex absolute top-0 left-0 text-white bg-gradient-to-r from-red-400 via-red-500 to-red-600 hover:bg-gradient-to-br font-medium rounded text-sm px-4 py-2.5"
          onClick={() => navigate("/home")}
        >
          Back
        </button>
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
          <h1 className="text-xl font-bold tracking-wide">AI Assistant</h1>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-6 max-w-3xl w-full mx-auto">
        {questions.length === 0 && !loading && (
          <div className="flex flex-col items-center justify-center h-64 text-gray-500">
            <svg className="w-12 h-12 mb-4 opacity-40" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
                d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-4 4-4-4z" />
            </svg>
            <p className="text-lg font-medium">No questions yet</p>
            <p className="text-sm mt-1">Ask something below to get started</p>
          </div>
        )}

        {questions.map((item, index) => (
          <ChatMessage key={index} item={item} />
        ))}

        {loading && <LoadingBubble />}

        {error && (
          <div className="text-center">
            <p className="text-red-400 text-sm bg-red-900/20 border border-red-800 rounded-lg px-4 py-2 inline-block">
              {error}
            </p>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      <ChatInput
        input={input}
        loading={loading}
        onChange={setInput}
        onSubmit={handleAsk}
      />
    </div>
  );
}