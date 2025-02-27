import React from "react";
import { Switch } from "antd";

/**
 * AutoExtractSwitch renders a disabled switch that is always off.
 */
const AutoExtractSwitch: React.FC = () => (
  <div className="template-uploader__field">
    <label className="template-uploader__label flex items-center gap-2" htmlFor="auto-extract">
      <Switch
        id="auto-extract"
        checked={false}
        disabled
        className="toggle"
        aria-label="Toggle auto-extract fields"
      />
      Автоизвлечение полей из шаблона
    </label>
  </div>
);

export default AutoExtractSwitch;
