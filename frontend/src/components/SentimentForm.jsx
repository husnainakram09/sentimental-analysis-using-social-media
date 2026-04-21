import { useState } from 'react'

export default function SentimentForm({ onPredict, loading }) {
  const [text, setText] = useState('')

  const submit = (e) => {
    e.preventDefault()
    if (!text.trim()) return
    onPredict(text)
  }

  return (
    <form onSubmit={submit} className="rounded-3xl bg-white p-6 shadow-sm">
      <h2 className="text-lg font-semibold">Single Prediction</h2>
      <p className="mt-1 text-sm text-slate-500">Enter a tweet or social media post.</p>
      <textarea
        className="mt-4 min-h-40 w-full rounded-2xl border border-slate-300 p-4 outline-none focus:border-slate-500"
        placeholder="Example: I love the new update, it feels so much faster now!"
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <button
        type="submit"
        disabled={loading}
        className="mt-4 rounded-2xl bg-slate-950 px-5 py-3 font-medium text-white disabled:opacity-50"
      >
        {loading ? 'Predicting...' : 'Predict Sentiment'}
      </button>
    </form>
  )
}
