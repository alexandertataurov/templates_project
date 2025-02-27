import React from "react";

interface FormFieldProps {
  label: string;
  children: React.ReactNode;
}

const FormField: React.FC<FormFieldProps> = ({ label, children }) => {
  return (
    <div className="template-uploader__field">
      <label className="template-uploader__label">{label}</label>
      <div>{children}</div>
    </div>
  );
};

export default FormField;