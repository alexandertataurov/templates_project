import React from "react";

interface Props {
  value: string;
  onChange: (value: string) => void;
}

const TemplateTypeSelector: React.FC<Props> = ({ value, onChange }) => {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="w-full border p-2 mt-2 rounded"
    >
      <option value="">Выберите тип шаблона</option>
      <option value="contract">Договор</option>
      <option value="specification">Спецификация</option>
      <option value="addendum">Дополнение</option>
    </select>
  );
};

export default TemplateTypeSelector;
