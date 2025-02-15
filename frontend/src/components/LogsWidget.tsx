import React, { useEffect, useRef, useState } from "react";
import { getLogs } from "../api";
import { ChevronUpIcon, ChevronDownIcon } from "@heroicons/react/24/solid";

const logColors = {
  INFO: "text-blue-500",
  ERROR: "text-red-500",
  WARNING: "text-yellow-500",
};

const LogsWidget: React.FC = () => {
  const [logs, setLogs] = useState<string[]>([]);
  const [level, setLevel] = useState("INFO");
  const [error, setError] = useState<string | null>(null);
  const logsEndRef = useRef<HTMLDivElement>(null);
  const [collapsed, setCollapsed] = useState(false);

  const fetchLogs = async () => {
    try {
      const response = await getLogs(level);
      setLogs(response?.logs || []);
      setError(response?.logs?.length ? null : "⚠️ Нет логов");
    } catch {
      setError("❌ Ошибка загрузки логов");
    }
  };

  useEffect(() => {
    fetchLogs();
    const interval = setInterval(fetchLogs, 5000);
    return () => clearInterval(interval);
  }, [level]);

  return (
    <div className="bg-white text-gray-800 p-4 rounded-lg shadow-md border border-gray-300 col-span-3">
      <div className="flex justify-between items-center">
        <h2 className="text-lg font-semibold">📜 Логи сервера</h2>
        <button onClick={() => setCollapsed(!collapsed)} className="text-gray-600 hover:text-gray-900">
          {collapsed ? <ChevronDownIcon className="h-5 w-5" /> : <ChevronUpIcon className="h-5 w-5" />}
        </button>
      </div>

      {!collapsed && (
        <>
          <div className="flex justify-between mb-2">
            <select className="border p-2 rounded text-sm bg-gray-100" value={level} onChange={(e) => setLevel(e.target.value)}>
              {["INFO", "WARNING", "ERROR"].map((lvl) => (
                <option key={lvl} value={lvl}>
                  {lvl}
                </option>
              ))}
            </select>
          </div>

          <div className="bg-gray-100 p-3 rounded-md h-72 overflow-y-auto text-sm leading-relaxed custom-scrollbar">
            {error ? (
              <p className="text-red-500">{error}</p>
            ) : (
              <ul>
                {logs.map((log, index) => (
                  <li key={index} className={logColors[log.includes("ERROR") ? "ERROR" : log.includes("WARNING") ? "WARNING" : "INFO"]}>
                    {log}
                  </li>
                ))}
                <div ref={logsEndRef} />
              </ul>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default LogsWidget;
