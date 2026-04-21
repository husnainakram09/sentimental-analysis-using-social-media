export default function StatsCards({ stats }) {
  const items = [
    ['Total Predictions', stats?.total_predictions ?? 0],
    ['Negative', stats?.negative ?? 0],
    ['Neutral', stats?.neutral ?? 0],
    ['Positive', stats?.positive ?? 0],
  ]

  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-4">
      {items.map(([label, value]) => (
        <div key={label} className="rounded-3xl bg-white p-5 shadow-sm">
          <div className="text-sm text-slate-500">{label}</div>
          <div className="mt-2 text-3xl font-bold">{value}</div>
        </div>
      ))}
    </div>
  )
}
