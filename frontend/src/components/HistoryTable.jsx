export default function HistoryTable({ history }) {
  return (
    <div className="rounded-3xl bg-white p-6 shadow-sm">
      <h2 className="text-lg font-semibold">Recent Predictions</h2>
      <div className="mt-4 overflow-x-auto">
        <table className="min-w-full text-left text-sm">
          <thead>
            <tr className="border-b border-slate-200 text-slate-500">
              <th className="py-3 pr-4">Text</th>
              <th className="py-3 pr-4">Label</th>
              <th className="py-3 pr-4">Confidence</th>
              <th className="py-3 pr-4">Time</th>
            </tr>
          </thead>
          <tbody>
            {history.map((item, index) => (
              <tr key={`${item.created_at}-${index}`} className="border-b border-slate-100 align-top">
                <td className="py-3 pr-4">{item.text}</td>
                <td className="py-3 pr-4">{item.label}</td>
                <td className="py-3 pr-4">{(item.confidence * 100).toFixed(2)}%</td>
                <td className="py-3 pr-4">{item.created_at ? new Date(item.created_at).toLocaleString() : '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
