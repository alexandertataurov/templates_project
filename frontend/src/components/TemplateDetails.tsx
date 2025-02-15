import { useState } from "react";

const TemplateDetails = ({ template, onClose, onSave }: { 
  template: any; 
  onClose: () => void;
  onSave: (updatedTemplate: any) => void;
}) => {
  const [editedTemplate, setEditedTemplate] = useState(template);

  return (
    <div className="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white p-6 rounded-lg shadow-lg w-96">
        <h2 className="text-xl font-bold mb-4">✏️ Редактирование шаблона</h2>
        
        <p className="text-gray-700"><b>ID:</b> {editedTemplate.id}</p>
        <p className="text-gray-700"><b>Дата добавления:</b> {new Date(editedTemplate.created_at).toLocaleString()}</p>

        <label className="block mb-2">
          <span className="text-gray-700">Название:</span>
          <input 
            type="text" 
            className="w-full p-2 border rounded"
            value={editedTemplate.display_name}
            onChange={(e) => setEditedTemplate({...editedTemplate, display_name: e.target.value})}
          />
        </label>

        <label className="block mb-2">
          <span className="text-gray-700">Тип:</span>
          <input 
            type="text" 
            className="w-full p-2 border rounded"
            value={editedTemplate.type}
            onChange={(e) => setEditedTemplate({...editedTemplate, type: e.target.value})}
          />
        </label>

        <p className="mt-2">
          <b>📥 Скачать:</b> 
          <a href={editedTemplate.file_path} download className="text-blue-500 underline ml-2">
            Скачать файл
          </a>
        </p>

        <div className="flex justify-end mt-4 space-x-2">
          <button className="bg-gray-400 text-white px-3 py-1 rounded" onClick={onClose}>❌ Отмена</button>
          <button 
            className="bg-green-500 text-white px-3 py-1 rounded" 
            onClick={() => onSave(editedTemplate)}
          >
            💾 Сохранить
          </button>
        </div>
      </div>
    </div>
  );
};

export default TemplateDetails;
