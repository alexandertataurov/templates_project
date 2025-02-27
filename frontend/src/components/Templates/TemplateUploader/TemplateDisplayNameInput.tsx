import React from "react";
import { Input as AntInput } from "antd";

interface TemplateDisplayNameInputProps {
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

const TemplateDisplayNameInput: React.FC<TemplateDisplayNameInputProps> = ({ value, onChange }) => (
  <div className="template-uploader__field">
    <label className="template-uploader__label" htmlFor="display-name">
      Название шаблона
    </label>
    <AntInput
      id="display-name"
      value={value}
      onChange={onChange}
      placeholder="Название шаблона"
      className="template-uploader__input"
      size="large"
      status={value.trim() ? "" : "error"}
      aria-label="Template Display Name"
    />
  </div>
);

export default TemplateDisplayNameInput;
