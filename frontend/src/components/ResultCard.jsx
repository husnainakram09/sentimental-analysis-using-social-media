const toneMap = {
  negative: 'Negative',
  neutral: 'Neutral',
  positive: 'Positive',
}

export default function ResultCard({ result }) {
  return (
    <div className="rounded-3xl bg-white p-6 shadow-sm">
      <h2 className="text-lg font-semibold">Latest Result</h2>
      {!result ? (
        <p className="mt-3 text-sm text-slate-500">No prediction yet.</p>
      ) : (
        <div className="mt-4 space-y-3">
          <p className="text-sm text-slate-500">Original text</p>
          <div className="rounded-2xl bg-slate-50 p-4 text-sm">{result.text}</div>
          <div className="grid grid-cols-2 gap-3 text-sm">
            <div className="rounded-2xl border p-4">
              <div className="text-slate-500">Label</div>
              <div className="mt-1 text-xl font-semibold">{toneMap[result.label] || result.label}</div>
            </div>
            <div className="rounded-2xl border p-4">
              <div className="text-slate-500">Confidence</div>
              <div className="mt-1 text-xl font-semibold">{(result.confidence * 100).toFixed(2)}%</div>
            </div>
          </div>
          <div className="space-y-2 rounded-2xl border p-4 text-sm">
            <div>Negative: {(result.probabilities.negative * 100).toFixed(2)}%</div>
            <div>Neutral: {(result.probabilities.neutral * 100).toFixed(2)}%</div>
            <div>Positive: {(result.probabilities.positive * 100).toFixed(2)}%</div>
          </div>
        </div>
      )}
    </div>
  )
}
