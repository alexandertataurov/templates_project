import React, { useState } from "react";
import Input from "./Input";
import Button from "./Button";

interface SearchBarProps {
  placeholder?: string;
  onSearch: (query: string) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ placeholder = "Поиск...", onSearch }) => {
  const [query, setQuery] = useState("");

  const handleSearch = () => {
    onSearch(query);
  };

  return (
    <div className="flex items-center space-x-2">
      <Input 
        placeholder={placeholder} 
        value={query} 
        onChange={(e) => setQuery(e.target.value)} 
      />
      <Button label="Найти" onClick={handleSearch} variant="primary" />
    </div>
  );
};

export default SearchBar;
