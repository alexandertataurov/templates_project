import { useState, useMemo } from "react";
import TemplateItem from "./TemplateItem";
import EditTemplate from "./EditTemplate";
import { PlusCircleIcon, ArrowPathIcon } from "@heroicons/react/24/outline";

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
  const [search, setSearch] = useState<string>("");
  const [sortBy, setSortBy] = useState<"name" | "date">("date");

  const handleEdit = (template: Template) => {
    setEditingTemplate(template);
    localStorage.setItem("lastEditedTemplate", template.id.toString());
  };

  const filteredTemplates = useMemo(() => {
    return templates
      .filter((t) => t.display_name.toLowerCase().includes(search.toLowerCase()))
      .sort((a, b) => (sortBy === "name" ? a.display_name.localeCompare(b.display_name) : new Date(b.created_at).getTime() - new Date(a.created_at).getTime()));
  }, [templates, search, sortBy]);

  return (
    <div className="container mx-auto p-6 max-w-10xl">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">📜 Шаблоны</h2>
        <div className="flex items-center gap-5">
          <input
            type="text"
            className="input w-36 text-xs"
            placeholder="🔍 Поиск..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <select
            className="input w-36 text-xs" 
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as "name" | "date")}
          >
            <option value="date" className="text-gray-900">📆 По дате</option>
            <option value="name" className="text-gray-900">🔤 По имени</option>
          </select>
          <button className="btn-secondary p-2 rounded-full hover:bg-gray-700 transition-all" title="Обновить">
            <ArrowPathIcon className="w-5 h-5" />
          </button>
          <button
            className="btn-primary p-2 rounded-full hover:bg-green-700 transition-all"
            title="Добавить новый шаблон"
            onClick={() => setEditingTemplate(null)}
          >
            <PlusCircleIcon className="w-5 h-5" />
          </button>
        </div>
      </div>

      <ul className="bg-white dark:bg-gray-900 shadow-md rounded-lg divide-y divide-gray-300 dark:divide-gray-700 max-h-[600px] overflow-y-auto custom-scrollbar animate-fadeIn">
        {filteredTemplates.map((template) => (
          <TemplateItem
            key={template.id}
            template={template}
            onDelete={onDelete}
            onEdit={() => handleEdit(template)}
          />
        ))}
      </ul>

      {editingTemplate && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center animate-fadeIn">
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg w-[500px]">
            <EditTemplate
              templateId={editingTemplate.id}
              currentDisplayName={editingTemplate.display_name}
              currentFields={editingTemplate.dynamic_fields}
              onClose={() => setEditingTemplate(null)}
              onSave={() => setEditingTemplate(null)}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default TemplateList;
