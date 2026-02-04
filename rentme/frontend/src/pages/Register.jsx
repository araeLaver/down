import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import toast from 'react-hot-toast'

export default function Register() {
  const navigate = useNavigate()
  const { register, isLoading } = useAuthStore()
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    phone: '',
  })

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (formData.password !== formData.confirmPassword) {
      toast.error('비밀번호가 일치하지 않습니다')
      return
    }

    if (formData.password.length < 6) {
      toast.error('비밀번호는 6자 이상이어야 합니다')
      return
    }

    const result = await register({
      name: formData.name,
      email: formData.email,
      password: formData.password,
      phone: formData.phone,
    })

    if (result.success) {
      toast.success('회원가입 성공!')
      navigate('/dashboard')
    } else {
      toast.error(result.error)
    }
  }

  return (
    <div className="min-h-screen bg-zinc-950 flex items-center justify-center px-6 py-12">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <Link to="/" className="text-3xl font-bold text-white inline-block">
            렌트<span className="text-primary-500">미</span>
          </Link>
          <p className="text-zinc-400 mt-2">무료로 신뢰 프로필을 만드세요</p>
        </div>

        <div className="card">
          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-zinc-300 text-sm font-medium mb-2">
                이름
              </label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                className="input"
                placeholder="홍길동"
                required
              />
            </div>

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
                전화번호
              </label>
              <input
                type="tel"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                className="input"
                placeholder="010-1234-5678"
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
                placeholder="6자 이상"
                required
              />
            </div>

            <div>
              <label className="block text-zinc-300 text-sm font-medium mb-2">
                비밀번호 확인
              </label>
              <input
                type="password"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                className="input"
                placeholder="비밀번호 재입력"
                required
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? '가입 중...' : '회원가입'}
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-zinc-400">
              이미 계정이 있으신가요?{' '}
              <Link to="/login" className="text-primary-500 hover:text-primary-400">
                로그인
              </Link>
            </p>
          </div>

          <p className="mt-6 text-xs text-zinc-500 text-center">
            가입 시{' '}
            <a href="#" className="text-primary-500">이용약관</a> 및{' '}
            <a href="#" className="text-primary-500">개인정보처리방침</a>에 동의합니다
          </p>
        </div>
      </div>
    </div>
  )
}
