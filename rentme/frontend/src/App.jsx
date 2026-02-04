import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './store/authStore'

// Pages
import Landing from './pages/Landing'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Profile from './pages/Profile'
import AIIntro from './pages/AIIntro'
import References from './pages/References'

// Components
import Layout from './components/Layout'
import ProtectedRoute from './components/ProtectedRoute'

function App() {
  return (
    <Routes>
      {/* Public Routes */}
      <Route path="/" element={<Landing />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      {/* Protected Routes */}
      <Route element={<ProtectedRoute />}>
        <Route element={<Layout />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/ai-intro" element={<AIIntro />} />
          <Route path="/references" element={<References />} />
        </Route>
      </Route>

      {/* Fallback */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default App
