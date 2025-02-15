import { Toaster } from "react-hot-toast";
import AppRouter from "./router";
import DebugLogger from "./components/DebugLogger"; // Подключаем DebugLogger

const App = () => {
  console.log("🛠 App загружен");

  return (
    <>
      <Toaster position="top-center" />
      <AppRouter />
      <DebugLogger /> {/* Логгер появляется только в DEBUG_MODE */}
    </>
  );
};

export default App;
