import React from "react";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

export const Input: React.FC<InputProps> = ({ className, ...props }) => {
  return (
    <input
      className={`w-full border p-2 rounded-lg focus:ring-2 focus:ring-blue-500 transition-all ${className}`}
      {...props}
    />
  );
};
