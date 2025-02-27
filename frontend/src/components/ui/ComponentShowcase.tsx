import React, { useState } from "react";
import Button from "./Button";
import Input from "./Input";
import Card from "./Card";
import Modal from "./Modal";
import Checkbox from "./Checkbox";
import FormField from "./FormField";
import FileUploader from "./FileUploader";

const ComponentShowcase: React.FC = () => {
  const [inputValue, setInputValue] = useState("");
  const [isChecked, setIsChecked] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 p-6">
      <Card title="Поле ввода">
        <Input
          placeholder="Введите текст..."
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
        />
      </Card>

      <Card title="Чекбокс">
        <Checkbox
          label="Согласен с условиями"
          checked={isChecked}
          onChange={(e) => setIsChecked(e.target.checked)}
        />
      </Card>

      <Card title="Поле формы">
        <FormField label="Имя">
          <Input
            placeholder="Введите имя"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
          />
        </FormField>
      </Card>

      <Card title="Загрузка файла">
        <FileUploader onFileSelect={setSelectedFile} selectedFile={selectedFile} />
      </Card>

      <Card title="Модальное окно">
        <Button
          label="Открыть модальное окно"
          onClick={() => setModalOpen(true)}
          variant="save"
        />
        <Modal isOpen={modalOpen} onClose={() => setModalOpen(false)}>
          <p className="text-gray-700">Содержимое модального окна.</p>
        </Modal>
      </Card>
    </div>
  );
};

export default ComponentShowcase;