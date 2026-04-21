import { useEffect, useMemo, useState } from 'react'
import {
  LayoutDashboard,
  PenSquare,
  Upload,
  History,
  Info,
  MessageSquare,
  SmilePlus,
  Meh,
  Frown,
  ShieldCheck,
  LogOut,
  Search,
} from 'lucide-react'
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
  Legend,
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
} from 'recharts'
import api from './services/api'

const SIDEBAR = [
  { key: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { key: 'predict', label: 'Predict', icon: PenSquare },
  { key: 'batch', label: 'Batch Analysis', icon: Upload },
  { key: 'history', label: 'History', icon: History },
  { key: 'about', label: 'About', icon: Info },
]

const COLORS = {
  positive: '#22c55e',
  neutral: '#f59e0b',
  negative: '#ef4444',
}

function sentimentBadge(sentiment) {
  const map = {
    positive: 'bg-green-100 text-green-700',
    neutral: 'bg-amber-100 text-amber-700',
    negative: 'bg-red-100 text-red-700',
  }
  return map[sentiment] || 'bg-slate-100 text-slate-700'
}

function AuthScreen({ onAuthSuccess }) {
  const [tab, setTab] = useState('login')
  const [form, setForm] = useState({ name: '', email: '', password: '' })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const submit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const endpoint = tab === 'login' ? '/auth/login' : '/auth/register'
      const payload = tab === 'login'
        ? { email: form.email, password: form.password }
        : { name: form.name, email: form.email, password: form.password }
      const { data } = await api.post(endpoint, payload)
      localStorage.setItem('token', data.access_token)
      localStorage.setItem('user', JSON.stringify(data.user))
      onAuthSuccess(data.user)
    } catch (err) {
      console.log(err?.response)
      setError(err?.response?.data?.detail[0]?.msg || err?.response?.data?.detail || 'Authentication failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-100 p-6">
      <div className="grid w-full max-w-6xl overflow-hidden rounded-[2rem] bg-white shadow-2xl lg:grid-cols-2">
        <div className="bg-indigo-600 p-10 text-white">
          <div className="flex items-center gap-3">
            <MessageSquare className="h-10 w-10" />
            <div>
              <h1 className="text-3xl font-bold">Sentiment Analysis</h1>
              <p className="mt-2 text-indigo-100">Private user dashboard with login, analytics, and history.</p>
            </div>
          </div>
          <div className="mt-10 space-y-5">
            <div className="rounded-2xl bg-white/10 p-4">
              <p className="font-semibold">Separate user accounts</p>
              <p className="mt-1 text-sm text-indigo-100">Each user sees only their own predictions and charts.</p>
            </div>
            <div className="rounded-2xl bg-white/10 p-4">
              <p className="font-semibold">Prediction history</p>
              <p className="mt-1 text-sm text-indigo-100">Every prediction is saved with confidence and timestamp.</p>
            </div>
            <div className="rounded-2xl bg-white/10 p-4">
              <p className="font-semibold">Dashboard analytics</p>
              <p className="mt-1 text-sm text-indigo-100">Pie chart, trend chart, and searchable history.</p>
            </div>
          </div>
        </div>

        <div className="p-10">
          <div className="mb-8 flex rounded-2xl bg-slate-100 p-1">
            <button onClick={() => setTab('login')} className={`flex-1 rounded-2xl px-4 py-3 font-medium ${tab === 'login' ? 'bg-white shadow-sm' : 'text-slate-500'}`}>
              Login
            </button>
            <button onClick={() => setTab('register')} className={`flex-1 rounded-2xl px-4 py-3 font-medium ${tab === 'register' ? 'bg-white shadow-sm' : 'text-slate-500'}`}>
              Register
            </button>
          </div>

          <h2 className="text-3xl font-bold text-slate-900">{tab === 'login' ? 'Welcome back' : 'Create account'}</h2>
          <p className="mt-2 text-slate-500">{tab === 'login' ? 'Login to access your personal dashboard.' : 'Register a new user to get a private dashboard.'}</p>

          <form onSubmit={submit} className="mt-8 space-y-4">
            {tab === 'register' && (
              <div>
                <label className="mb-2 block text-sm font-medium text-slate-700">Full name</label>
                <input value={form.name} onChange={(e) => setForm((p) => ({ ...p, name: e.target.value }))} className="w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none focus:border-indigo-400" required />
              </div>
            )}
            <div>
              <label className="mb-2 block text-sm font-medium text-slate-700">Email</label>
              <input type="email" value={form.email} onChange={(e) => setForm((p) => ({ ...p, email: e.target.value }))} className="w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none focus:border-indigo-400" required />
            </div>
            <div>
              <label className="mb-2 block text-sm font-medium text-slate-700">Password</label>
              <input type="password" value={form.password} onChange={(e) => setForm((p) => ({ ...p, password: e.target.value }))} className="w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none focus:border-indigo-400" required />
            </div>
            {error && <div className="rounded-2xl bg-red-50 px-4 py-3 text-sm text-red-600">{error}</div>}
            <button type='submit' disabled={loading} className="w-full rounded-2xl bg-indigo-600 px-4 py-3 font-semibold text-white hover:bg-indigo-700 disabled:opacity-50">
              {loading ? 'Please wait...' : tab === 'login' ? 'Login' : 'Create account'}
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}

function StatCard({ title, value, subtitle, icon: Icon, iconClass }) {
  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm text-slate-500">{title}</p>
          <h3 className="mt-2 text-3xl font-bold text-slate-900">{value}</h3>
          <p className="mt-1 text-sm text-slate-500">{subtitle}</p>
        </div>
        <div className={`flex h-14 w-14 items-center justify-center rounded-2xl ${iconClass}`}>
          <Icon className="h-7 w-7 text-white" />
        </div>
      </div>
    </div>
  )
}

function PredictPanel({ onPredict, loading, result }) {
  const [text, setText] = useState('')
  const submit = (e) => {
    e.preventDefault()
    if (!text.trim()) return
    onPredict(text)
  }
  return (
    <div className="grid gap-6 xl:grid-cols-2">
      <form onSubmit={submit} className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-2xl font-bold text-slate-900">Single Prediction</h2>
        <p className="mt-2 text-slate-500">Enter a tweet or social media post to analyze sentiment.</p>
        <textarea value={text} onChange={(e) => setText(e.target.value)} className="mt-4 min-h-48 w-full rounded-2xl border border-slate-300 p-4 outline-none focus:border-indigo-400" placeholder="The update is okay, nothing special." />
        <button disabled={loading} className="mt-4 rounded-2xl bg-slate-900 px-5 py-3 font-medium text-white disabled:opacity-50">{loading ? 'Predicting...' : 'Predict Sentiment'}</button>
      </form>
      <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-2xl font-bold text-slate-900">Latest Result</h2>
        {!result ? <p className="mt-4 text-slate-500">No prediction yet.</p> : (
          <div className="mt-4 space-y-4">
            <div className="rounded-2xl bg-slate-50 p-4 text-sm text-slate-700">{result.text}</div>
            <div className="grid grid-cols-2 gap-4">
              <div className="rounded-2xl border border-slate-200 p-4"><div className="text-sm text-slate-500">Label</div><div className="mt-2 text-2xl font-bold capitalize">{result.label}</div></div>
              <div className="rounded-2xl border border-slate-200 p-4"><div className="text-sm text-slate-500">Confidence</div><div className="mt-2 text-2xl font-bold">{(result.confidence * 100).toFixed(2)}%</div></div>
            </div>
            <div className="rounded-2xl border border-slate-200 p-4 text-sm">
              <div>Negative: {(result.probabilities.negative * 100).toFixed(2)}%</div>
              <div>Neutral: {(result.probabilities.neutral * 100).toFixed(2)}%</div>
              <div>Positive: {(result.probabilities.positive * 100).toFixed(2)}%</div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default function App() {
  const [user, setUser] = useState(() => {
    try {
      const raw = localStorage.getItem('user')
      return raw ? JSON.parse(raw) : null
    } catch {
      return null
    }
  })
  const [active, setActive] = useState('dashboard')
  const [search, setSearch] = useState('')
  const [stats, setStats] = useState({ total_predictions: 0, positive: 0, neutral: 0, negative: 0 })
  const [history, setHistory] = useState([])
  const [trends, setTrends] = useState([])
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setUser(null)
  }

  const loadDashboard = async () => {
    const [statsRes, historyRes, trendsRes] = await Promise.all([
      api.get('/analytics/stats'),
      api.get('/analytics/history?limit=50'),
      api.get('/analytics/trends'),
    ])
    setStats(statsRes.data)
    setHistory(historyRes.data.history)
    setTrends(trendsRes.data.trends)
  }

  useEffect(() => {
    const init = async () => {
      if (!localStorage.getItem('token')) return
      try {
        const { data } = await api.get('/auth/me')
        setUser(data)
        await loadDashboard()
      } catch {
        logout()
      }
    }
    init()
  }, [])

  const filteredHistory = useMemo(() => {
    if (!search.trim()) return history
    return history.filter((item) => item.text.toLowerCase().includes(search.toLowerCase()) || item.label.toLowerCase().includes(search.toLowerCase()))
  }, [history, search])

  const pieData = [
    { name: 'Negative', value: stats.negative ?? 0, fill: COLORS.negative },
    { name: 'Neutral', value: stats.neutral ?? 0, fill: COLORS.neutral },
    { name: 'Positive', value: stats.positive ?? 0, fill: COLORS.positive },
  ]

  const handlePredict = async (text) => {
    try {
      setLoading(true)
      const { data } = await api.post('/predictions/predict', { text })
      setResult(data)
      await loadDashboard()
      setActive('dashboard')
    } catch (err) {
      alert(err?.response?.data?.detail || 'Prediction failed')
    } finally {
      setLoading(false)
    }
  }

  const handleBatchUpload = async (e) => {
    const file = e.target.files?.[0]
    if (!file) return
    const text = await file.text()
    const rows = text.split(/\r?\n/).map((line) => line.trim()).filter(Boolean)
    if (!rows.length) return
    try {
      setLoading(true)
      await api.post('/predictions/batch', { texts: rows })
      await loadDashboard()
      setActive('history')
      alert('Batch analysis completed')
    } catch (err) {
      alert(err?.response?.data?.detail || 'Batch prediction failed')
    } finally {
      setLoading(false)
      e.target.value = ''
    }
  }

  if (!user) {
    return <AuthScreen onAuthSuccess={async (loggedInUser) => { setUser(loggedInUser); await loadDashboard() }} />
  }

  return (
    <div className="min-h-screen bg-slate-100 text-slate-900">
      <div className="grid min-h-screen lg:grid-cols-[280px_1fr]">
        <aside className="flex flex-col border-r border-slate-200 bg-white p-5">
          <div className="flex items-center gap-3 px-2 py-3">
            <div className="rounded-2xl bg-indigo-600 p-2 text-white"><MessageSquare className="h-6 w-6" /></div>
            <div>
              <h1 className="text-2xl font-bold text-indigo-600">Sentiment Analysis</h1>
              <p className="text-sm text-slate-500">Private user dashboard</p>
            </div>
          </div>

          <nav className="mt-8 space-y-2">
            {SIDEBAR.map((item) => {
              const Icon = item.icon
              const isActive = active === item.key
              return (
                <button key={item.key} onClick={() => setActive(item.key)} className={`flex w-full items-center gap-3 rounded-2xl px-4 py-3 text-left transition ${isActive ? 'bg-indigo-50 text-indigo-600' : 'text-slate-600 hover:bg-slate-50'}`}>
                  <Icon className="h-5 w-5" />
                  <span className="font-medium">{item.label}</span>
                </button>
              )
            })}
          </nav>

          <div className="mt-auto space-y-4">
            <div className="rounded-2xl border border-slate-200 p-4">
              <div className="flex items-center gap-3"><ShieldCheck className="h-5 w-5 text-green-600" /><span className="font-medium text-slate-700">Connected</span></div>
              <p className="mt-2 text-sm text-slate-500">{user.email}</p>
            </div>
            <button onClick={logout} className="flex w-full items-center justify-center gap-2 rounded-2xl bg-slate-900 px-4 py-3 font-semibold text-white"><LogOut className="h-5 w-5" /> Logout</button>
          </div>
        </aside>

        <main className="p-6 lg:p-8">
          <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
            <div>
              <h2 className="text-5xl font-bold tracking-tight">Dashboard</h2>
              <p className="mt-2 text-lg text-slate-500">Overview of {user.name}'s sentiment analysis</p>
            </div>
            <div className="flex items-center gap-3 rounded-2xl bg-white px-4 py-3 shadow-sm">
              <Search className="h-5 w-5 text-slate-400" />
              <input placeholder="Search user history" value={search} onChange={(e) => setSearch(e.target.value)} className="w-64 outline-none" />
            </div>
          </div>

          <div className="mt-8 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            <StatCard title="Total Predictions" value={stats.total_predictions} subtitle="All time" icon={MessageSquare} iconClass="bg-indigo-600" />
            <StatCard title="Positive" value={stats.positive} subtitle={`${stats.total_predictions ? ((stats.positive / stats.total_predictions) * 100).toFixed(1) : 0}%`} icon={SmilePlus} iconClass="bg-green-500" />
            <StatCard title="Neutral" value={stats.neutral} subtitle={`${stats.total_predictions ? ((stats.neutral / stats.total_predictions) * 100).toFixed(1) : 0}%`} icon={Meh} iconClass="bg-amber-500" />
            <StatCard title="Negative" value={stats.negative} subtitle={`${stats.total_predictions ? ((stats.negative / stats.total_predictions) * 100).toFixed(1) : 0}%`} icon={Frown} iconClass="bg-red-500" />
          </div>

          {active === 'predict' && <div className="mt-6"><PredictPanel onPredict={handlePredict} loading={loading} result={result} /></div>}

          {active === 'batch' && (
            <div className="mt-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <h2 className="text-2xl font-bold text-slate-900">Batch Analysis</h2>
              <p className="mt-2 text-slate-500">Upload a .txt file with one text item per line.</p>
              <input type="file" accept=".txt,.csv" onChange={handleBatchUpload} className="mt-4 block" disabled={loading} />
              <p className="mt-3 text-sm text-slate-500">CSV support works best when each line contains one text input.</p>
            </div>
          )}

          {(active === 'dashboard' || active === 'history' || active === 'about') && (
            <>
              <div className="mt-6 grid gap-6 xl:grid-cols-2">
                <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
                  <h2 className="text-2xl font-bold text-slate-900">Sentiment Distribution</h2>
                  <div className="mt-4 h-80">
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie data={pieData} dataKey="value" nameKey="name" outerRadius={120} labelLine={false} label={({ percent }) => `${(percent * 100).toFixed(1)}%`}>
                          {pieData.map((entry, index) => <Cell key={index} fill={entry.fill} />)}
                        </Pie>
                        <Tooltip />
                        <Legend />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
                  <h2 className="text-2xl font-bold text-slate-900">Predictions Over Time</h2>
                  <div className="mt-4 h-80">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={trends}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                        <XAxis dataKey="date" />
                        <YAxis allowDecimals={false} />
                        <Tooltip />
                        <Legend />
                        <Line type="monotone" dataKey="positive" stroke={COLORS.positive} strokeWidth={3} />
                        <Line type="monotone" dataKey="neutral" stroke={COLORS.neutral} strokeWidth={3} />
                        <Line type="monotone" dataKey="negative" stroke={COLORS.negative} strokeWidth={3} />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </div>

              <div className="mt-6 rounded-3xl border border-slate-200 bg-white shadow-sm">
                <div className="border-b border-slate-200 px-6 py-4"><h2 className="text-2xl font-bold text-slate-900">Recent Predictions</h2></div>
                <div className="overflow-x-auto">
                  <table className="min-w-full text-left text-sm">
                    <thead className="bg-slate-50 text-slate-500">
                      <tr>
                        <th className="px-6 py-4 font-semibold">Text</th>
                        <th className="px-6 py-4 font-semibold">Sentiment</th>
                        <th className="px-6 py-4 font-semibold">Confidence</th>
                        <th className="px-6 py-4 font-semibold">Date</th>
                      </tr>
                    </thead>
                    <tbody>
                      {filteredHistory.map((item, index) => (
                        <tr key={`${item.created_at}-${index}`} className="border-t border-slate-100">
                          <td className="px-6 py-4 text-slate-700">{item.text}</td>
                          <td className="px-6 py-4"><span className={`rounded-full px-3 py-1 text-xs font-semibold capitalize ${sentimentBadge(item.label)}`}>{item.label}</span></td>
                          <td className="px-6 py-4 text-indigo-600">{item.confidence.toFixed(2)}</td>
                          <td className="px-6 py-4 text-slate-500">{item.created_at ? new Date(item.created_at).toLocaleString() : '-'}</td>
                        </tr>
                      ))}
                      {!filteredHistory.length && (
                        <tr><td colSpan="4" className="px-6 py-10 text-center text-slate-500">No history found yet.</td></tr>
                      )}
                    </tbody>
                  </table>
                </div>
              </div>

              {active === 'about' && (
                <div className="mt-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                  <h2 className="text-2xl font-bold text-slate-900">About this dashboard</h2>
                  <p className="mt-3 text-slate-600">This version includes authentication, per-user private dashboards, stored prediction history, batch processing, and analytics powered by FastAPI and MongoDB.</p>
                </div>
              )}
            </>
          )}
        </main>
      </div>
    </div>
  )
}
