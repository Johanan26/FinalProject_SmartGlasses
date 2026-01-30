import React from "react";

type TileProps = {
  title: string;
  subtitle?: string;
  onClick: () => void;
};

function Tile({ title, subtitle, onClick }: TileProps) {
  return (
    <button
      onClick={onClick}
      className="w-80 rounded-2xl border border-gray-200 bg-white p-6 shadow-sm hover:shadow-md active:scale-[0.99] transition">
      <div className="text-xl font-bold text-gray-900">{title}</div>
      {subtitle && <div className="mt-2 text-sm text-gray-600">{subtitle}</div>}
      <div className="mt-5 text-sm font-semibold text-gray-900">Tap to open →</div>
    </button>
  );
}

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center px-4">
      <div className="flex flex-col gap-4 items-center">
        <Tile
          title="AI Questions"
          subtitle="Ask a question and get an answer."
          onClick={() => alert("AI Questions")}
        />
        <Tile
          title="Photos / Videos"
          subtitle="View or upload your media."
          onClick={() => alert("Photos / Videos")}
        />
        <Tile
          title="Last Location"
          subtitle="Check your last saved location."
          onClick={() => alert("Last Location")}
        />
      </div>
    </div>
  );
}
