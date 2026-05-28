interface ToastProps {
  message: string;
}

export function Toast({ message }: ToastProps) {
  return (
    <div className="fixed bottom-5 right-5 z-50 rounded-xl border border-emerald-200 bg-emerald-50/90 px-4 py-2 text-sm text-emerald-700 shadow-md shadow-emerald-100 backdrop-blur-xl">
      {message}
    </div>
  );
}
