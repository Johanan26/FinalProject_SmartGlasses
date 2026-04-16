export default function LoadingBubble() {
  return (
    <div className="space-y-3">
      <div className="flex justify-end">
        <div className="max-w-[80%] bg-gradient-to-br from-red-500 to-red-600 opacity-60 rounded-2xl rounded-tr-sm px-4 py-3">
          <p className="text-sm text-white">Sending...</p>
        </div>
      </div>
      <div className="flex justify-start">
        <div className="flex gap-3">
          <div className="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center flex-shrink-0 mt-1">
            <svg
              className="w-4 h-4 text-red-400"
              fill="currentColor"
              viewBox="0 0 24 24"
            >
              <path d="M12 2a2 2 0 012 2c0 .74-.4 1.39-1 1.73V7h1a7 7 0 017 7h1a1 1 0 010 2h-1v1a2 2 0 01-2 2H5a2 2 0 01-2-2v-1H2a1 1 0 010-2h1a7 7 0 017-7h1V5.73A2 2 0 0110 4a2 2 0 012-2zm-3 9a1 1 0 100 2 1 1 0 000-2zm6 0a1 1 0 100 2 1 1 0 000-2z" />
            </svg>
          </div>
          <div className="bg-gray-800 border border-gray-700 rounded-2xl rounded-tl-sm px-5 py-4">
            <div className="flex gap-1.5 items-center h-4">
              <span
                className="w-2 h-2 rounded-full bg-gray-400 animate-bounce"
                style={{ animationDelay: "0ms" }}
              />
              <span
                className="w-2 h-2 rounded-full bg-gray-400 animate-bounce"
                style={{ animationDelay: "150ms" }}
              />
              <span
                className="w-2 h-2 rounded-full bg-gray-400 animate-bounce"
                style={{ animationDelay: "300ms" }}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
