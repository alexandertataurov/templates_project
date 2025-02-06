const DEBUG_MODE = import.meta.env.VITE_DEBUG_MODE === "on";

const WizardStep = ({ step, children }: { step: number; children: React.ReactNode }) => {
  if (DEBUG_MODE) console.log(`🔹 [WIZARD] Отображение шага ${step}`);

  return (
    <div className="p-6 bg-white rounded-lg shadow-lg w-96">
      <h1 className="text-xl font-bold">🔹 Шаг {step}</h1>
      {children}
    </div>
  );
};

export default WizardStep;
