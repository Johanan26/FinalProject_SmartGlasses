interface Props {
  input: string;
  loading: boolean;
  onChange: (value: string) => void;
  onSubmit: () => void;
}

export default function ChatInput({
  input,
  loading,
  onChange,
  onSubmit,
}: Props) {
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      onSubmit();
    }
  };

  return (
    <div className="sticky bottom-0 bg-gray-900 border-t border-gray-700 px-4 py-4">
      <div className="max-w-3xl mx-auto flex gap-3 items-end">
        <textarea
          value={input}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask anything… (Enter to send, Shift+Enter for new line)"
          rows={1}
          disabled={loading}
          className="flex-1 resize-none bg-gray-800 border border-gray-600 rounded-xl px-4 py-3 text-sm text-white placeholder-gray-500
            focus:outline-none focus:border-red-500 focus:ring-1 focus:ring-red-500 transition-colors
            disabled:opacity-50 disabled:cursor-not-allowed max-h-40 overflow-y-auto"
          style={{ lineHeight: "1.5" }}
          onInput={(e) => {
            const el = e.currentTarget;
            el.style.height = "auto";
            el.style.height = Math.min(el.scrollHeight, 160) + "px";
          }}
        />
        <button
          onClick={onSubmit}
          disabled={loading || !input.trim()}
          className="flex-shrink-0 w-11 h-11 flex items-center justify-center rounded-xl
            bg-gradient-to-br from-red-500 to-red-600 hover:from-red-400 hover:to-red-500
            disabled:opacity-40 disabled:cursor-not-allowed
            transition-all duration-150 shadow-lg hover:shadow-red-500/25"
        >
          {loading ? (
            <svg
              className="w-4 h-4 animate-spin text-white"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8v8z"
              />
            </svg>
          ) : (
            <svg
              className="w-4 h-4 text-white"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
              />
            </svg>
          )}
        </button>
      </div>
    </div>
  );
}
