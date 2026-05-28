import { motion } from "framer-motion";

interface ScoreBarProps {
  label: string;
  score: number;
}

export function ScoreBar({ label, score }: ScoreBarProps) {
  const clampedScore = Math.max(0, Math.min(100, score));
  const radius = 34;
  const strokeWidth = 8;
  const normalizedRadius = radius - strokeWidth / 2;
  const circumference = 2 * Math.PI * normalizedRadius;
  const dashOffset = circumference - (clampedScore / 100) * circumference;
  const gradientId = `score-gradient-${label.toLowerCase().replace(/\s+/g, "-")}`;

  return (
    <motion.div
      whileHover={{ y: -3 }}
      transition={{ type: "spring", stiffness: 320, damping: 24 }}
      className="flex w-[140px] flex-col items-center justify-center px-2 py-1"
    >
      <div className="relative h-28 w-28">
        <svg className="h-full w-full -rotate-90" viewBox={`0 0 ${radius * 2} ${radius * 2}`} fill="none">
          <defs>
            <linearGradient id={gradientId} x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#2563eb" />
              <stop offset="50%" stopColor="#38bdf8" />
              <stop offset="100%" stopColor="#06b6d4" />
            </linearGradient>
          </defs>
          <circle
            cx={radius}
            cy={radius}
            r={normalizedRadius}
            stroke="#e4e4e7"
            strokeWidth={strokeWidth}
            className="opacity-95"
          />
          <motion.circle
            cx={radius}
            cy={radius}
            r={normalizedRadius}
            stroke={`url(#${gradientId})`}
            strokeWidth={strokeWidth}
            strokeLinecap="round"
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset: dashOffset }}
            transition={{ duration: 0.9, ease: "easeOut" }}
          />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-[38px] font-semibold leading-none text-slate-800">{score}</span>
        </div>
      </div>
      <p className="mt-3 text-center text-base font-medium text-slate-700">{label}</p>
    </motion.div>
  );
}
