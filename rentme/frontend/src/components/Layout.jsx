import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'

const navItems = [
  { path: '/dashboard', label: '대시보드', icon: '📊' },
  { path: '/profile', label: '내 프로필', icon: '👤' },
  { path: '/references', label: '레퍼런스', icon: '⭐' },
  { path: '/ai-intro', label: 'AI 자기소개', icon: '🤖' },
]

export default function Layout() {
  const navigate = useNavigate()
  const { user, logout } = useAuthStore()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="min-h-screen bg-zinc-950 flex">
      {/* Sidebar */}
      <aside className="w-64 bg-zinc-900 border-r border-zinc-800 flex flex-col">
        <div className="p-6">
          <h1 className="text-2xl font-bold text-white">
            렌트<span className="text-primary-500">미</span>
          </h1>
          <p className="text-zinc-500 text-sm mt-1">세입자 신뢰 프로필</p>
        </div>

        <nav className="flex-1 px-4">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-3 rounded-xl mb-2 transition-colors ${
                  isActive
                    ? 'bg-primary-500/10 text-primary-500'
                    : 'text-zinc-400 hover:text-white hover:bg-zinc-800'
                }`
              }
            >
              <span>{item.icon}</span>
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="p-4 border-t border-zinc-800">
          <div className="flex items-center gap-3 px-4 py-3">
            <div className="w-10 h-10 bg-primary-500/20 rounded-full flex items-center justify-center">
              <span className="text-primary-500 font-semibold">
                {user?.name?.[0] || 'U'}
              </span>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-white font-medium truncate">{user?.name || '사용자'}</p>
              <p className="text-zinc-500 text-sm truncate">{user?.email}</p>
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="w-full mt-2 px-4 py-2 text-zinc-400 hover:text-white hover:bg-zinc-800 rounded-lg transition-colors text-left"
          >
            로그아웃
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-auto">
        <div className="p-8">
          <Outlet />
        </div>
      </main>
    </div>
  )
}
