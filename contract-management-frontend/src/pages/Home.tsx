import { useState, useEffect, useCallback } from "react";
import { getTemplates, deleteTemplate } from "../api";
import TemplateList from "../components/TemplateList";
import Toast, { notifySuccess, notifyError } from "../components/ToastProvider";

const DEBUG_MODE = import.meta.env.VITE_DEBUG_MODE === "on"; // Читаем DEBUG_MODE

const Home = () => {
  const [templates, setTemplates] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // 🚀 Загружаем шаблоны при загрузке страницы
  useEffect(() => {
    const fetchTemplates = async () => {
      try {
        if (DEBUG_MODE) console.log("📡 [API] Запрос списка шаблонов...");
        const data = await getTemplates();
        setTemplates(data);
        notifySuccess("📋 Шаблоны загружены успешно");
        if (DEBUG_MODE) console.log("✅ [API] Полученные шаблоны:", data);
      } catch (err: any) {
        setError("Ошибка загрузки данных");
        notifyError(`❌ Ошибка загрузки шаблонов: ${err.message}`);
        console.error("❌ [API ERROR] Ошибка загрузки шаблонов:", err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchTemplates();
  }, []);

  // 🚀 Обновленный `handleDelete` с API response code и `toast`
  const handleDelete = useCallback(async (id: number) => {
    try {
      if (DEBUG_MODE) console.log("🗑 [API] Удаление шаблона:", id);
  
      // ✅ Проверяем, есть ли такой шаблон в списке
      const template = templates.find((t) => t.id === id);
      if (!template) {
        notifyError("❌ Шаблон не найден!");
        console.error("❌ [API ERROR] Шаблон не найден!");
        return;
      }
  
      // ✅ Проверяем, что у шаблона есть `type` и `display_name`
      if (!template.type || !template.display_name) {
        notifyError("⚠️ Ошибка: отсутствуют данные `type` или `display_name`.");
        console.error("⚠️ [API ERROR] Нет `type` или `display_name` у шаблона:", template);
        return;
      }
  
      console.log("📤 [API] Перед удалением шаблона проверяем данные:", template);
  
      // ✅ Вызываем API для удаления
      await deleteTemplate(template.type, template.display_name);
  
      // ✅ Обновляем UI после успешного удаления
      setTemplates((prev) => prev.filter((t) => t.id !== id));
      notifySuccess(`🗑 Шаблон "${template.display_name}" удалён`);
      if (DEBUG_MODE) console.log("✅ [API] Шаблон удалён:", template);
    } catch (err: any) {
      notifyError(`❌ Ошибка удаления шаблона: ${err.message}`);
      console.error("❌ [API ERROR] Ошибка удаления:", err);
    }
  }, [templates]);
  

  if (isLoading) return <p className="text-center">⏳ Загрузка...</p>;
  if (error) return <p className="text-center text-red-500">❌ {error}</p>;

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-2xl font-bold">📋 Список шаблонов</h1>
      <TemplateList templates={templates} onDelete={handleDelete} />
      <Toast /> {/* 🔥 Включаем ToastContainer для уведомлений */}
    </div>
  );
};

export default Home;
