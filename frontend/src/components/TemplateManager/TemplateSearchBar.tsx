// TemplateSearchBar.tsx
import React, { ChangeEvent } from "react";
import { Input as AntInput, Button as AntButton } from "antd";
import { SearchOutlined } from "@ant-design/icons";

interface TemplateSearchBarProps {
  searchQuery: string;
  onSearchChange: (e: ChangeEvent<HTMLInputElement>) => void;
  onRefresh: () => void;
}

const TemplateSearchBar: React.FC<TemplateSearchBarProps> = ({ searchQuery, onSearchChange, onRefresh }) => (
  <div className="template-search-bar">
    <AntInput
      prefix={<SearchOutlined />}
      placeholder="Поиск шаблонов..."
      value={searchQuery}
      onChange={onSearchChange}
      size="large"
      aria-label="Search Templates"
    />
    <AntButton type="primary" size="large" onClick={onRefresh} aria-label="Refresh Templates">
      Обновить
    </AntButton>
  </div>
);

export default TemplateSearchBar;
