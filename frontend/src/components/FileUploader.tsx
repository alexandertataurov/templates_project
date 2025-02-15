import { useState } from "react";

const FileUploader = ({ onFileUpload }: { onFileUpload: (file: File) => void }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  return (
    <div className="p-4 border border-gray-300 rounded">
      <input type="file" onChange={(e) => {
        const file = e.target.files?.[0];
        console.log("📂 Файл выбран:", file?.name);
        setSelectedFile(file || null);
        file && onFileUpload(file);
      }} />
      {selectedFile && <p>📂 {selectedFile.name}</p>}
    </div>
  );
};

export default FileUploader;
