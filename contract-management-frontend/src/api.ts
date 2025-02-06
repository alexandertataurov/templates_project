const API_URL = "http://localhost:8000/templates"; // 🔥 Убедись, что тут правильный URL
const DEBUG_MODE = import.meta.env.VITE_DEBUG_MODE === "on"; // Читаем DEBUG_MODE

// 🛠️ Логгер API-запросов
const apiLogger = async (method: string, url: string, body?: any) => {
  console.log(`📡 [API] ${method.toUpperCase()} ${url}`);
  if (body instanceof FormData) {
    console.log("📤 Отправленные FormData данные:");
    for (let [key, value] of body.entries()) {
      console.log(`  🔹 ${key}: ${value}`);
    }
  } else if (body) {
    console.log("📤 Отправленные JSON данные:", JSON.stringify(body, null, 2));
  }

  const options: RequestInit = { method };
  if (body) {
    options.body = body instanceof FormData ? body : JSON.stringify(body);
    if (!(body instanceof FormData)) {
      options.headers = { "Content-Type": "application/json" };
    }
  }

  try {
    const response = await fetch(url, options);
    const status = response.status;
    console.log(`📥 [API] Ответ ${status} ${response.statusText}`);

    // 🔴 Обрабатываем ошибки HTTP (404, 500 и т.д.)
    if (!response.ok) {
      if (status === 401) throw new Error("🚫 Ошибка 401: Не авторизован");
      if (status === 403) throw new Error("⛔ Ошибка 403: Доступ запрещён");
      if (status === 404) throw new Error("❌ Ошибка 404: Ресурс не найден");
      if (status === 500) throw new Error("💥 Ошибка 500: Ошибка сервера");
      throw new Error(`⚠️ Неизвестная ошибка ${status}: ${response.statusText}`);
    }

    const text = await response.text();
    try {
      const json = JSON.parse(text);
      console.log("✅ [API] Ответ JSON:", json);
      return json;
    } catch (error) {
      console.error("❌ [API ERROR] Сервер вернул не JSON:", text);
      throw new Error("Ошибка: API вернул HTML вместо JSON");
    }
  } catch (error) {
    console.error("❌ [API ERROR] Ошибка запроса:", error);
    throw error;
  }
};

// 1️⃣ Проверка статуса загрузки шаблонов
export interface TemplateStatusResponse {
  status: string;
  message: string;
}

export const checkTemplatesStatus = async (): Promise<TemplateStatusResponse> => {
  try {
    const response = await fetch("YOUR_API_ENDPOINT");
    const data: TemplateStatusResponse = await response.json();
    return data; 
  } catch (error) {
    console.error("API error:", error);
    return { status: "error", message: "Ошибка при получении статуса" };
  }
};

// 2️⃣ Запуск процесса создания шаблонов
export const startTemplateSetup = async (): Promise<any> =>
  apiLogger("POST", `${API_URL}/start-setup`);

// 3️⃣ Определение динамических полей
export const defineFields = async (fields: string[]): Promise<any> =>
  apiLogger("POST", `${API_URL}/define-fields`, { fields });

// 4️⃣ Получение списка динамических полей (для инструкции)
export const getInstructionFields = async (): Promise<string[]> =>
  apiLogger("GET", `${API_URL}/instruction`);

// 5️⃣ Загрузка нового шаблона
export const uploadTemplate = async (file: File, templateType: string, displayName: string): Promise<any> => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("template_type", templateType);
  formData.append("display_name", displayName);
  return apiLogger("POST", `${API_URL}/upload`, formData);
};

// 6️⃣ Обновление шаблона
export const updateTemplate = async (templateId: number, displayName: string, fields: string[]): Promise<any> => {
  const formData = new FormData();
  formData.append("template_id", templateId.toString());
  formData.append("display_name", displayName);
  formData.append("fields", JSON.stringify(fields));
  return apiLogger("POST", `${API_URL}/update`, formData);
};

// 7️⃣ Удаление шаблона
export const deleteTemplate = async (templateType: string, displayName: string): Promise<any> => {
  const formData = new FormData();
  formData.append("template_type", templateType);
  formData.append("display_name", displayName);

  if (DEBUG_MODE) console.log("📤 [API] Отправка DELETE запроса с данными:", {
    template_type: templateType,
    display_name: displayName
  });

  return apiLogger("POST", `${API_URL}/delete`, formData);
};


// 8️⃣ Получение списка шаблонов
export const getTemplates = async (): Promise<any[]> =>
  apiLogger("GET", `${API_URL}/`);
