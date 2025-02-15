module.exports = {
    env: {
      browser: true,
      es2021: true,
    },
    extends: [
      "eslint:recommended",
      "plugin:react/recommended",
      "plugin:jsx-a11y/recommended",
      "plugin:import/errors",
      "plugin:import/warnings",
      "plugin:react-hooks/recommended",
      "plugin:prettier/recommended",
      "plugin:storybook/recommended"
    ],
    parserOptions: {
      ecmaFeatures: { jsx: true },
      ecmaVersion: 12,
      sourceType: "module",
    },
    plugins: ["react", "jsx-a11y", "import", "prettier"],
    rules: {
      "prettier/prettier": ["error"],
      "react/react-in-jsx-scope": "off",
      "no-console": "warn",
      "import/order": ["error", { "groups": ["builtin", "external", "internal"] }]
    },
  };
  