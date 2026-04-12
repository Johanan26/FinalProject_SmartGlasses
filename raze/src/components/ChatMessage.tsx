interface AIQuestionItem {
  _id: string;
  user_id: string | number;
  data: string;
  response: string;
}

interface Props {
  item: AIQuestionItem;
}

export default function ChatMessage({ item }: Props) {
  return (
    <div className="space-y-3">
      <div className="flex justify-end">
        <div className="max-w-[80%] bg-gradient-to-br from-red-500 to-red-600 text-white rounded-2xl rounded-tr-sm px-4 py-3 shadow-lg">
          <p className="text-sm leading-relaxed whitespace-pre-wrap">
            {item.data}
          </p>
        </div>
      </div>

      <div className="flex justify-start">
        <div className="flex gap-3 max-w-[80%]">
          <div className="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center flex-shrink-0 mt-1">
            <svg
              className="w-4 h-4 text-red-400"
              fill="currentColor"
              viewBox="0 0 24 24"
            >
              <path d="M12 2a2 2 0 012 2c0 .74-.4 1.39-1 1.73V7h1a7 7 0 017 7h1a1 1 0 010 2h-1v1a2 2 0 01-2 2H5a2 2 0 01-2-2v-1H2a1 1 0 010-2h1a7 7 0 017-7h1V5.73A2 2 0 0110 4a2 2 0 012-2zm-3 9a1 1 0 100 2 1 1 0 000-2zm6 0a1 1 0 100 2 1 1 0 000-2z" />
            </svg>
          </div>
          <div className="bg-gray-800 border border-gray-700 rounded-2xl rounded-tl-sm px-4 py-3 shadow-lg">
            <p className="text-sm leading-relaxed text-gray-200 whitespace-pre-wrap">
              {item.response}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
