import React from "react";
import { UploadOutlined } from "@ant-design/icons";

interface FileUploaderProps {
  file: File | null;
  fileInfo: string | null;
  onFileSelect: (file: File | null) => void;
}

/**
 * Handles file selection via input or drag-and-drop.
 */
const FileUploader: React.FC<FileUploaderProps> = ({ file, fileInfo, onFileSelect }) => (
  <div className="template-uploader__field">
    <label className="template-uploader__label" htmlFor="file-upload">
      Файл шаблона
    </label>
    <div
      className={`template-uploader__upload-wrapper ${file ? "border-green-500" : ""}`}
      onDragOver={(e) => e.preventDefault()}
      onDrop={(e) => {
        e.preventDefault();
        const droppedFile = e.dataTransfer.files[0];
        if (droppedFile) onFileSelect(droppedFile);
      }}
    >
      <input
        type="file"
        onChange={(e) => onFileSelect(e.target.files?.[0] || null)}
        className="template-uploader__file-input"
        id="file-upload"
        aria-label="File Upload"
      />
      <label htmlFor="file-upload" className="template-uploader__file-label">
        <UploadOutlined className="template-uploader__file-label-icon" />
        <span className="template-uploader__file-label-text">
          {file ? "Заменить файл" : "Перетащите файл или кликните для выбора"}
        </span>
      </label>
    </div>
    {fileInfo && (
      <div className={`template-uploader__file-info ${file ? "template-uploader__file-info--success" : ""}`}>
        {fileInfo}
      </div>
    )}
  </div>
);

export default FileUploader;
