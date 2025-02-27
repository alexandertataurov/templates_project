import React, { useState, useCallback } from "react";
import { motion } from "framer-motion";
import { UploadOutlined } from "@ant-design/icons";

interface FileUploaderProps {
  onFileSelect: (file: File | null) => void; // Allow null for reset
  selectedFile: File | null;
}

const FileUploader: React.FC<FileUploaderProps> = ({ onFileSelect, selectedFile }) => {
  const [dragOver, setDragOver] = useState(false);

  const handleDrop = useCallback(
    (e: React.DragEvent<HTMLDivElement>) => {
      e.preventDefault();
      setDragOver(false);
      const file = e.dataTransfer.files?.[0];
      if (file) onFileSelect(file);
    },
    [onFileSelect]
  );

  const handleFileChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0] || null;
      onFileSelect(file);
    },
    [onFileSelect]
  );

  return (
    <motion.div
      className={`template-uploader__upload-wrapper ${dragOver ? "dragover" : ""} ${selectedFile ? "border-green-500" : ""}`}
      onDragOver={(e) => {
        e.preventDefault();
        setDragOver(true);
      }}
      onDragLeave={(e) => {
        e.preventDefault();
        setDragOver(false);
      }}
      onDrop={handleDrop}
      whileHover={{ scale: 1.01 }}
      transition={{ duration: 0.2 }}
    >
      <input
        type="file"
        onChange={handleFileChange}
        className="template-uploader__file-input"
        accept=".doc,.docx"
        id="file-uploader"
      />
      <label htmlFor="file-uploader" className="template-uploader__file-label">
        <UploadOutlined className="template-uploader__file-label-icon" />
        <span className="template-uploader__file-label-text">
          {selectedFile ? selectedFile.name : "Перетащите файл или кликните для выбора"}
        </span>
      </label>
    </motion.div>
  );
};

export default FileUploader;