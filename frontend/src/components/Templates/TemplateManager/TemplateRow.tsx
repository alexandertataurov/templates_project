import React from "react";
import { motion } from "framer-motion";
import { Button as AntButton, Input as AntInput } from "antd";
import { PlusOutlined } from "@ant-design/icons";
import { Template } from "../../../types/template";

export interface TemplateRowProps {
  template: Template;
  isEditing: boolean;
  tagColors: string[];
  editDisplayName: string;
  newEditField: string;
  editDynamicFields: string[];
  onEdit: (template: Template) => void;
  onUpdate: (template: Template) => void;
  onDelete: (id: number) => void;
  onCancelEdit: () => void;
  onChangeDisplayName: (value: string) => void;
  onAddEditField: () => void;
  onRemoveEditField: (field: string) => void;
  onSetNewEditField: (value: string) => void;
}

/**
 * TemplateRow renders a single table row for a template.
 */
const TemplateRow: React.FC<TemplateRowProps> = ({
  template,
  isEditing,
  tagColors,
  editDisplayName,
  newEditField,
  editDynamicFields,
  onEdit,
  onUpdate,
  onDelete,
  onCancelEdit,
  onChangeDisplayName,
  onAddEditField,
  onRemoveEditField,
  onSetNewEditField,
}) => {
  // Parse dynamic fields (if provided as a comma-separated string)
  const parseDynamicFields = (fields?: string[]): string[] => {
    if (Array.isArray(fields)) {
      if (fields.length === 1 && fields[0].includes(",")) {
        return fields[0].split(",").map(f => f.trim()).filter(Boolean);
      }
      return fields;
    }
    return [];
  };

  return (
    <motion.tr
      key={template.id}
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      whileHover={{ backgroundColor: "#f9fafb" }}
      transition={{ duration: 0.3 }}
    >
      <td className="template-manager__td">{template.id}</td>
      <td className="template-manager__td">{template.templateType || "contract"}</td>
      <td className="template-manager__td">
        {isEditing ? (
          <AntInput
            value={editDisplayName}
            onChange={(e) => onChangeDisplayName(e.target.value)}
            status={editDisplayName.trim() ? "" : "error"}
            aria-label="Template Display Name"
          />
        ) : (
          template.displayName
        )}
      </td>
      <td className="template-manager__td">
        {isEditing ? (
          <div>
            <div className="template-manager__tags">
              {editDynamicFields.map((field, idx) => (
                <motion.span
                  key={`${template.id}-${idx}`}
                  className={`template-manager__tag ${tagColors[idx % tagColors.length]}`}
                  initial={{ scale: 0.9 }}
                  animate={{ scale: 1 }}
                  exit={{ scale: 0.9 }}
                >
                  {field}
                  <button
                    type="button"
                    onClick={() => onRemoveEditField(field)}
                    aria-label={`Remove field ${field}`}
                    className="template-manager__tag-close"
                  >
                    ×
                  </button>
                </motion.span>
              ))}
            </div>
            <div className="template-manager__field-add">
              <AntInput
                value={newEditField}
                onChange={(e) => onSetNewEditField(e.target.value)}
                onPressEnter={onAddEditField}
                placeholder="Новое поле"
                aria-label="New Field Input"
                className="template-manager__input"
              />
              <AntButton
                type="primary"
                icon={<PlusOutlined />}
                onClick={onAddEditField}
                aria-label="Add New Field"
              />
            </div>
          </div>
        ) : (
          <div className="template-manager__tags">
            {parseDynamicFields(template.fields).map((field, idx) => (
              <span key={`${template.id}-${idx}`} className={`template-manager__tag ${tagColors[idx % tagColors.length]}`}>
                {field}
              </span>
            ))}
          </div>
        )}
      </td>
      <td className="template-manager__td">
        {isEditing ? (
          <div className="template-manager__actions">
            <AntButton type="primary" onClick={() => onUpdate(template)}>
              Сохранить
            </AntButton>
            <AntButton onClick={onCancelEdit}>Отмена</AntButton>
          </div>
        ) : (
          <div className="template-manager__actions">
            <AntButton
              type="primary"
              onClick={() => onEdit(template)}
              aria-label="Edit Template"
            >
              Редактировать
            </AntButton>
            <AntButton
              danger
              onClick={() => onDelete(template.id)}
              aria-label="Delete Template"
            >
              Удалить
            </AntButton>
          </div>
        )}
      </td>
    </motion.tr>
  );
};

export default TemplateRow;
