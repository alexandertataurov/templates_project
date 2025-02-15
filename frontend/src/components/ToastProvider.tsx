import React from "react";
import { ToastContainer, toast } from "react-toastify";

export const notifySuccess = (message: string) => {
  toast.success(message, { position: "top-right", autoClose: 3000 });
};

export const notifyError = (message: string) => {
  toast.error(message, { position: "top-right", autoClose: 3000 });
};

const Toast: React.FC = () => <ToastContainer />;

export default React.memo(Toast);
