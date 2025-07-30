import React, { useState, Suspense } from 'react';
import CyberBackground from './CyberBackground';
import { motion } from 'framer-motion';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Stage } from '@react-three/drei';

function App() {
  const [message, setMessage] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzeMessage = async () => {
    if (!message.trim()) return;
    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: message }),
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error analyzing message:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <CyberBackground />
      <div className="min-h-screen flex flex-col items-center justify-center px-4 py-8 max-w-4xl mx-auto relative">
        {/* Header Section */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <div className="w-32 h-32 mx-auto mb-6">
            <Canvas camera={{ position: [0, 0, 2.5], fov: 50 }}>
              <ambientLight intensity={0.7} />
              <directionalLight position={[2, 2, 2]} intensity={1} />
              <Suspense fallback={null}>
                <Stage environment={null} intensity={0.5} shadows={false}>
                  <LockModel scale={1.1} />
                </Stage>
              </Suspense>
              <OrbitControls enableZoom={false} enablePan={false} autoRotate autoRotateSpeed={2} />
            </Canvas>
          </div>
          <motion.h1
            className="text-5xl font-black text-center neon-glitch tracking-tight mb-4"
            initial={{ scale: 0.9 }}
            animate={{ scale: 1 }}
            transition={{ duration: 0.5 }}
          >
            AI ScamBuster
          </motion.h1>
        </motion.div>

        {/* Main Content */}
        <motion.div
          className="w-full max-w-xl"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          {!result ? (
            <motion.div
              className="space-y-6"
              layout
            >
              <div className="relative">
                <motion.div
                  className="absolute inset-0 bg-cyan-500/20 rounded-xl blur-xl"
                  animate={{
                    scale: [1, 1.02, 1],
                    opacity: [0.5, 0.3, 0.5],
                  }}
                  transition={{
                    duration: 2,
                    repeat: Infinity,
                    ease: "easeInOut"
                  }}
                />
                <textarea
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  placeholder="Paste suspicious message..."
                  className="w-full p-6 rounded-xl bg-gray-900/90 text-white border-2 border-cyan-500/30 focus:border-cyan-400 focus:outline-none font-mono placeholder-cyan-300/50 shadow-[0_0_15px_rgba(6,182,212,0.15)] resize-none relative z-10"
                  rows={6}
                />
              </div>
              <motion.button
                onClick={analyzeMessage}
                disabled={loading || !message.trim()}
                className={`w-full py-4 rounded-xl text-xl font-bold bg-gradient-to-r from-cyan-500 to-blue-500 text-white shadow-lg transition-all ${
                  loading || !message.trim() ? 'opacity-50 cursor-not-allowed' : 'hover:shadow-cyan-500/25'
                }`}
                whileHover={{ scale: message.trim() ? 1.02 : 1 }}
                whileTap={{ scale: message.trim() ? 0.98 : 1 }}
              >
                {loading ? (
                  <span className="flex items-center justify-center gap-3">
                    <motion.span
                      animate={{ rotate: 360 }}
                      transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                    >
                      ⚡
                    </motion.span>
                    Analyzing...
                  </span>
                ) : (
                  'Detect Scam'
                )}
              </motion.button>
            </motion.div>
          ) : (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="rounded-2xl bg-gray-900/90 shadow-2xl p-8 border-2 border-cyan-500/20"
            >
              <div className="flex items-center gap-2 text-2xl font-bold mb-2">
                {result.label === 'spam' ? (
                  <span className="text-red-400">🚨</span>
                ) : result.label === 'not spam' ? (
                  <span className="text-green-400">✅</span>
                ) : (
                  <span className="text-yellow-400">⚠️</span>
                )}
                <span
                  className={
                    result.label === 'spam'
                      ? 'text-red-400 neon-glitch'
                      : result.label === 'not spam'
                      ? 'text-green-400 neon-glitch'
                      : 'text-yellow-400 neon-glitch'
                  }
                >
                  {result.label.toUpperCase()}
                </span>
              </div>
              <div className="space-y-2 text-base">
                <div className="flex items-start gap-2">
                  <span className="text-cyan-300 text-lg">💬</span>
                  <span className="text-cyan-100">{result.reason}</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-cyan-300 text-lg">🎯</span>
                  <span className="text-cyan-100 font-semibold">{(result.confidence * 100).toFixed(2)}%</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-cyan-300 text-lg">🧠</span>
                  <span className="text-cyan-100">{result.source}</span>
                </div>
              </div>
              <button
                className="mt-6 w-full py-3 rounded-xl bg-gradient-to-r from-gray-800 to-gray-700 text-white font-bold hover:from-gray-700 hover:to-gray-600 transition-all border border-cyan-500/20"
                onClick={() => {
                  setResult(null);
                  setMessage('');
                }}
              >
                Analyze Another Message
              </button>
            </motion.div>
          )}
        </motion.div>
      </div>
    </>
  );
}

function LockModel(props) {
  // A simple lock: cylinder (shackle) + box (body)
  return (
    <group {...props}>
      {/* Lock Body */}
      <mesh position={[0, -0.3, 0]}>
        <boxGeometry args={[0.7, 0.7, 0.3]} />
        <meshStandardMaterial color="#06b6d4" metalness={0.7} roughness={0.3} />
      </mesh>
      {/* Lock Shackle */}
      <mesh position={[0, 0.25, 0]}>
        <torusGeometry args={[0.28, 0.08, 16, 100, Math.PI]} />
        <meshStandardMaterial color="#fbbf24" metalness={1} roughness={0.2} />
      </mesh>
    </group>
  );
}

export default App;