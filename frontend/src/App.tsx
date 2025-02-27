import React, { Suspense, lazy } from "react";
import { motion } from "framer-motion";
import Navbar from "./components/ui/Navbar";
import ErrorBoundary from "./components/ErrorBoundary";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
// Import the React 19 compatibility patch for antd v5
import "@ant-design/v5-patch-for-react-19";

const TemplateManager = lazy(() => import("./components/TemplateManager"));
const TemplateUploader = lazy(() => import("./components/TemplateUploader"));

const App: React.FC = () => {
  return (
    <div className="app-container">
      <Navbar />
      <main className="container">
        <ErrorBoundary>
          <Suspense
            fallback={
              <div className="flex items-center justify-center min-h-[50vh]">
                <svg
                  className="w-8 h-8 text-blue-500 animate-spin"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8v8z"
                  />
                </svg>
              </div>
            }
          >
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5 }}
            >
              <TemplateUploader />
              <TemplateManager />
            </motion.div>
          </Suspense>
        </ErrorBoundary>
      </main>
      <ToastContainer
        position="top-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="light"
      />
    </div>
  );
};

export default App;