import React, { ErrorInfo, ReactNode } from "react";
import { toast } from "react-toastify";

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
}

class ErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  // Переименовываем параметр, чтобы TS понял, что он намеренно не используется
  static getDerivedStateFromError(_error: Error): State {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Ошибка в компоненте:", error, errorInfo);
    toast.error("Произошла непредвиденная ошибка");
  }

  render() {
    if (this.state.hasError) {
      return <h2>Что-то пошло не так.</h2>;
    }
    return this.props.children;
  }
}

export default ErrorBoundary;
