import React, { useEffect, useState } from "react";
import { ChevronUpIcon, ChevronDownIcon } from "@heroicons/react/24/solid";

interface WidgetProps {
  title: string;
  fetchData: () => Promise<any>;
  refreshInterval?: number;
}

const Widget: React.FC<WidgetProps> = ({ title, fetchData, refreshInterval = 20000 }) => {
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [collapsed, setCollapsed] = useState(false);

  const loadData = async () => {
    setLoading(true);
    try {
      const response = await fetchData();
      setData(response);
      setError(response?.error || null);
    } catch {
      setError("Ошибка загрузки данных");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, refreshInterval);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-white text-gray-800 p-4 rounded-lg shadow-md border border-gray-300">
      <div className="flex justify-between items-center">
        <h2 className="text-lg font-semibold">{title}</h2>
        <button onClick={() => setCollapsed(!collapsed)} className="text-gray-600 hover:text-gray-900">
          {collapsed ? <ChevronDownIcon className="h-5 w-5" /> : <ChevronUpIcon className="h-5 w-5" />}
        </button>
      </div>

      {!collapsed && (
        <div className="transition-all duration-300 mt-2">
          {loading ? (
            <div className="animate-pulse space-y-2">
              <div className="h-4 bg-gray-300 rounded w-3/4"></div>
              <div className="h-4 bg-gray-300 rounded w-5/6"></div>
            </div>
          ) : error ? (
            <p className="text-red-500">⚠️ {error}</p>
          ) : (
            <ul className="text-sm bg-gray-100 p-2 rounded space-y-1">
              {Object.entries(data || {}).map(([key, value]) => (
                <li key={key} className="flex justify-between">
                  <span className="font-medium">{key}:</span>
                  <span className="text-gray-700">{typeof value === "object" ? JSON.stringify(value) : String(value)}</span>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
};

export default Widget;
