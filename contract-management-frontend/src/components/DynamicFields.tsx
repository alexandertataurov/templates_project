interface DynamicFieldsProps {
  fields: string[];
  setFields: (fields: string[]) => void;
}

const DynamicFields = ({ fields, setFields }: DynamicFieldsProps) => {
  const handleFieldChange = (index: number, value: string) => {
    const newFields = [...fields];
    newFields[index] = value;
    setFields(newFields);
  };

  const addField = () => setFields([...fields, ""]);
  const removeField = (index: number) => {
    setFields(fields.filter((_, i) => i !== index));
  };

  return (
    <div className="mt-4">
      <h3 className="font-bold">📌 Динамические поля</h3>
      {fields.map((field, index) => (
        <div key={index} className="flex gap-2 mt-2">
          <input
            type="text"
            placeholder={`Поле ${index + 1}`}
            value={field}
            onChange={(e) => handleFieldChange(index, e.target.value)}
            className="w-full border p-2 rounded"
          />
          {fields.length > 1 && (
            <button
              onClick={() => removeField(index)}
              className="bg-red-500 text-white px-3 py-1 rounded"
            >
              ❌
            </button>
          )}
        </div>
      ))}
      <button onClick={addField} className="w-full bg-gray-500 text-white p-2 mt-2 rounded">
        ➕ Добавить поле
      </button>
    </div>
  );
};

export default DynamicFields;
