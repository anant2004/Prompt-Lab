"use client";

import { motion } from "framer-motion";

interface PromptInputCardProps {
  prompt: string;
  maxChars: number;
  isLoading: boolean;
  onChange: (value: string) => void;
  onEvaluate: () => void;
}

export function PromptInputCard({
  prompt,
  maxChars,
  isLoading,
  onChange,
  onEvaluate
}: PromptInputCardProps) {
  return (
    <motion.section
      initial={{ opacity: 0, y: 18 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.45, ease: "easeOut" }}
      className="h-fit rounded-3xl border border-zinc-200 bg-white/80 p-6 shadow-md shadow-zinc-200/60 backdrop-blur-xl md:sticky md:top-8 md:p-7"
    >
      <div className="mb-3 flex items-center justify-between">
        <h2 className="text-lg font-semibold text-slate-900 md:text-xl">Prompt Input</h2>
        <span className="text-xs font-medium text-slate-500">
          {prompt.length}/{maxChars}
        </span>
      </div>

      <textarea
        value={prompt}
        onChange={(event) => onChange(event.target.value.slice(0, maxChars))}
        placeholder="Example: You are a senior strategy consultant. Create a 1-page commercial launch plan for a steel manufacturing business unit targeting automotive and construction clients. Include assumptions, rollout timeline, and KPIs in a markdown table."
        className="h-44 w-full resize-none rounded-2xl border border-zinc-200 bg-white p-4 text-sm leading-relaxed text-slate-800 outline-none transition duration-300 placeholder:text-slate-400 focus:border-blue-400 focus:ring-2 focus:ring-blue-400/25"
      />

      <button
        onClick={onEvaluate}
        disabled={isLoading || !prompt.trim()}
        className="group mt-5 inline-flex items-center justify-center rounded-2xl border border-white/10 bg-gradient-to-r from-blue-600 via-blue-500 to-sky-500 px-6 py-3 text-sm font-semibold text-white shadow-[0_4px_20px_-2px_rgba(37,99,235,0.35)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_8px_25px_-2px_rgba(37,99,235,0.45)] hover:brightness-105 active:scale-[0.98] disabled:pointer-events-none disabled:opacity-50"
      >
        {isLoading ? (
          <span className="flex items-center gap-2">
            <svg className="h-4 w-4 animate-spin text-white" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            Evaluating...
          </span>
        ) : (
          "Evaluate Prompt"
        )}
      </button>
    </motion.section>
  );
}
