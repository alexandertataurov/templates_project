import React from "react";
import ReactDOM from "react-dom/client";
import { QueryClient, QueryClientProvider, QueryCache } from "@tanstack/react-query";
import App from "./App";
import "./index.css";

const queryClient = new QueryClient({
  queryCache: new QueryCache({
    onError: (error) => {
      console.error("❌ React Query Error:", error);
    },
  }),
});

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </React.StrictMode>
);
