import { useState } from 'react'
import { motion } from 'framer-motion'
import CyberBackground from './CyberBackground'

export default function App() {
  const [message, setMessage] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const analyzeMessage = async () => {
    setLoading(true)
    try {
      const res = await fetch('http://127.0.0.1:8000/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message }),
      })
      const data = await res.json()
      setResult(data)
    } catch (err) {
      setResult({ prediction: { label: 'error' }, explanation: 'Server error.' })
    } finally {
      setLoading(false)
    }
  }

  const reset = () => {
    setMessage('')
    setResult(null)
  }

  return (
    <main className="min-h-screen flex items-center justify-center bg-cyber-gradient">
      <CyberBackground />
      <div className="cyber-glass max-w-md w-[95vw] mx-2 px-4 py-6 flex flex-col justify-center items-center z-10 rounded-2xl shadow-cyber">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center space-y-2 mb-6"
        >
          <h1 className="text-3xl sm:text-4xl font-extrabold neon-glitch drop-shadow-lg">
            AI ScamBuster
          </h1>
          <p className="text-base sm:text-lg text-cyan-200 font-mono tracking-widest glitch">
            Real-time cybercrime detection powered by AI 🛡️
          </p>
        </motion.div>
        {/* Input or Result */}
        {!result ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="w-full bg-white/10 backdrop-blur-lg p-4 rounded-xl shadow space-y-4 border border-cyan-400/30"
          >
            <textarea
              rows={4}
              placeholder="Paste suspicious message here..."
              className="w-full p-2 rounded-md bg-black/30 border border-cyan-700 text-white resize-none outline-none placeholder:text-cyan-400 text-sm sm:text-base font-mono"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
            />
            <button
              onClick={analyzeMessage}
              disabled={!message || loading}
              className="w-full py-2 text-base font-semibold bg-cyan-500 hover:bg-cyan-400 rounded-md transition disabled:opacity-50 shadow neon-btn"
            >
              {loading ? 'Analyzing...' : '🧠 Analyze Message'}
            </button>
          </motion.div>
        ) : (
          <motion.div
            initial={{ scale: 0.95, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="w-full bg-white/10 backdrop-blur-lg p-4 rounded-xl shadow space-y-4 border border-cyan-400/30"
          >
            <h2 className="text-lg sm:text-xl font-semibold">
              🎯 Classification:{' '}
              <span
                className={
                  result.prediction.label === 'spam'
                    ? 'text-red-400 neon-glow'
                    : result.prediction.label === 'not spam'
                    ? 'text-green-400 neon-glow'
                    : 'text-yellow-400 neon-glow'
                }
              >
                {result.prediction.label.toUpperCase()}
              </span>
            </h2>
            <p className="text-cyan-200 whitespace-pre-wrap text-sm sm:text-base font-mono">
              🔍 {result.explanation}
            </p>
            <button
              onClick={reset}
              className="w-full py-2 mt-2 bg-gray-800 hover:bg-gray-700 rounded-md text-sm sm:text-base neon-btn"
            >
              🔁 Analyze Another Message
            </button>
          </motion.div>
        )}
      </div>
    </main>
  )
}