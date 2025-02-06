import { Suspense, lazy } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";

const Home = lazy(() => import("./pages/Home"));
const CheckStatus = lazy(() => import("./pages/CheckStatus"));
const ManageFields = lazy(() => import("./pages/ManageFields"));
const UploadTemplate = lazy(() => import("./components/UploadTemplate"));
const Wizard = lazy(() => import("./pages/Wizard"));

const ErrorBoundary = ({ children }: { children: React.ReactNode }) => {
  try {
    return <>{children}</>;
  } catch (error) {
    console.error("🔥 Ошибка в маршрутах:", error);
    return <div className="text-red-500 p-6">🚨 Ошибка загрузки страницы!</div>;
  }
};

const AppRouter = () => {
  console.log("🚀 Router загружен");

  return (
    <Router>
      <Navbar />
      <ErrorBoundary>
        <Suspense fallback={<div className="text-center p-6">⏳ Загрузка...</div>}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/check-status" element={<CheckStatus />} />
            <Route path="/manage-fields" element={<ManageFields />} />
            <Route path="/upload-template" element={<UploadTemplate />} />
            <Route path="/wizard" element={<Wizard onComplete={() => window.location.href = "/"} />} />
          </Routes>
        </Suspense>
      </ErrorBoundary>
    </Router>
  );
};

export default AppRouter;
