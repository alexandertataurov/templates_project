// useDebouncedValue.ts
import { useState, useEffect } from "react";
import debounce from "lodash/debounce";

export function useDebouncedValue<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = debounce(() => setDebouncedValue(value), delay);
    handler();
    return () => {
      handler.cancel();
    };
  }, [value, delay]);

  return debouncedValue;
}
