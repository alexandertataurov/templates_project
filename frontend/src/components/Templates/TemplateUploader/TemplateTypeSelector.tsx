import React from 'react';
import { Select as AntSelect } from 'antd';

interface TemplateTypeSelectorProps {
  value: string;
  onChange: (value: string) => void;
}

const TEMPLATE_TYPES = [
  { value: "contract", label: "Contract" },
  { value: "specification", label: "Specification" },
  { value: "addendum", label: "Addendum" },
];

const TemplateTypeSelector: React.FC<TemplateTypeSelectorProps> = ({ value, onChange }) => (
  <div className="template-uploader__field">
    <label className="template-uploader__label" htmlFor="template-type">
      Тип шаблона
    </label>
    <AntSelect
      id="template-type"
      value={value}
      onChange={onChange}
      className="template-uploader__select w-full"
      size="large"
      options={TEMPLATE_TYPES.map((type) => ({
        value: type.value,
        label: type.label,
      }))}
      aria-label="Template Type"
    />
  </div>
);

export default TemplateTypeSelector;
