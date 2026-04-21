import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from 'recharts'

export default function SentimentChart({ stats }) {
  const data = [
    { name: 'Negative', value: stats?.negative ?? 0 },
    { name: 'Neutral', value: stats?.neutral ?? 0 },
    { name: 'Positive', value: stats?.positive ?? 0 },
  ]

  return (
    <div className="rounded-3xl bg-white p-6 shadow-sm">
      <h2 className="text-lg font-semibold">Sentiment Distribution</h2>
      <div className="mt-4 h-80">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie data={data} dataKey="value" nameKey="name" outerRadius={100} label>
              <Cell />
              <Cell />
              <Cell />
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
