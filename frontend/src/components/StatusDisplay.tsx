const StatusDisplay = ({ status }: { status: string }) => (
    <div className="p-4 bg-white shadow-md rounded">
      <p>{status || "⏳ Загрузка..."}</p>
    </div>
  );
  
  export default StatusDisplay;
  