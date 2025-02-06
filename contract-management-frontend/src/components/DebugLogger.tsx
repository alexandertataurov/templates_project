import { useEffect, useState, useCallback, useRef } from "react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { dracula } from "react-syntax-highlighter/dist/esm/styles/prism";

const DebugLogger = () => {
  const [logs, setLogs] = useState<string[]>([]);
  const [collapsed, setCollapsed] = useState(false);
  const [debugEnabled, setDebugEnabled] = useState<boolean>(
    localStorage.getItem("debug_mode") === "on"
  );
  const [height, setHeight] = useState(250); // Начальная высота терминала
  const resizeRef = useRef<HTMLDivElement>(null);
  const isResizing = useRef(false);

  useEffect(() => {
    if (!debugEnabled) return;

    const originalLog = console.log;
    const originalWarn = console.warn;
    const originalError = console.error;

    const logBuffer: string[] = [];

    const logHandler = (type: string, args: any[]) => {
      const formattedArgs = args.map((a) =>
        typeof a === "object" ? JSON.stringify(a, null, 2) : a
      );

      const message = `[${new Date().toLocaleTimeString()}] ${type}: ${formattedArgs.join(" ")}`;
      logBuffer.unshift(message);
    };

    console.log = (...args) => {
      logHandler("🟢 LOG", args);
      originalLog(...args);
    };
    console.warn = (...args) => {
      logHandler("🟡 WARN", args);
      originalWarn(...args);
    };
    console.error = (...args) => {
      logHandler("🔴 ERROR", args);
      originalError(...args);
    };

    const flushLogs = () => {
      if (logBuffer.length > 0) {
        setLogs((prevLogs) => [...logBuffer, ...prevLogs].slice(0, 100)); // Ограничение в 100 сообщений
        logBuffer.length = 0;
      }
    };

    const interval = setInterval(flushLogs, 500);

    return () => {
      console.log = originalLog;
      console.warn = originalWarn;
      console.error = originalError;
      clearInterval(interval);
    };
  }, [debugEnabled]);

  // 🔥 Копирование всех логов
  const copyLogsToClipboard = useCallback(() => {
    const textToCopy = logs.join("\n");
    navigator.clipboard
      .writeText(textToCopy)
      .then(() => console.log("✅ Логи скопированы в буфер обмена!"))
      .catch((err) => console.error("❌ Ошибка копирования логов:", err));
  }, [logs]);

  // 🔥 Копирование конкретного лога
  const copySingleLog = (log: string) => {
    navigator.clipboard
      .writeText(log)
      .then(() => console.log("✅ Лог скопирован!"))
      .catch((err) => console.error("❌ Ошибка копирования:", err));
  };

  // 🔥 Переключение `DEBUG_MODE`
  const toggleDebugMode = () => {
    const newState = !debugEnabled;
    setDebugEnabled(newState);
    localStorage.setItem("debug_mode", newState ? "on" : "off");
    console.log(newState ? "🛠 Debug Mode Включен" : "🛠 Debug Mode Выключен");
  };

  // 🔥 Обработчик начала изменения размера
  const startResizing = () => {
    isResizing.current = true;
    document.addEventListener("mousemove", handleResizing);
    document.addEventListener("mouseup", stopResizing);
  };
  
  // 🔥 Обработчик изменения размера
  const handleResizing = (event: MouseEvent) => {
    if (!isResizing.current) return;
    const newHeight = Math.max(100, window.innerHeight - event.clientY);
    setHeight(newHeight);
  };

  // 🔥 Обработчик завершения изменения размера
  const stopResizing = () => {
    isResizing.current = false;
    document.removeEventListener("mousemove", handleResizing);
    document.removeEventListener("mouseup", stopResizing);
  };

  return (
    <>
      {/* Кнопка включения/выключения DEBUG_MODE */}
      <div className="fixed bottom-16 right-4 z-50">
        <button
          onClick={toggleDebugMode}
          className={`px-4 py-2 rounded text-white ${
            debugEnabled ? "bg-red-600 hover:bg-red-700" : "bg-green-600 hover:bg-green-700"
          }`}
        >
          {debugEnabled ? "🛑 Выключить DEBUG" : "🟢 Включить DEBUG"}
        </button>
      </div>

      {/* Debug Console */}
      {debugEnabled && (
        <div
          className="fixed bottom-0 left-0 right-0 bg-black text-xs font-mono border-t border-gray-700 shadow-lg z-50 transition-all"
          style={{ height: collapsed ? "40px" : `${height}px` }}
        >
          {/* Верхняя панель */}
          <div className="flex justify-between items-center px-4 py-2 bg-gray-900 text-white">
            <span
              className="font-bold cursor-pointer"
              onClick={() => setCollapsed(!collapsed)}
            >
              🛠 Debug Terminal {collapsed ? "🔽" : "🔼"}
            </span>
            <span
              onClick={copyLogsToClipboard}
              className="text-gray-400 cursor-pointer hover:text-gray-300 text-m"
            >
              📋 Копировать логи
            </span>
          </div>

          {/* Полоса для изменения размера */}
          <div
            ref={resizeRef}
            className="w-full h-2 cursor-ns-resize bg-gray-800 hover:bg-gray-600"
            onMouseDown={startResizing}
          />

          {/* Логи */}
          {!collapsed && (
            <div className="max-h-full overflow-y-auto p-2 custom-scrollbar">
              {logs.map((log, i) => (
                <div key={i} onClick={() => copySingleLog(log)} className="cursor-pointer">
                  <SyntaxHighlighter
                    language="json"
                    style={dracula}
                    customStyle={{
                      background: "transparent",
                      fontSize: "12px",
                      padding: "4px",
                      borderRadius: "4px",
                    }}
                    wrapLongLines
                  >
                    {log}
                  </SyntaxHighlighter>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </>
  );
};

export default DebugLogger;
