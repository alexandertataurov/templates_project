import { useState } from "react";
import WizardStep from "../components/WizardStep";
import FileUploader from "../components/FileUploader";
import DynamicFields from "../components/DynamicFields";
import { notifySuccess, notifyError } from "../components/ToastProvider";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const Wizard = () => {
  const [step, setStep] = useState(1);
  const [file, setFile] = useState<File | null>(null);
  const [templateType, setTemplateType] = useState<string>("");
  const [displayName, setDisplayName] = useState<string>("");
  const [dynamicFields, setDynamicFields] = useState<string[]>([""]);
  const [isUploading, setUploading] = useState(false);

  // 🔥 Форматирование названий полей для шаблона
  const transformFieldName = (name: string) => {
    return `{{${name.replace(/\s+/g, "_").toLowerCase()}}}`;
  };

  // 🚀 Генерация инструкции
  const generateInstructionText = () => {
    return `
      📌 **Как создать шаблон?**
      1️⃣ Вставьте в шаблон следующие переменные вместо значений:
      ${dynamicFields.map(field => `- ${field} → ${transformFieldName(field)}`).join("\n")}
      
      2️⃣ Сохраните документ и загрузите его в систему.
    `;
  };
  
  // 🚀 **Обработка загрузки файла**
  const handleUpload = async () => {
    if (!file || !templateType || !displayName) {
      notifyError("❌ Все поля обязательны для загрузки!");
      return;
    }
  
    setUploading(true);
  
    // 🔍 **Формируем объект динамических полей**
    const transformedFields = dynamicFields.reduce((acc, field) => {
      acc[transformFieldName(field)] = field;
      return acc;
    }, {} as Record<string, string>);
  
    console.log("🔹 Преобразованные поля перед отправкой:", transformedFields);
  
    const formData = new FormData();
    formData.append("file", file);
    formData.append("template_type", templateType);
    formData.append("display_name", displayName);
  
    // 📌 **Передаём `fields` в правильном формате**
    formData.append("fields", JSON.stringify(Object.values(transformedFields)));
  
    console.log("📤 [UPLOAD] Данные перед отправкой:", {
      template_type: templateType,
      display_name: displayName,
      fields: transformedFields,
      file: file.name
    });
  
    try {
      console.log(`📤 [UPLOAD] Отправка запроса на: ${API_URL}/templates/upload`);
  
      const response = await fetch(`${API_URL}/templates/upload`, {
        method: "POST",
        body: formData,
      });
  
      console.log("📥 [UPLOAD] Ответ сервера:", response.status, response.statusText);
  
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Ошибка ${response.status}: ${errorText}`);
      }
  
      const data = await response.json();
      notifySuccess(`✅ Шаблон загружен: ${data.display_name}`);
  
      console.log("✅ [UPLOAD SUCCESS] Ответ сервера:", data);
    } catch (error: any) {
      console.error("🚨 [UPLOAD ERROR]", error);
      notifyError(`❌ Ошибка загрузки: ${error.message || "Сервер недоступен!"}`);
    } finally {
      setUploading(false);
    }
  };
  
  

  return (
    <div className="container mx-auto p-6">
      {/* 🔹 Первый шаг - Описание процесса + Заполнение динамических полей */}
      {step === 1 && (
        <WizardStep step={1}>
          <h2 className="text-xl font-bold">📌 Описание процесса</h2>
          <p className="text-sm mt-2">
            В этом мастере вы создадите шаблон документа с динамическими полями.
            Укажите, какие части текста должны заменяться на значения.
            Например, <b>"Дата договора"</b> будет преобразовано в <b>{'{{дата_договора}}'}</b>.
          </p>

          {/* 🔥 Управление динамическими полями */}
          <DynamicFields fields={dynamicFields} setFields={setDynamicFields} />

          <button 
            onClick={() => setStep(2)} 
            className="w-full bg-blue-500 text-white p-3 mt-4 rounded"
          >
            Далее ➡️
          </button>
        </WizardStep>
      )}

      {/* 🔹 Второй шаг - Инструкция по созданию шаблона */}
      {step === 2 && (
        <WizardStep step={2}>
          <h2 className="text-xl font-bold">📑 Инструкция</h2>
          <p className="text-sm mt-2">
            Заполните ваш документ, используя переменные ниже:
          </p>
          <pre className="text-sm bg-gray-800 text-green-400 p-4 rounded">
            {generateInstructionText()}
          </pre>
          
          <button 
            onClick={() => setStep(3)} 
            className="w-full bg-blue-500 text-white p-3 mt-4 rounded"
          >
            Продолжить ➡️
          </button>
        </WizardStep>
      )}

      {/* 🔹 Третий шаг - Загрузка шаблона */}
      {step === 3 && (
        <WizardStep step={3}>
          <h2 className="text-xl font-bold">📤 Загрузка шаблона</h2>
          <FileUploader onFileUpload={setFile} />

          <input
            type="text"
            placeholder="Название шаблона"
            value={displayName}
            onChange={(e) => setDisplayName(e.target.value)}
            className="w-full border p-2 mt-2 rounded"
          />

          <select
            value={templateType}
            onChange={(e) => setTemplateType(e.target.value)}
            className="w-full border p-2 mt-2 rounded"
          >
            <option value="">Выберите тип шаблона</option>
            <option value="contract">Договор</option>
            <option value="specification">Спецификация</option>
            <option value="addendum">Дополнение</option>
          </select>

          {/* 🔥 Кнопка загрузки */}
          <button
            onClick={handleUpload}
            className={`w-full text-white p-2 mt-4 rounded ${
              isUploading ? "bg-gray-400 cursor-not-allowed" : "bg-green-500"
            }`}
            disabled={isUploading}
          >
            {isUploading ? "⏳ Загрузка..." : "✅ Загрузить"}
          </button>
        </WizardStep>
      )}
    </div>
  );
};

export default Wizard;
