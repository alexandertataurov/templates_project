import { useState } from "react";
import EditTemplate from "./EditTemplate";

// Определение типа шаблона
interface Template {
  id: number;
  type: string;
  display_name: string;
  file_path: string;
  dynamic_fields: string[];
  created_at: string;
}

interface TemplateListProps {
  templates: Template[];
  onDelete: (id: number) => void;
}

const TemplateList: React.FC<TemplateListProps> = ({ templates, onDelete }) => {
  const [editingTemplate, setEditingTemplate] = useState<Template | null>(null);

  const handleEdit = (template: Template) => {
    console.log("✏️ Начало редактирования шаблона:", template);

    // Проверяем формат dynamic_fields и парсим, если это строка
    const parsedFields = Array.isArray(template.dynamic_fields)
      ? template.dynamic_fields.map((field) => {
          try {
            return JSON.parse(field);
          } catch (e) {
            return field;
          }
        }).flat()
      : [];

    setEditingTemplate({
      ...template,
      dynamic_fields: parsedFields,
    });
  };

  return (
    <div className="container mx-auto p-6">
      <ul>
        {templates.length === 0 ? (
          <p className="text-gray-500">⚠️ Нет шаблонов</p>
        ) : (
          templates.map((template) => (
            <li key={template.id} className="flex justify-between items-center p-2 border-b">
              <div>
                <p className="font-bold">{template.display_name}</p>
                <p className="text-sm text-gray-500">📄 Тип: {template.type}</p>
                <p className="text-sm text-gray-500">📂 Файл: {template.file_path}</p>
                <p className="text-sm text-gray-500">📆 Создан: {new Date(template.created_at).toLocaleString()}</p>
                <p className="text-sm text-gray-500">
                  🔑 Динамические поля: {template.dynamic_fields.join(", ") || "Нет"}
                </p>
              </div>
              <div>
                <button
                  onClick={() => handleEdit(template)}
                  className="bg-blue-500 text-white px-3 py-1 rounded mr-2"
                >
                  ✏️ Редактировать
                </button>
                <button
                  onClick={() => onDelete(template.id)}
                  className="bg-red-500 text-white px-3 py-1 rounded"
                >
                  🗑 Удалить
                </button>
              </div>
            </li>
          ))
        )}
      </ul>

      {editingTemplate && (
        <EditTemplate
          templateId={editingTemplate.id}
          currentDisplayName={editingTemplate.display_name}
          currentFields={editingTemplate.dynamic_fields}
          onClose={() => setEditingTemplate(null)}
          onSave={(updatedTemplate) => {
            console.log("✅ Шаблон обновлен:", updatedTemplate);
            setEditingTemplate(null);
          }}
        />
      )}
    </div>
  );
};

export default TemplateList;
