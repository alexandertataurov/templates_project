import { useEffect, useState, useCallback, useRef, useMemo } from "react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { dracula } from "react-syntax-highlighter/dist/esm/styles/prism";
import { XMarkIcon, ClipboardIcon, TrashIcon, ChevronUpIcon, ChevronDownIcon } from "@heroicons/react/24/outline";

const DebugLogger = () => {
  const [logs, setLogs] = useState<string[]>([]);
  const [collapsed, setCollapsed] = useState(false);
  const [debugEnabled, setDebugEnabled] = useState<boolean>(
    localStorage.getItem("debug_mode") === "on"
  );
  const [height, setHeight] = useState(200);
  const [filter, setFilter] = useState<string>("");
  const logContainerRef = useRef<HTMLDivElement>(null);
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
        setLogs((prevLogs) => [...logBuffer, ...prevLogs].slice(0, 100));
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

  useEffect(() => {
    if (logContainerRef.current) {
      logContainerRef.current.scrollTop = 0; // 🔥 Автопрокрутка наверх всегда
    }
  }, [logs]);

  const copyLogsToClipboard = useCallback((e: React.MouseEvent) => {
    e.stopPropagation();
    navigator.clipboard
      .writeText(logs.join("\n"))
      .then(() => console.log("✅ Логи скопированы!"))
      .catch((err) => console.error("❌ Ошибка копирования:", err));
  }, [logs]);

  const copySingleLog = useCallback((log: string) => {
    navigator.clipboard
      .writeText(log)
      .then(() => console.log("✅ Лог скопирован!"))
      .catch((err) => console.error("❌ Ошибка копирования:", err));
  }, []);

  const toggleDebugMode = () => {
    const newState = !debugEnabled;
    setDebugEnabled(newState);
    localStorage.setItem("debug_mode", newState ? "on" : "off");
  };

  const clearLogs = (e: React.MouseEvent) => {
    e.stopPropagation();
    setLogs([]);
  };

  const startResizing = (e: React.MouseEvent) => {
    e.preventDefault();
    isResizing.current = true;
    document.addEventListener("mousemove", handleResizing);
    document.addEventListener("mouseup", stopResizing);
  };

  const handleResizing = (event: MouseEvent) => {
    if (!isResizing.current) return;
    const newHeight = Math.max(100, window.innerHeight - event.clientY);
    setHeight(newHeight);
  };

  const stopResizing = () => {
    isResizing.current = false;
    document.removeEventListener("mousemove", handleResizing);
    document.removeEventListener("mouseup", stopResizing);
  };

  const filteredLogs = useMemo(
    () => logs.filter((log) => log.toLowerCase().includes(filter.toLowerCase())),
    [logs, filter]
  );

  return (
    <>
      {/* Кнопка включения/выключения DEBUG */}
      <div className="fixed top-20 right-4 z-50">
        {debugEnabled ? (
          <button onClick={toggleDebugMode} className="bg-red-600 text-white p-2 rounded-full hover:bg-red-700 transition">
            <XMarkIcon className="w-5 h-5" /> 
          </button>
        ) : (
          <button onClick={toggleDebugMode} className="bg-green-600 text-white p-2 rounded-full hover:bg-green-700 transition">
            🟢
          </button>
        )}
      </div>

      {debugEnabled && (
        <div className="fixed bottom-0 left-0 right-0 bg-black text-xs font-mono border-t border-gray-700 shadow-lg transition-all"
             style={{ height: collapsed ? "40px" : `${height}px` }}>
          
          {/* Заголовок терминала */}
          <div className="flex justify-between items-center px-4 py-2 bg-gray-900 text-white select-none">
            <span className="font-bold flex items-center gap-3 cursor-pointer" onClick={() => setCollapsed(!collapsed)}>
              {collapsed ? <ChevronUpIcon className="w-4 h-4" /> : <ChevronDownIcon className="w-4 h-4" />}
              Debug Terminal
            </span>

            {/* Кнопки управления */}
            <div className="flex gap-2">
              <input
                type="text"
                className="bg-gray-800 text-white px-2 py-1 rounded-md text-xs placeholder-gray-400 outline-none border border-gray-700 focus:border-gray-500"
                placeholder="🔍 Фильтр..."
                value={filter}
                onChange={(e) => setFilter(e.target.value)}
                onClick={(e) => e.stopPropagation()}
              />
              <button onClick={clearLogs} className="text-gray-400 hover:text-white">
                <TrashIcon className="w-4 h-4" />
              </button>
              <button onClick={copyLogsToClipboard} className="text-gray-400 hover:text-white">
                <ClipboardIcon className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Полоса для изменения размера */}
          <div className="w-full h-2 bg-gray-800 cursor-ns-resize" onMouseDown={startResizing} />

          {/* Список логов */}
          {!collapsed && (
            <div ref={logContainerRef} className="overflow-y-auto p-2 h-full custom-scrollbar select-text">
              {filteredLogs.map((log, i) => (
                <div key={i} onClick={() => copySingleLog(log)} className="cursor-text hover:bg-gray-800 p-1 rounded-md">
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
