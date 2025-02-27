import { useState, useEffect, useCallback } from "react";
import { listTemplates, Template } from "../api/templates";

const useTemplates = () => {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const fetchTemplates = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await listTemplates();
      data.sort((a: Template, b: Template) => a.id - b.id);
      setTemplates(data);
    } catch (err) {
      setError("Ошибка загрузки шаблонов");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTemplates();
  }, [fetchTemplates]);

  return { templates, loading, error, fetchTemplates };
};

export default useTemplates;
