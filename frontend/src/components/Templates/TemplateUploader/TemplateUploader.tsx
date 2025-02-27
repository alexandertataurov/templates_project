import React, { useState, useCallback, useEffect, useRef } from "react";
import { motion } from "framer-motion";
import { toast } from "react-toastify";
import { Button } from "antd";
import { uploadTemplate } from "../../../api/templates";
import { TemplateFormData } from "../../../types/template";
import TemplateTypeSelector from "./TemplateTypeSelector";
import TemplateDisplayNameInput from "./TemplateDisplayNameInput";
import DynamicFieldsEditor from "./DynamicFieldsEditor";
import FileUploader from "./FileUploader";
import AutoExtractSwitch from "./AutoExtractSwitch";

// Initial form data state.
const INITIAL_FORM_DATA: TemplateFormData = {
  file: null,
  templateType: "contract",
  displayName: "",
  fields: [],
};

const TemplateUploader: React.FC = React.memo(() => {
  const [formData, setFormData] = useState<TemplateFormData>(INITIAL_FORM_DATA);
  const [uploading, setUploading] = useState<boolean>(false);
  // Removed extractFieldsEnabled state as auto-extraction is disabled.
  const [fileInfo, setFileInfo] = useState<string | null>(null);
  const [fieldInput, setFieldInput] = useState<string>("");

  // useRef to track if the component is still mounted.
  const isMountedRef = useRef<boolean>(true);
  useEffect(() => {
    isMountedRef.current = true;
    return () => {
      isMountedRef.current = false;
    };
  }, []);

  const handleSubmit = useCallback(
    async (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();

      // Validate that a file is selected.
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
      const maxFileSize = 5 * 1024 * 1024; // 5 MB
      if (!allowedTypes.includes(formData.file.type)) {
        toast.error("Неверный формат файла. Допустимые форматы: PDF, DOC, DOCX");
        return;
      }
      if (formData.file.size > maxFileSize) {
        toast.error("Размер файла превышает допустимый лимит в 5 MB");
        return;
      }

      // Validate display name.
      if (!formData.displayName.trim()) {
        toast.error("Название шаблона не может быть пустым");
        return;
      }

      setUploading(true);
      try {
        // Since auto-extraction is disabled (switch is off), we simply use the manually entered fields.
        const finalFields = formData.fields;
        const result = await uploadTemplate(
          formData.file,
          formData.templateType,
          formData.displayName,
          finalFields
        );
        toast.success(result.message);
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
    [formData]
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
      }
    },
    [formData.fields]
  );

  // Handler to remove an existing field.
  const handleRemoveField = useCallback(
    (field: string) => {
      setFormData((prev) => ({ ...prev, fields: prev.fields.filter((f) => f !== field) }));
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
        <TemplateTypeSelector
          value={formData.templateType}
          onChange={(value) => setFormData((prev) => ({ ...prev, templateType: value }))}
        />
        <TemplateDisplayNameInput
          value={formData.displayName}
          onChange={(e) => setFormData((prev) => ({ ...prev, displayName: e.target.value }))}
        />
        <DynamicFieldsEditor
          fields={formData.fields}
          fieldInput={fieldInput}
          onFieldInputChange={setFieldInput}
          onAddField={handleAddField}
          onRemoveField={handleRemoveField}
        />
        <FileUploader file={formData.file} fileInfo={fileInfo} onFileSelect={handleFileSelect} />
        {/* Render the disabled auto-extract switch */}
        <AutoExtractSwitch />
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
