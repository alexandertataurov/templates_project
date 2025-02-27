import React from "react";
import { motion } from "framer-motion";
import { Button as AntButton } from "antd";

export interface ButtonProps {
  label: string;
  onClick?: () => void;
  type?: "button" | "submit";
  variant?: "primary" | "secondary" | "danger" | "save" | "update" | "delete";
  disabled?: boolean;
}

const Button: React.FC<ButtonProps> = ({
  label,
  onClick,
  type = "button",
  variant = "primary",
  disabled = false,
}) => {
  const variantMap = {
    primary: "btn-save",
    secondary: "btn-outline",
    danger: "btn-delete",
    save: "btn-save",
    update: "btn-update",
    delete: "btn-delete",
  };

  return (
    <motion.div whileHover={{ scale: disabled ? 1 : 1.02 }} whileTap={{ scale: disabled ? 1 : 0.98 }}>
      <AntButton
        type={variant === "primary" || variant === "save" || variant === "update" ? "primary" : "default"}
        htmlType={type}
        onClick={onClick}
        disabled={disabled}
        className={`btn ${variantMap[variant] || "btn-save"}`}
        danger={variant === "danger" || variant === "delete"}
      >
        {label}
      </AntButton>
    </motion.div>
  );
};

export default Button;