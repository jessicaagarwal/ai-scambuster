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
    <div className="absolute inset-0 -z-10">
      <Canvas camera={{ position: [0, 0, 4] }}>
        <ambientLight intensity={0.7} />
        <pointLight position={[10, 10, 10]} intensity={1.5} />
        <Shield />
        <OrbitControls enableZoom={false} enablePan={false} autoRotate autoRotateSpeed={2} />
      </Canvas>
      <div className="absolute inset-0 bg-gradient-to-br from-[#0f172a]/95 to-[#1e293b]/98 pointer-events-none" />
      <div
        className="absolute inset-0 pointer-events-none animate-moveGrid"
        style={{
          backgroundImage:
            'linear-gradient(rgba(0,255,247,0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(0,255,247,0.04) 1px, transparent 1px)',
          backgroundSize: '32px 32px'
        }}
      />
    </div>
  )
}