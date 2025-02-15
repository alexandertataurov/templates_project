const FieldList = ({ fields, removeField }: { fields: string[], removeField: (field: string) => void }) => (
    <ul className="mt-4">
      {fields.map((field, index) => (
        <li key={index} className="flex justify-between p-2 border-b">
          {field}
          <button onClick={() => removeField(field)} className="bg-red-500 text-white px-2 py-1 rounded">❌</button>
        </li>
      ))}
    </ul>
  );
  
  export default FieldList;
  