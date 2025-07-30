import { Canvas } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'

function Shield() {
  return (
    <mesh scale={0.35} position={[0, 1.2, 0]}>
      <torusKnotGeometry args={[1, 0.3, 128, 32]} />
      <meshStandardMaterial color="#00fff7" emissive="#00fff7" metalness={0.8} roughness={0.2} transparent opacity={0.18} />
    </mesh>
  )
}

export default function CyberBackground() {
  return (
    <div className="fixed inset-0 -z-10">
      <div className="absolute inset-0 bg-gradient-to-br from-[#0f172a] to-[#1e293b]" />
      <div
        className="absolute inset-0 opacity-20 animate-moveGrid"
        style={{
          backgroundImage:
            'linear-gradient(rgba(0,255,247,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(0,255,247,0.1) 1px, transparent 1px)',
          backgroundSize: '32px 32px'
        }}
      />
    </div>
  )
}

// In App.jsx, update LockModel
function LockModel(props) {
  return (
    <group {...props}>
      <mesh position={[0, -0.3, 0]}>
        <boxGeometry args={[0.7, 0.7, 0.3]} />
        <meshStandardMaterial color="#0ea5e9" metalness={0.9} roughness={0.2} />
      </mesh>
      <mesh position={[0, 0.25, 0]}>
        <torusGeometry args={[0.28, 0.08, 16, 100, Math.PI]} />
        <meshStandardMaterial color="#0ea5e9" metalness={0.9} roughness={0.2} />
      </mesh>
    </group>
  );
}