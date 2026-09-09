import eslint from "@eslint/js";
import globals from "globals";
import tseslint from "typescript-eslint";


export default tseslint.config(
  {
    ignores: [
      "dist/**",
      "node_modules/**",
    ],
  },
  eslint.configs.recommended,
  ...tseslint.configs.recommended,
  {
    files: [
      "src/**/*.ts",
      "tests/**/*.ts",
    ],
    languageOptions: {
      globals: {
        ...globals.node,
      },
    },
    rules: {
      "@typescript-eslint/consistent-type-imports": [
        "error",
        {
          prefer: "type-imports",
        },
      ],
      "@typescript-eslint/no-explicit-any": "error",
    },
  },
);