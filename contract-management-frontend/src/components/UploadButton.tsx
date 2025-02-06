import React from "react";

interface Props {
  isUploading: boolean;
  onClick: () => void;
}

const UploadButton: React.FC<Props> = React.memo(({ isUploading, onClick }) => (
  <button
    onClick={onClick}
    disabled={isUploading}
    className={`w-full px-4 py-2 rounded text-white font-medium transition ${isUploading ? "bg-gray-400" : "bg-green-500 hover:bg-green-600"}`}
  >
    {isUploading ? "⏳ Загрузка..." : "✅ Загрузить"}
  </button>
));

export default UploadButton;
