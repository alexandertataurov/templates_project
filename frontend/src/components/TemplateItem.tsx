import { useState, useEffect, useRef } from "react";
import { TrashIcon, PencilSquareIcon, ArrowUturnLeftIcon } from "@heroicons/react/24/outline";

interface Template {
  id: number;
  display_name: string;
  file_path?: string;
  file_size?: string;
}

interface TemplateItemProps {
  template: Template;
  onDelete: (id: number) => void;
  onEdit: (template: Template) => void;
}

const TemplateItem: React.FC<TemplateItemProps> = ({ template, onDelete, onEdit }) => {
  if (!template) return null; // ✅ Защита от рендера пустых данных

  const [isDeleting, setIsDeleting] = useState(false);
  const [showUndo, setShowUndo] = useState(false);
  const undoTimer = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    return () => {
      if (undoTimer.current) clearTimeout(undoTimer.current);
    };
  }, []);

  const handleDelete = () => {
    console.log(`⏳ Подготовка к удалению шаблона: ${template.display_name}`);
    setIsDeleting(true);
    setShowUndo(true);
    undoTimer.current = setTimeout(() => {
      setShowUndo(false);
      onDelete(template.id);
      console.log(`✅ Шаблон удален: ${template.display_name}`);
    }, 3000);
  };

  const cancelDelete = () => {
    console.log(`🔄 Отмена удаления шаблона: ${template.display_name}`);
    if (undoTimer.current) clearTimeout(undoTimer.current);
    setIsDeleting(false);
    setShowUndo(false);
  };

  return (
    <li
      className={`flex justify-between items-center p-5 border-b border-gray-300 dark:border-gray-600 transition-all ${
        isDeleting ? "opacity-50" : "hover:opacity-75"
      }`}
      tabIndex={0}
    >
      <div className="flex flex-col">
        <span className="truncate font-medium text-gray-900 dark:text-gray-200 m-3" title={template.display_name}>
          {template.display_name || "📄 Без названия"} {/* ✅ Безопасное отображение имени */}
        </span>
        {template.file_path && (
          <a
            href={template.file_path}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-blue-600 dark:text-blue-400 hover:underline"
          >
            📂 Открыть файл
          </a>
        )}
        {template.file_size && <p className="text-xs text-gray-500 dark:text-gray-400">📏 Размер: {template.file_size}</p>}
      </div>

      <div className="flex gap-3">
        <button
          onClick={() => onEdit(template)}
          className="btn-secondary p-1.5"
          title="Редактировать шаблон"
          aria-label="Редактировать"
        >
          <PencilSquareIcon className="w-5 h-5" />
        </button>

        {showUndo ? (
          <button
            onClick={cancelDelete}
            className="btn-primary p-1.5"
            title="Отменить удаление"
            aria-label="Отменить удаление"
          >
            <ArrowUturnLeftIcon className="w-5 h-5" />
          </button>
        ) : (
          <button
            onClick={handleDelete}
            className="btn-danger p-1.5 transition-all hover:bg-red-700"
            title="Удалить шаблон"
            aria-label="Удалить"
          >
            <TrashIcon className="w-5 h-5" />
          </button>
        )}
      </div>
    </li>
  );
};

export default TemplateItem;
