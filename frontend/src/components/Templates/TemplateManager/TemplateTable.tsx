// TemplateTable.tsx
import React from "react";
import { motion } from "framer-motion";
import TemplateRow, { TemplateRowProps } from "./TemplateRow";
import { Template } from "../../../types/template";

interface TemplateTableProps {
  templates: Template[];
  rowProps: Omit<TemplateRowProps, "template" | "isEditing">;
  editingTemplateId: number | null; // Add this
  onRowAction: (template: Template, action: "edit" | "update" | "delete" | "cancel") => void;
}

const TemplateTable: React.FC<TemplateTableProps> = ({ templates, rowProps, editingTemplateId, onRowAction }) => (
  <motion.div className="template-manager__table-container" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.3 }}>
    <table className="template-manager__table">
      <thead>
        <tr>
          <th className="template-manager__th">ID</th>
          <th className="template-manager__th">Тип</th>
          <th className="template-manager__th">Название</th>
          <th className="template-manager__th">Поля</th>
          <th className="template-manager__th">Действия</th>
        </tr>
      </thead>
      <tbody>
        {templates.map((template) => (
          <TemplateRow
            key={template.id}
            template={template}
            isEditing={template.id === editingTemplateId} // Compute per row
            {...rowProps}
            onEdit={() => onRowAction(template, "edit")}
            onUpdate={() => onRowAction(template, "update")}
            onDelete={() => onRowAction(template, "delete")}
            onCancelEdit={() => onRowAction(template, "cancel")}
          />
        ))}
      </tbody>
    </table>
  </motion.div>
);

export default TemplateTable;