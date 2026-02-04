import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import toast from 'react-hot-toast'

export default function Login() {
  const navigate = useNavigate()
  const { login, isLoading } = useAuthStore()
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  })

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    const result = await login(formData.email, formData.password)

    if (result.success) {
      toast.success('로그인 성공!')
      navigate('/dashboard')
    } else {
      toast.error(result.error)
    }
  }

  return (
    <div className="min-h-screen bg-zinc-950 flex items-center justify-center px-6">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <Link to="/" className="text-3xl font-bold text-white inline-block">
            렌트<span className="text-primary-500">미</span>
          </Link>
          <p className="text-zinc-400 mt-2">계정에 로그인하세요</p>
        </div>

        <div className="card">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-zinc-300 text-sm font-medium mb-2">
                이메일
              </label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className="input"
                placeholder="hello@example.com"
                required
              />
            </div>

            <div>
              <label className="block text-zinc-300 text-sm font-medium mb-2">
                비밀번호
              </label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className="input"
                placeholder="••••••••"
                required
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? '로그인 중...' : '로그인'}
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-zinc-400">
              계정이 없으신가요?{' '}
              <Link to="/register" className="text-primary-500 hover:text-primary-400">
                회원가입
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
