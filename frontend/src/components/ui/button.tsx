import React from "react";
import clsx from "clsx";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "destructive" | "success" | "outline";
}

const variants = {
  default: "bg-gray-700 hover:bg-gray-800 text-white",
  destructive: "bg-red-600 hover:bg-red-700 text-white",
  success: "bg-green-600 hover:bg-green-700 text-white",
  outline: "border border-gray-500 text-gray-700 hover:bg-gray-100",
} as const;

export const Button: React.FC<ButtonProps> = ({ variant = "default", className, ...props }) => {
  return (
    <button className={clsx("px-4 py-2 rounded transition-all", variants[variant], className)} {...props} />
  );
};
