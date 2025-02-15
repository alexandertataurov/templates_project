import React, { useState } from "react";

interface UploadTemplateProps {
  onSuccess: (response: any) => void;
  onError: (error: any) => void;
  setUploading: React.Dispatch<React.SetStateAction<boolean>>;
}

const UploadTemplate: React.FC<UploadTemplateProps> = ({ onSuccess, onError, setUploading }) => {
  const [file, setFile] = useState<File | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      setFile(event.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      onError(new Error("Файл не выбран"));
      return;
    }

    setUploading(true);
    const formData = new FormData();
    formData.append("file", file);
    formData.append("template_type", "contract"); // Укажи тип
    formData.append("display_name", file.name);

    try {
      const response = await fetch("/templates/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Ошибка ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      onSuccess(data);
    } catch (error: any) {
      onError(error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="p-4 border rounded">
      <input type="file" onChange={handleFileChange} className="mb-2" />
      <button onClick={handleUpload} className="bg-blue-500 text-white p-2 rounded">
        📤 Загрузить шаблон
      </button>
    </div>
  );
};

export default UploadTemplate;
