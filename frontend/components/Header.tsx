export function Header() {
  return (
    <header className="mb-10 space-y-4 md:mb-12">
      <div className="inline-flex items-center rounded-full border border-blue-200/80 bg-blue-50/80 px-4 py-1.5 text-xs font-medium tracking-wide text-blue-700 backdrop-blur">
        AI Prompt Engineering Workshop Tool
      </div>
      <h1 className="text-5xl font-semibold tracking-tight text-slate-900 md:text-6xl">Prompt Lab</h1>
      <p className="max-w-2xl text-base leading-relaxed text-slate-600 md:text-lg">
        Evaluate prompt quality, understand strengths and weaknesses, and get an improved prompt ready for real-world use.
      </p>
    </header>
  );
}
