// TemplateTable.tsx
import React from "react";
import { motion } from "framer-motion";
import TemplateRow, { TemplateRowProps } from "./TemplateRow";
import { Template } from "../../types/template";

interface TemplateTableProps {
  templates: Template[];
  rowProps: Omit<TemplateRowProps, "template">; // common props for each row
  onRowAction: (template: Template, action: "edit" | "update" | "delete" | "cancel") => void;
}

const TemplateTable: React.FC<TemplateTableProps> = ({ templates, rowProps, onRowAction }) => (
  <motion.div
    className="template-table-container"
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
    transition={{ duration: 0.3 }}
  >
    <table className="template-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Тип</th>
          <th>Название</th>
          <th>Поля</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        {templates.map((template) => (
          <TemplateRow
            key={template.id}
            template={template}
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
