import React, { useState, useCallback } from 'react';
import { motion } from 'framer-motion';
import Button from './Button';

interface FieldsEditorProps {
  fields: string[];
  onChange: (fields: string[]) => void;
}

const FieldsEditor: React.FC<FieldsEditorProps> = ({ fields, onChange }) => {
  const [newField, setNewField] = useState('');

  const handleAddField = useCallback(() => {
    const trimmed = newField.trim();
    if (trimmed && !fields.includes(trimmed)) {
      onChange([...fields, trimmed]);
      setNewField('');
    }
  }, [newField, fields, onChange]);

  const handleRemoveField = useCallback((fieldToRemove: string) => {
    onChange(fields.filter(field => field !== fieldToRemove));
  }, [fields, onChange]);

  return (
    <div className="fields-editor">
      <div className="fields-editor__input-row">
        <input
          type="text"
          value={newField}
          onChange={e => setNewField(e.target.value)}
          placeholder="Add new field (e.g., seller)"
          className="fields-editor__input"
          onKeyPress={e => e.key === 'Enter' && handleAddField()}
        />
        <Button
          label="Add"
          onClick={handleAddField}
          variant="secondary"
          disabled={!newField.trim()}
        />
      </div>

      <div className="fields-editor__tags">
        {fields.map((field, index) => (
          <motion.span
            key={`${field}-${index}`}
            className={`fields-editor__tag tag-${index % 7}`}
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
          >
            {field}
            <button
              type="button"
              onClick={() => handleRemoveField(field)}
              className="fields-editor__tag-remove"
            >
              ×
            </button>
          </motion.span>
        ))}
      </div>

      {fields.length > 0 && (
        <div className="fields-editor__help">
          <p>Use these fields in your template with curly braces: <code>{`{${fields[0]}}`}</code></p>
        </div>
      )}
    </div>
  );
};

export default FieldsEditor; 