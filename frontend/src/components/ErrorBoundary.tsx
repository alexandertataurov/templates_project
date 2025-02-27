import React, { ErrorInfo, ReactNode } from "react";
import { toast } from "react-toastify";
// Optional: Integrate Sentry for centralized error logging
import * as Sentry from "@sentry/react";

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
}

/**
 * ErrorBoundary catches errors from its child component tree, logs them,
 * and displays a fallback UI.
 */
class ErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(_error: Error): State {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Ошибка в компоненте:", error, errorInfo);
    // Log the error to Sentry (or any logging service)
    Sentry.captureException(error);
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
