import React from "react";
import { motion } from "framer-motion";

interface CardProps {
  title: string;
  children: React.ReactNode;
}

const Card: React.FC<CardProps> = ({ title, children }) => {
  return (
    <motion.div
      className="component-block"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <h3 className="component-title">{title}</h3>
      <div className="p-4">{children}</div>
    </motion.div>
  );
};

export default Card;