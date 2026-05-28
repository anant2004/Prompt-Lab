import { EvaluationResponse } from "@/types/evaluation";
import { ScoreBar } from "./ScoreBar";
import { motion } from "framer-motion";

interface ResultsPanelProps {
  data: EvaluationResponse;
  onCopy: () => void;
}

function ListBlock({ title, items }: { title: string; items: string[] }) {
  return (
    <motion.div
      whileHover={{ y: -3 }}
      transition={{ type: "spring", stiffness: 320, damping: 24 }}
      className="rounded-3xl border border-zinc-200 bg-white/80 p-6 shadow-sm shadow-zinc-200/70 backdrop-blur"
    >
      <h3 className="mb-4 text-lg md:text-xl font-semibold text-slate-900">{title}</h3>
      <ul className="space-y-3 text-sm text-slate-600">
        {items.map((item, index) => (
          <li key={`${title}-${index}`} className="rounded-xl border border-zinc-200 bg-zinc-50/80 p-3 leading-relaxed">
            {item}
          </li>
        ))}
      </ul>
    </motion.div>
  );
}

export function ResultsPanel({ data, onCopy }: ResultsPanelProps) {
  return (
    <motion.section
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.45, ease: "easeOut" }}
      className="space-y-8"
    >
      <motion.div
        whileHover={{ y: -3 }}
        transition={{ type: "spring", stiffness: 300, damping: 24 }}
        className="overflow-x-auto rounded-3xl border border-blue-200 bg-gradient-to-r from-blue-50 via-sky-50 to-cyan-50 p-6 shadow-md shadow-blue-100/70 backdrop-blur"
      >
        <div className="flex min-w-[980px] w-full items-center justify-between gap-3">
          <div className="flex min-w-[220px] flex-col justify-center pr-2">
            <p className="text-lg font-medium text-blue-700">Overall Prompt Quality</p>
            <div className="mt-2 flex items-end gap-1">
              <span className="text-7xl font-semibold leading-none tracking-tight text-slate-900">{data.overall_score}</span>
              <span className="pb-1 text-4xl font-medium leading-none text-slate-400">/100</span>
            </div>
          </div>

          <ScoreBar label="Clarity" score={data.scores.clarity} />
          <ScoreBar label="Context" score={data.scores.context} />
          <ScoreBar label="Specificity" score={data.scores.specificity} />
          <ScoreBar label="Structure" score={data.scores.structure} />
          <ScoreBar label="Professional Tone" score={data.scores.tone} />
        </div>
      </motion.div>

      <div className="grid gap-6 xl:grid-cols-3">
        <ListBlock title="Strengths" items={data.strengths} />
        <ListBlock title="Weaknesses" items={data.weaknesses} />
        <ListBlock title="AI Suggestions" items={data.suggestions} />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 14 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
        className="relative overflow-hidden rounded-3xl border border-blue-200 bg-gradient-to-b from-white via-zinc-50 to-slate-100/60 p-6 shadow-md shadow-blue-100/70"
      >
        <div className="pointer-events-none absolute -right-10 -top-10 h-36 w-36 rounded-full bg-blue-200/60 blur-3xl" />
        <div className="pointer-events-none absolute -bottom-10 -left-10 h-36 w-36 rounded-full bg-sky-200/60 blur-3xl" />

        <div className="relative mb-4 flex flex-wrap items-center justify-between gap-3">
          <h3 className="text-lg font-semibold text-slate-900">Improved Prompt</h3>
          <button
            onClick={onCopy}
            className="sticky top-3 rounded-xl border border-blue-200 bg-blue-50 px-3 py-1.5 text-xs font-medium text-blue-700 transition duration-300 hover:bg-blue-100"
          >
            Copy improved prompt
          </button>
        </div>
        <pre className="relative whitespace-pre-wrap rounded-2xl border border-zinc-200 bg-white/90 p-5 font-mono text-sm leading-relaxed text-slate-700 shadow-inner shadow-zinc-100">
          {data.improved_prompt}
        </pre>
      </motion.div>
    </motion.section>
  );
}
