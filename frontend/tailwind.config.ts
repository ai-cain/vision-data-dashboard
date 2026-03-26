import type { Config } from "tailwindcss";
import animate from "tailwindcss-animate";

const config: Config = {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        sand: "#f6efe6",
        paper: "#fffaf3",
        ink: "#112328",
        panel: "#1a2d33",
        fog: "#d7cfc4",
        ember: "#db6d34",
        teal: "#127c73",
        lemon: "#f4c95d",
        danger: "#b53f2f",
      },
      fontFamily: {
        display: ['"Space Grotesk"', "sans-serif"],
        mono: ['"IBM Plex Mono"', "monospace"],
      },
      boxShadow: {
        panel: "0 18px 60px rgba(17, 35, 40, 0.12)",
      },
      backgroundImage: {
        grid: "linear-gradient(rgba(17,35,40,0.06) 1px, transparent 1px), linear-gradient(90deg, rgba(17,35,40,0.06) 1px, transparent 1px)",
      },
    },
  },
  plugins: [animate],
};

export default config;
