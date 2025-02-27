import React, { useState, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { toast } from "react-toastify";
import { Button, Switch, Select as AntSelect, Input as AntInput } from "antd";
import { PlusOutlined, UploadOutlined } from "@ant-design/icons";
import { uploadTemplate, extractFields } from "../api/templates";
import { TemplateFormData } from "../types/template";

const TEMPLATE_TYPES = [
  { value: "contract", label: "Contract" },
  { value: "specification", label: "Specification" },
  { value: "addendum", label: "Addendum" },
] as const;

const INITIAL_FORM_DATA: TemplateFormData = {
  file: null,
  templateType: "contract",
  displayName: "",
  fields: [],
};

const TemplateUploader: React.FC = () => {
  const [formData, setFormData] = useState<TemplateFormData>(INITIAL_FORM_DATA);
  const [uploading, setUploading] = useState(false);
  const [extractFieldsEnabled, setExtractFieldsEnabled] = useState(true);
  const [fileInfo, setFileInfo] = useState<string | null>(null);
  const [fieldInput, setFieldInput] = useState(""); // New state for controlled input

  const tagColors = ["tag-0", "tag-1", "tag-2", "tag-3", "tag-4", "tag-5", "tag-6"];

  const handleSubmit = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault();
      if (!formData.file) {
        toast.error("Пожалуйста, выберите файл");
        return;
      }
      if (!formData.displayName.trim()) {
        toast.error("Название шаблона не может быть пустым");
        return;
      }

      setUploading(true);
      try {
        const finalFields = extractFieldsEnabled
          ? [...new Set([...formData.fields, ...(await extractFields(formData.file))])]
          : formData.fields;

        const result = await uploadTemplate(
          formData.file,
          formData.templateType,
          formData.displayName,
          finalFields
        );

        toast.success(result.message);
        setFormData(INITIAL_FORM_DATA);
        setFileInfo(null);
        setFieldInput(""); // Reset field input on successful upload
      } catch (error) {
        toast.error(error instanceof Error ? error.message : "Ошибка загрузки");
      } finally {
        setUploading(false);
      }
    },
    [formData, extractFieldsEnabled]
  );

  const handleFileSelect = useCallback((file: File | null) => {
    setFormData((prev) => ({ ...prev, file }));
    setFileInfo(file ? `${file.name} (${(file.size / 1024).toFixed(2)} KB)` : null);
  }, []);

  const handleAddField = useCallback(
    (newField: string) => {
      const trimmed = newField.trim();
      if (trimmed && !formData.fields.includes(trimmed)) {
        setFormData((prev) => ({ ...prev, fields: [...prev.fields, trimmed] }));
        setFieldInput(""); // Clear input after adding
      }
    },
    [formData.fields]
  );

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
      <form onSubmit={handleSubmit} className="template-uploader__form">
        <div className="template-uploader__field">
          <label className="template-uploader__label">Тип шаблона</label>
          <AntSelect
            value={formData.templateType}
            onChange={(value) => setFormData((prev) => ({ ...prev, templateType: value }))}
            className="template-uploader__select w-full"
            size="large"
            options={TEMPLATE_TYPES.map((type) => ({
              value: type.value,
              label: type.label,
            }))}
          />
        </div>

        <div className="template-uploader__field">
          <label className="template-uploader__label">Название шаблона</label>
          <AntInput
            value={formData.displayName}
            onChange={(e) => setFormData((prev) => ({ ...prev, displayName: e.target.value }))}
            placeholder="Название шаблона"
            className="template-uploader__input"
            size="large"
            status={formData.displayName.trim() ? "" : "error"}
          />
        </div>

        <div className="template-uploader__field">
          <label className="template-uploader__label">Динамические поля</label>
          <div className="template-uploader__tags">
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
                if (e.target.value.includes(",")) {
                  const fields = e.target.value
                    .split(",")
                    .map((f) => f.trim())
                    .filter(Boolean);
                  fields.forEach(handleAddField);
                  setFieldInput("");
                }
              }}
              onPressEnter={(e) => {
                handleAddField(e.currentTarget.value);
              }}
              placeholder="Новое поле"
              className="template-uploader__input flex-1"
              size="large"
            />
            <Button
              type="primary"
              icon={<PlusOutlined />}
              onClick={() => handleAddField(fieldInput)}
              className="btn-save"
            />
          </div>
        </div>

        <div className="template-uploader__field">
          <label className="template-uploader__label">Файл шаблона</label>
          <div
            className={`template-uploader__upload-wrapper ${formData.file ? "border-green-500" : ""}`}
            onDragOver={(e) => e.preventDefault()}
            onDrop={(e) => {
              e.preventDefault();
              const file = e.dataTransfer.files[0];
              if (file) handleFileSelect(file);
            }}
          >
            <input
              type="file"
              onChange={(e) => handleFileSelect(e.target.files?.[0] || null)}
              className="template-uploader__file-input"
              id="file-upload"
            />
            <label htmlFor="file-upload" className="template-uploader__file-label">
              <UploadOutlined className="template-uploader__file-label-icon" />
              <span className="template-uploader__file-label-text">
                {formData.file ? "Заменить файл" : "Перетащите файл или кликните для выбора"}
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

        <div className="template-uploader__field">
          <label className="template-uploader__label flex items-center gap-2">
            <Switch
              checked={extractFieldsEnabled}
              onChange={setExtractFieldsEnabled}
              className="toggle"
            />
            Автоизвлечение полей из шаблона
          </label>
        </div>

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
          >
            {uploading ? "Загрузка..." : "Загрузить шаблон"}
          </Button>
        </motion.div>
      </form>
    </motion.div>
  );
};

export default TemplateUploader;