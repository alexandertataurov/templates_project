const TemplateItem = ({ template, onDelete }: { template: any; onDelete: (id: number) => void }) => {
    return (
      <li className="flex justify-between p-2 border-b border-gray-300">
        {template.display_name}
        <button
          onClick={() => onDelete(template.id)}
          className="bg-red-500 text-white px-3 py-1 rounded"
        >
          🗑 Удалить
        </button>
      </li>
    );
  };
  
  export default TemplateItem;
  