"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Header } from "@/components/Header";
import { PromptInputCard } from "@/components/PromptInputCard";
import { ResultsPanel } from "@/components/ResultsPanel";
import { Toast } from "@/components/Toast";
import { evaluatePrompt } from "@/lib/api";
import { EvaluationResponse } from "@/types/evaluation";

const MAX_CHARS = 2000;

export default function HomePage() {
  const [prompt, setPrompt] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<EvaluationResponse | null>(null);
  const [toast, setToast] = useState("");

  const runEvaluation = async () => {
    if (!prompt.trim()) return;

    setIsLoading(true);
    try {
      const response = await evaluatePrompt(prompt);
      setResult(response);
      setToast("Prompt evaluated successfully.");
      setTimeout(() => setToast(""), 2200);
    } catch (error) {
      console.error(error);
      setToast("Evaluation failed. Please try again.");
      setTimeout(() => setToast(""), 2200);
    } finally {
      setIsLoading(false);
    }
  };

  const copyImprovedPrompt = async () => {
    if (!result?.improved_prompt) return;
    await navigator.clipboard.writeText(result.improved_prompt);
    setToast("Improved prompt copied.");
    setTimeout(() => setToast(""), 2200);
  };

  return (
    <main className="relative min-h-screen px-4 py-10 md:px-8 md:py-12">
      <div className="mx-auto max-w-6xl space-y-8">
        <Header />

        {/* 1. Added relative positioning and a z-index to keep this ABOVE the results */}
        <section className="relative z-20">
          <PromptInputCard
            prompt={prompt}
            maxChars={MAX_CHARS}
            isLoading={isLoading}
            onChange={setPrompt}
            onEvaluate={runEvaluation}
          />
        </section>

        {/* 2. Ensured the results panel sits on a lower z-index layer */}
        <section className="relative z-10">
          {result ? (
            <ResultsPanel data={result} onCopy={copyImprovedPrompt} />
          ) : (
            <motion.section
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex min-h-[24rem] items-center justify-center rounded-3xl border border-dashed border-zinc-300 bg-white/70 p-8 text-center text-slate-500 shadow-sm shadow-zinc-200/70 backdrop-blur-xl"
            >
              <p className="max-w-md text-sm leading-relaxed md:text-base">
                Your prompt evaluation results will appear here after you click &quot;Evaluate Prompt&quot;.
              </p>
            </motion.section>
          )}
        </section>
      </div>
      {toast ? <Toast message={toast} /> : null}
    </main>
  );
}
