import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}"
  ],
  theme: {
    extend: {
      colors: {
        panel: "#0b1020"
      },
      boxShadow: {
        glow: "0 8px 40px rgba(79, 70, 229, 0.25)"
      }
    }
  },
  plugins: []
};

export default config;
