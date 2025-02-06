import { useState } from "react";
import { uploadTemplate } from "../api";

const UploadForm = () => {
  const [file, setFile] = useState<File | null>(null);
  const [name, setName] = useState("");

  const handleUpload = async () => {
    if (!file || !name) {
      console.warn("⚠️ Файл или имя шаблона не заполнены");
      alert("Выберите файл и введите имя шаблона");
      return;
    }

    console.log("🚀 Загрузка файла:", file.name, "с именем:", name);
    try {
      const response = await uploadTemplate(file, name);
      console.log("✅ Ответ сервера:", response);
      alert(response.message);
    } catch (error) {
      console.error("❌ Ошибка загрузки шаблона:", error);
    }
  };

  return (
    <div className="p-4 bg-white shadow-md rounded">
      <input type="text" placeholder="Имя шаблона" className="border p-2 w-full mt-4 rounded" onChange={(e) => setName(e.target.value)} />
      <input type="file" className="mt-4" onChange={(e) => setFile(e.target.files?.[0] || null)} />
      <button onClick={handleUpload} className="mt-4 bg-green-500 text-white px-4 py-2 rounded w-full">🚀 Загрузить</button>
    </div>
  );
};

export default UploadForm;
