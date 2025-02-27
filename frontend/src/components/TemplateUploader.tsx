import React, { useState, useCallback, useMemo, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { toast } from "react-toastify";
import { Button, Switch, Select as AntSelect, Input as AntInput } from "antd";
import { PlusOutlined, UploadOutlined } from "@ant-design/icons";
import { uploadTemplate, extractFields } from "../api/templates";
import { TemplateFormData } from "../types/template";

// Define supported template types.
const TEMPLATE_TYPES = [
  { value: "contract", label: "Contract" },
  { value: "specification", label: "Specification" },
  { value: "addendum", label: "Addendum" },
] as const;

// Initial form data state.
const INITIAL_FORM_DATA: TemplateFormData = {
  file: null,
  templateType: "contract",
  displayName: "",
  fields: [],
};

/**
 * TemplateUploader component allows users to upload new templates.
 * This version includes file validations and a cancellation pattern to prevent state updates on unmounted components.
 */
const TemplateUploader: React.FC = React.memo(() => {
  const [formData, setFormData] = useState<TemplateFormData>(INITIAL_FORM_DATA);
  const [uploading, setUploading] = useState(false);
  const [extractFieldsEnabled, setExtractFieldsEnabled] = useState(true);
  const [fileInfo, setFileInfo] = useState<string | null>(null);
  const [fieldInput, setFieldInput] = useState(""); // Controlled input for new dynamic field

  // Pre-defined tag colors for styling dynamic fields.
  const tagColors = useMemo(
    () => ["tag-0", "tag-1", "tag-2", "tag-3", "tag-4", "tag-5", "tag-6"],
    []
  );

  // Using a ref to track if the component is still mounted.
  const isMountedRef = useRef(true);
  useEffect(() => {
    isMountedRef.current = true;
    return () => {
      isMountedRef.current = false;
    };
  }, []);

  // Handle form submission with file type and size validations.
  const handleSubmit = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault();

      // Validate file selection.
      if (!formData.file) {
        toast.error("Пожалуйста, выберите файл");
        return;
      }

      // Validate allowed file types and maximum file size (5 MB).
      const allowedTypes = [
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      ];
      const maxFileSize = 5 * 1024 * 1024; // 5 MB in bytes

      if (!allowedTypes.includes(formData.file.type)) {
        toast.error("Неверный формат файла. Допустимые форматы: PDF, DOC, DOCX");
        return;
      }
      if (formData.file.size > maxFileSize) {
        toast.error("Размер файла превышает допустимый лимит в 5 MB");
        return;
      }

      // Validate non-empty display name.
      if (!formData.displayName.trim()) {
        toast.error("Название шаблона не может быть пустым");
        return;
      }

      setUploading(true);
      try {
        // Optionally extract fields from the file.
        const extractedFields = extractFieldsEnabled ? await extractFields(formData.file) : [];
        const finalFields = extractFieldsEnabled
          ? [...new Set([...formData.fields, ...extractedFields])]
          : formData.fields;

        const result = await uploadTemplate(
          formData.file,
          formData.templateType,
          formData.displayName,
          finalFields
        );

        toast.success(result.message);
        // Only update state if the component is still mounted.
        if (isMountedRef.current) {
          setFormData(INITIAL_FORM_DATA);
          setFileInfo(null);
          setFieldInput("");
        }
      } catch (error) {
        console.error("Ошибка загрузки шаблона:", error);
        toast.error(error instanceof Error ? error.message : "Ошибка загрузки");
      } finally {
        if (isMountedRef.current) {
          setUploading(false);
        }
      }
    },
    [formData, extractFieldsEnabled]
  );

  // Handle file selection from input or drag-and-drop.
  const handleFileSelect = useCallback((file: File | null) => {
    setFormData((prev) => ({ ...prev, file }));
    setFileInfo(file ? `${file.name} (${(file.size / 1024).toFixed(2)} KB)` : null);
  }, []);

  // Handler to add a new dynamic field.
  const handleAddField = useCallback(
    (newField: string) => {
      const trimmed = newField.trim();
      if (trimmed && !formData.fields.includes(trimmed)) {
        setFormData((prev) => ({ ...prev, fields: [...prev.fields, trimmed] }));
        setFieldInput("");
      }
    },
    [formData.fields]
  );

  // Handler to remove a dynamic field.
  const handleRemoveField = useCallback(
    (field: string) => {
      setFormData((prev) => ({
        ...prev,
        fields: prev.fields.filter((f) => f !== field),
      }));
    },
    []
  );

  return (
    <motion.div
      className="template-uploader"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <h2 className="template-uploader__title">Загрузка нового шаблона</h2>
      <form onSubmit={handleSubmit} className="template-uploader__form" noValidate>
        {/* Template type selection */}
        <div className="template-uploader__field">
          <label className="template-uploader__label" htmlFor="template-type">
            Тип шаблона
          </label>
          <AntSelect
            id="template-type"
            value={formData.templateType}
            onChange={(value) =>
              setFormData((prev) => ({ ...prev, templateType: value }))
            }
            className="template-uploader__select w-full"
            size="large"
            options={TEMPLATE_TYPES.map((type) => ({
              value: type.value,
              label: type.label,
            }))}
            aria-label="Template Type"
          />
        </div>

        {/* Template display name input */}
        <div className="template-uploader__field">
          <label className="template-uploader__label" htmlFor="display-name">
            Название шаблона
          </label>
          <AntInput
            id="display-name"
            value={formData.displayName}
            onChange={(e) =>
              setFormData((prev) => ({ ...prev, displayName: e.target.value }))
            }
            placeholder="Название шаблона"
            className="template-uploader__input"
            size="large"
            status={formData.displayName.trim() ? "" : "error"}
            aria-label="Template Display Name"
          />
        </div>

        {/* Dynamic fields input */}
        <div className="template-uploader__field">
          <label className="template-uploader__label" htmlFor="dynamic-fields">
            Динамические поля
          </label>
          <div className="template-uploader__tags" id="dynamic-fields">
            <AnimatePresence>
              {formData.fields.map((field, idx) => (
                <motion.span
                  key={`${field}-${idx}`}
                  className={`template-uploader__tag ${tagColors[idx % tagColors.length]}`}
                  initial={{ scale: 0.9 }}
                  animate={{ scale: 1 }}
                  exit={{ scale: 0.9 }}
                  transition={{ duration: 0.2 }}
                >
                  {field}
                  <button
                    type="button"
                    onClick={() => handleRemoveField(field)}
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
                setFieldInput(e.target.value);
                // If comma is detected, split and add multiple fields.
                if (e.target.value.includes(",")) {
                  const fields = e.target.value
                    .split(",")
                    .map((f) => f.trim())
                    .filter(Boolean);
                  fields.forEach(handleAddField);
                  setFieldInput("");
                }
              }}
              onPressEnter={(e) => handleAddField(e.currentTarget.value)}
              placeholder="Новое поле"
              className="template-uploader__input flex-1"
              size="large"
              aria-label="New Field Input"
            />
            <Button
              type="primary"
              icon={<PlusOutlined />}
              onClick={() => handleAddField(fieldInput)}
              className="btn-save"
              aria-label="Add Field"
            />
          </div>
        </div>

        {/* File upload */}
        <div className="template-uploader__field">
          <label className="template-uploader__label" htmlFor="file-upload">
            Файл шаблона
          </label>
          <div
            className={`template-uploader__upload-wrapper ${
              formData.file ? "border-green-500" : ""
            }`}
            onDragOver={(e) => e.preventDefault()}
            onDrop={(e) => {
              e.preventDefault();
              const file = e.dataTransfer.files[0];
              if (file) handleFileSelect(file);
            }}
          >
            <input
              type="file"
              onChange={(e) =>
                handleFileSelect(e.target.files?.[0] || null)
              }
              className="template-uploader__file-input"
              id="file-upload"
              aria-label="File Upload"
            />
            <label htmlFor="file-upload" className="template-uploader__file-label">
              <UploadOutlined className="template-uploader__file-label-icon" />
              <span className="template-uploader__file-label-text">
                {formData.file
                  ? "Заменить файл"
                  : "Перетащите файл или кликните для выбора"}
              </span>
            </label>
          </div>
          <AnimatePresence>
            {fileInfo && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className={`template-uploader__file-info ${
                  formData.file ? "template-uploader__file-info--success" : ""
                }`}
              >
                {fileInfo}
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Auto-extract fields switch */}
        <div className="template-uploader__field">
          <label
            className="template-uploader__label flex items-center gap-2"
            htmlFor="auto-extract"
          >
            <Switch
              id="auto-extract"
              checked={extractFieldsEnabled}
              onChange={setExtractFieldsEnabled}
              className="toggle"
              aria-label="Toggle auto-extract fields"
            />
            Автоизвлечение полей из шаблона
          </label>
        </div>

        {/* Submit button */}
        <motion.div
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className="template-uploader__button"
        >
          <Button
            type="primary"
            size="large"
            htmlType="submit"
            loading={uploading}
            disabled={uploading}
            className="btn-save w-full"
            aria-label="Upload Template"
          >
            {uploading ? "Загрузка..." : "Загрузить шаблон"}
          </Button>
        </motion.div>
      </form>
    </motion.div>
  );
});

export default TemplateUploader;
