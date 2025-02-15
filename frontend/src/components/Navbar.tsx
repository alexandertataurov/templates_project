import { Link } from "react-router-dom";

const Navbar = () => {
  console.log("🛠 Навбар загружен");

  return (
    <nav className="bg-gray-900 text-white p-4 flex justify-between items-center shadow-lg">
      <div className="text-2xl font-bold">📂 Template Manager</div>
      <div className="flex gap-6">
        <Link to="/" className="hover:text-blue-400">🏠 Главная</Link>
        <Link to="/wizard" className="hover:text-green-400">➕ Добавить шаблон</Link>
        <Link to="/settings" className="hover:text-yellow-400">⚙️ Настройки</Link>
      </div>
    </nav>
  );
};

export default Navbar;
