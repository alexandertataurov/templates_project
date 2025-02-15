import Widget from "../components/Widget";
import LogsWidget from "../components/LogsWidget";
import { getServerHealth, getApiStats, getDbStatus, getTaskStatus, getServerConfig } from "../api";

const Dashboard = () => {
  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6 text-center text-gray-800">📊 Панель управления</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <LogsWidget />
        <Widget title="🔋 Статус сервера" fetchData={getServerHealth} />
        <Widget title="📊 Статистика API" fetchData={getApiStats} />
        <Widget title="🛢 Статус базы данных" fetchData={getDbStatus} />
        <Widget title="⚙️ Фоновые задачи" fetchData={getTaskStatus} />
        <Widget title="⚙️ Конфигурация сервера" fetchData={getServerConfig} />
      </div>
    </div>
  );
};

export default Dashboard;
