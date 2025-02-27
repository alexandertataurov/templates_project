import React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Button, Input as AntInput } from "antd";
import { PlusOutlined } from "@ant-design/icons";

interface DynamicFieldsEditorProps {
  fields: string[];
  fieldInput: string;
  onFieldInputChange: (value: string) => void;
  onAddField: (value: string) => void;
  onRemoveField: (field: string) => void;
}

/**
 * Renders the list of dynamic fields and an input for adding new ones.
 */
const DynamicFieldsEditor: React.FC<DynamicFieldsEditorProps> = ({
  fields,
  fieldInput,
  onFieldInputChange,
  onAddField,
  onRemoveField,
}) => {
  const handleAddField = () => {
    const trimmed = fieldInput.trim();
    if (trimmed && !fields.includes(trimmed)) {
      onAddField(trimmed);
      onFieldInputChange("");
    }
  };

  return (
    <div className="template-uploader__field">
      <label className="template-uploader__label" htmlFor="dynamic-fields">
        Динамические поля
      </label>
      <div className="template-uploader__tags" id="dynamic-fields">
        <AnimatePresence>
          {fields.map((field, idx) => (
            <motion.span
              key={`${field}-${idx}`}
              className="template-uploader__tag"
              initial={{ scale: 0.9 }}
              animate={{ scale: 1 }}
              exit={{ scale: 0.9 }}
              transition={{ duration: 0.2 }}
            >
              {field}
              <button
                type="button"
                onClick={() => onRemoveField(field)}
                className="template-uploader__tag-close"
                aria-label={`Remove field ${field}`}
              >
                ×
              </button>
            </motion.span>
          ))}
        </AnimatePresence>
      </div>
      <div className="template-uploader__row mt-2">
        <AntInput
          value={fieldInput}
          onChange={(e) => {
            onFieldInputChange(e.target.value);
            if (e.target.value.includes(",")) {
              const fieldsArr = e.target.value
                .split(",")
                .map((f) => f.trim())
                .filter(Boolean);
              fieldsArr.forEach((f) => onAddField(f));
              onFieldInputChange("");
            }
          }}
          onPressEnter={handleAddField}
          placeholder="Новое поле"
          className="template-uploader__input flex-1"
          size="large"
          aria-label="New Field Input"
        />
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={handleAddField}
          className="btn-save"
          aria-label="Add Field"
        />
      </div>
    </div>
  );
};

export default DynamicFieldsEditor;
