import { useEffect, useState } from "react";
import { checkTemplatesStatus } from "../api";
import StatusDisplay from "../components/StatusDisplay";

const CheckStatus = () => {
  const [status, setStatus] = useState("");

  useEffect(() => {
    checkTemplatesStatus()
      .then((data) => {
        if (data && typeof data === "object" && "message" in data) {
          setStatus(data.message);
        } else {
          setStatus("Неизвестный статус");
        }
      })
      .catch((error) => {
        console.error("❌ Ошибка:", error);
        setStatus("Ошибка при получении статуса");
      });
  }, []);
  

  return (
    <div className="container mx-auto p-6">
      <h1>📊 Статус шаблонов</h1>
      <StatusDisplay status={status} />
    </div>
  );
};

export default CheckStatus;
