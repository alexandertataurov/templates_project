import React from "react";

interface CheckboxProps {
  label: string;
  checked: boolean;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

const Checkbox: React.FC<CheckboxProps> = ({ label, checked, onChange }) => {
  return (
    <label className="template-uploader__label flex items-center gap-2">
      <span className="toggle">
        <input type="checkbox" checked={checked} onChange={onChange} className="hidden" />
        <span className="slider" />
      </span>
      <span>{label}</span>
    </label>
  );
};

export default Checkbox;