import { useState } from "react";
import { notifySuccess, notifyError } from "../components/ToastProvider";

interface EditTemplateProps {
  templateId: number;
  currentDisplayName: string;
  currentFields?: string[];
  onClose: () => void;
  onSave: (updatedTemplate: { id: number; display_name: string; dynamic_fields: string[] }) => void;
}

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"; // Фоллбэк

const EditTemplate = ({ templateId, currentDisplayName, currentFields = [], onClose, onSave }: EditTemplateProps) => {
  const [displayName, setDisplayName] = useState(currentDisplayName);
  const [dynamicFields, setDynamicFields] = useState(currentFields);

  const handleFieldChange = (index: number, value: string) => {
    const updatedFields = [...dynamicFields];
    updatedFields[index] = value;
    setDynamicFields(updatedFields);
  };

  const addField = () => setDynamicFields([...dynamicFields, ""]);
  const removeField = (index: number) => setDynamicFields(dynamicFields.filter((_, i) => i !== index));

  const handleSave = async () => {
    console.log("💾 Сохранение шаблона:", { templateId, displayName, dynamicFields });

    const formData = new FormData();
    formData.append("template_id", templateId.toString());
    formData.append("display_name", displayName);
    formData.append("fields", JSON.stringify(dynamicFields));

    try {
      console.log(`📤 [UPDATE] Запрос: ${API_URL}/templates/update`);
      console.log("📤 [UPDATE] Данные:", Object.fromEntries(formData));

      const response = await fetch(`${API_URL}/templates/update`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorResponse = await response.json();
        console.error("❌ Ошибка обновления:", errorResponse);
        throw new Error(`Ошибка ${response.status}: ${JSON.stringify(errorResponse)}`);
      }

      const data = await response.json();
      notifySuccess(`✅ Шаблон обновлен: ${data.message}`);
      onSave({ id: templateId, display_name: displayName, dynamic_fields: dynamicFields });
      onClose();
    } catch (error: any) {
      console.error("🚨 [UPDATE ERROR]", error);
      notifyError(`❌ Ошибка обновления: ${error.message || "Сервер недоступен!"}`);
    }
  };

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white p-6 rounded shadow-lg w-96">
        <h2 className="text-lg font-bold">Редактирование шаблона</h2>

        <label className="block mt-4">Название:</label>
        <input
          type="text"
          value={displayName}
          onChange={(e) => setDisplayName(e.target.value)}
          className="w-full border p-2 rounded"
        />

        <label className="block mt-4">Динамические поля:</label>
        {dynamicFields.map((field, index) => (
          <div key={index} className="flex gap-2 mt-2">
            <input
              type="text"
              value={field}
              onChange={(e) => handleFieldChange(index, e.target.value)}
              className="w-full border p-2 rounded"
            />
            {dynamicFields.length > 1 && (
              <button
                onClick={() => removeField(index)}
                className="bg-red-500 text-white px-3 py-1 rounded"
              >
                ❌
              </button>
            )}
          </div>
        ))}

        <button
          onClick={addField}
          className="w-full bg-gray-500 text-white p-2 mt-2 rounded"
        >
          ➕ Добавить поле
        </button>

        <button
          onClick={handleSave}
          className="mt-4 bg-blue-500 text-white px-4 py-2 rounded"
        >
          ✅ Сохранить
        </button>
        <button
          onClick={onClose}
          className="mt-2 bg-gray-500 text-white px-4 py-2 rounded"
        >
          ❌ Закрыть
        </button>
      </div>
    </div>
  );
};

export default EditTemplate;
