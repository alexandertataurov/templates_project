import { useState } from "react";
import FieldList from "../components/FieldList";

const ManageFields = () => {
  const [fields, setFields] = useState<string[]>([]);
  const [newField, setNewField] = useState("");

  return (
    <div className="container mx-auto p-6">
      <h1>📝 Управление полями</h1>
      <input type="text" onChange={(e) => setNewField(e.target.value)} className="border p-2 w-full mt-4 rounded" />
      <button onClick={() => setFields([...fields, newField])} className="w-full bg-blue-500 text-white p-2 mt-4 rounded">➕ Добавить</button>
      <FieldList fields={fields} removeField={(field) => setFields(fields.filter(f => f !== field))} />
    </div>
  );
};

export default ManageFields;
