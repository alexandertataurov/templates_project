import React, { useEffect, useState, useCallback, ChangeEvent } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Button as AntButton, message, Input as AntInput } from "antd";
import { PlusOutlined, SearchOutlined } from "@ant-design/icons";
import { listTemplates, updateTemplate, deleteTemplate, Template } from "../api/templates";

const TemplateManager: React.FC = () => {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [editingTemplateId, setEditingTemplateId] = useState<number | null>(null);
  const [editDisplayName, setEditDisplayName] = useState<string>("");
  const [editDynamicFields, setEditDynamicFields] = useState<string[]>([]);
  const [newEditField, setNewEditField] = useState<string>("");
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [debouncedQuery, setDebouncedQuery] = useState<string>("");

  const tagColors = ["tag-0", "tag-1", "tag-2", "tag-3", "tag-4", "tag-5", "tag-6"];

  // Debounce search query
  useEffect(() => {
    const handler = setTimeout(() => setDebouncedQuery(searchQuery), 300);
    return () => clearTimeout(handler);
  }, [searchQuery]);

  // Auto-clear error after 5 seconds
  useEffect(() => {
    if (error) {
      const timer = setTimeout(() => setError(null), 5000);
      return () => clearTimeout(timer);
    }
  }, [error]);

  // Fetch templates
  const fetchTemplates = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await listTemplates();
      data.sort((a: Template, b: Template) => a.id - b.id);
      setTemplates(data);
    } catch (err) {
      setError("Ошибка загрузки шаблонов");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTemplates();
  }, [fetchTemplates]);

  // Parse dynamic fields
  const parseDynamicFields = (fields?: string[]): string[] => {
    if (Array.isArray(fields)) {
      if (fields.length === 1 && fields[0].includes(",")) {
        return fields[0].split(",").map(f => f.trim()).filter(Boolean);
      }
      return fields;
    }
    return [];
  };

  // Edit handlers
  const handleEdit = useCallback((template: Template) => {
    setEditingTemplateId(template.id);
    setEditDisplayName(template.displayName);
    setEditDynamicFields(parseDynamicFields(template.fields));
    setNewEditField("");
  }, []);

  const handleAddEditField = useCallback(() => {
    const trimmed = newEditField.trim();
    if (trimmed && !editDynamicFields.includes(trimmed)) {
      setEditDynamicFields([...editDynamicFields, trimmed]);
      setNewEditField("");
    }
  }, [newEditField, editDynamicFields]);

  const handleRemoveEditField = useCallback(
    (field: string) => {
      setEditDynamicFields(editDynamicFields.filter(f => f !== field));
    },
    [editDynamicFields]
  );

  const handleUpdate = useCallback(
    async (template: Template) => {
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
    },
    [editDisplayName, editDynamicFields, fetchTemplates]
  );

  const handleDelete = useCallback(
    async (templateId: number) => {
      if (window.confirm("Вы уверены, что хотите удалить этот шаблон?")) {
        try {
          await deleteTemplate(templateId);
          message.success("Шаблон успешно удален");
          await fetchTemplates();
        } catch (error) {
          message.error("Ошибка удаления шаблона");
        }
      }
    },
    [fetchTemplates]
  );

  // Filter templates based on debounced query
  const filteredTemplates = templates.filter((template) =>
    (template.displayName || "").toLowerCase().includes(debouncedQuery.toLowerCase())
  );

  return (
    <motion.div
      className="template-manager"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <h2 className="template-manager__title">Управление шаблонами</h2>
      <div className="template-manager__controls">
        <AntInput
          prefix={<SearchOutlined />}
          placeholder="Поиск шаблонов..."
          value={searchQuery}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setSearchQuery(e.target.value)}
          className="template-manager__search-input"
          size="large"
        />
        <AntButton
          type="primary"
          size="large"
          onClick={fetchTemplates}
          className="btn-update"
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
          <motion.div
            className="template-manager__table-container"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.3 }}
          >
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
                {filteredTemplates.map((template, index) => (
                  <motion.tr
                    key={template.id ?? index}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    whileHover={{ backgroundColor: "#f9fafb" }}
                    transition={{ duration: 0.3 }}
                  >
                    <td className="template-manager__td">{template.id}</td>
                    <td className="template-manager__td">
                      {template.templateType || "contract"}
                    </td>
                    <td className="template-manager__td">
                      {editingTemplateId === template.id ? (
                        <AntInput
                          value={editDisplayName}
                          onChange={(e) => setEditDisplayName(e.target.value)}
                          className="template-manager__input"
                          status={editDisplayName.trim() ? "" : "error"}
                        />
                      ) : (
                        template.displayName
                      )}
                    </td>
                    <td className="template-manager__td">
                      {editingTemplateId === template.id ? (
                        <div className="template-manager__edit-fields">
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
                                  onClick={() => handleRemoveEditField(field)}
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
                              onChange={(e) => setNewEditField(e.target.value)}
                              onPressEnter={handleAddEditField}
                              placeholder="Новое поле"
                              className="template-manager__input template-manager__input--flex"
                            />
                            <AntButton
                              type="primary"
                              icon={<PlusOutlined />}
                              onClick={handleAddEditField}
                            />
                          </div>
                        </div>
                      ) : (
                        <div className="template-manager__tags">
                          {parseDynamicFields(template.fields).map((field, idx) => (
                            <span
                              key={`${template.id}-${idx}`}
                              className={`template-manager__tag ${tagColors[idx % tagColors.length]}`}
                            >
                              {field}
                            </span>
                          ))}
                        </div>
                      )}
                    </td>
                    <td className="template-manager__td">
                      {editingTemplateId === template.id ? (
                        <div className="template-manager__actions">
                          <AntButton
                            type="primary"
                            className="btn-save"
                            onClick={() => handleUpdate(template)}
                          >
                            Сохранить
                          </AntButton>
                          <AntButton
                            className="btn-outline"
                            onClick={() => setEditingTemplateId(null)}
                          >
                            Отмена
                          </AntButton>
                        </div>
                      ) : (
                        <div className="template-manager__actions">
                          <AntButton
                            type="primary"
                            className="btn-update"
                            onClick={() => handleEdit(template)}
                          >
                            Редактировать
                          </AntButton>
                          <AntButton
                            danger
                            className="btn-delete"
                            onClick={() => handleDelete(template.id)}
                            data-testid={`delete-template-${template.id}`}
                          >
                            Удалить
                          </AntButton>
                        </div>
                      )}
                    </td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

export default TemplateManager;