import React, { useState, useCallback, ChangeEvent, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { message, Input as AntInput, Button as AntButton } from "antd";
import useTemplates from "../../../hooks/useTemplates";
import ErrorBoundary from "../../ErrorBoundary";
import TemplateTable from "./TemplateTable";
import { Template } from "../../../types/template";
import { updateTemplate, deleteTemplate } from "../../../api/templates";
import { useDebouncedValue } from "../../../hooks/useDebounceValue";

const TemplateManager: React.FC = () => {
  const { templates, loading, error, fetchTemplates } = useTemplates();
  const [editingTemplateId, setEditingTemplateId] = useState<number | null>(null);
  const [editDisplayName, setEditDisplayName] = useState<string>("");
  const [editDynamicFields, setEditDynamicFields] = useState<string[]>([]);
  const [newEditField, setNewEditField] = useState<string>("");
  const [searchQuery, setSearchQuery] = useState<string>("");

  const debouncedQuery = useDebouncedValue(searchQuery, 300);

  const tagColors = useMemo(
    () => ["tag-0", "tag-1", "tag-2", "tag-3", "tag-4", "tag-5", "tag-6"],
    []
  );

  // Handle row actions (edit, update, delete, cancel) for each template.
  const handleRowAction = useCallback(
    async (template: Template, action: "edit" | "update" | "delete" | "cancel") => {
      if (action === "edit") {
        setEditingTemplateId(template.id);
        setEditDisplayName(template.displayName);
        setEditDynamicFields(template.fields);
        setNewEditField("");
      } else if (action === "cancel") {
        setEditingTemplateId(null);
      } else if (action === "update") {
        if (!editDisplayName.trim()) {
          message.error("Название шаблона не может быть пустым");
          return;
        }
        try {
          await updateTemplate(template.id, {
            displayName: editDisplayName,
            fields: editDynamicFields,
          });
          await fetchTemplates();
          setEditingTemplateId(null);
          message.success("Шаблон успешно обновлен");
        } catch (err) {
          console.error("Update failed:", err);
          message.error("Ошибка обновления шаблона");
        }
      } else if (action === "delete") {
        if (window.confirm("Вы уверены, что хотите удалить этот шаблон?")) {
          try {
            await deleteTemplate(template.id);
            message.success("Шаблон успешно удален");
            await fetchTemplates();
          } catch (error) {
            message.error("Ошибка удаления шаблона");
          }
        }
      }
    },
    [editDisplayName, editDynamicFields, fetchTemplates]
  );

  // Filter templates based on the debounced search query.
  const filteredTemplates = useMemo(() => {
    return templates.filter((template) =>
      (template.displayName || "").toLowerCase().includes(debouncedQuery.toLowerCase())
    );
  }, [templates, debouncedQuery]);

  // Common row properties (excluding the per-row "isEditing" which is computed per row)
  const rowProps = {
    tagColors,
    editDisplayName,
    newEditField,
    editDynamicFields,
    onChangeDisplayName: setEditDisplayName,
    onAddEditField: () => {
      const trimmed = newEditField.trim();
      if (trimmed && !editDynamicFields.includes(trimmed)) {
        setEditDynamicFields([...editDynamicFields, trimmed]);
        setNewEditField("");
      }
    },
    onRemoveEditField: (field: string) =>
      setEditDynamicFields(editDynamicFields.filter((f) => f !== field)),
    onSetNewEditField: setNewEditField,
    onUpdate: (template: Template) => handleRowAction(template, "update"),
    onEdit: (template: Template) => handleRowAction(template, "edit"),
    onDelete: (id: number) => handleRowAction({ id } as Template, "delete"),
    onCancelEdit: () => setEditingTemplateId(null),
  };

  return (
    <ErrorBoundary>
      <motion.div
        className="template-manager"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h2 className="template-manager__title">Управление шаблонами</h2>
        <div className="template-manager__controls">
          <AntInput
            prefix={null}
            placeholder="Поиск шаблонов..."
            value={searchQuery}
            onChange={(e: ChangeEvent<HTMLInputElement>) => setSearchQuery(e.target.value)}
            className="template-manager__search-input"
            size="large"
            aria-label="Search Templates"
          />
          <AntButton
            type="primary"
            size="large"
            onClick={fetchTemplates}
            className="btn-update"
            aria-label="Refresh Templates"
          >
            Обновить
          </AntButton>
        </div>

        <AnimatePresence>
          {loading ? (
            <motion.div
              className="template-manager__loading"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <svg
                className="w-8 h-8 text-blue-500 animate-spin"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
              </svg>
            </motion.div>
          ) : error ? (
            <motion.div
              className="template-manager__error"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              {error}
            </motion.div>
          ) : filteredTemplates.length === 0 ? (
            <motion.div
              className="template-manager__no-results"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              Шаблоны не найдены
            </motion.div>
          ) : (
            <TemplateTable
              templates={filteredTemplates}
              rowProps={rowProps}
              editingTemplateId={editingTemplateId} // Pass this
              onRowAction={handleRowAction}
              />
          )}
        </AnimatePresence>
      </motion.div>
    </ErrorBoundary>
  );
};

export default TemplateManager;
