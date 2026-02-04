import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import api from '../api/client'

export default function Dashboard() {
  const { user } = useAuthStore()
  const [profile, setProfile] = useState(null)
  const [references, setReferences] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [profileRes, refsRes] = await Promise.all([
          api.get('/profiles/me'),
          api.get('/references/'),
        ])
        setProfile(profileRes.data)
        setReferences(refsRes.data)
      } catch (error) {
        console.error('Failed to fetch data:', error)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  const trustScore = profile?.trust_score || 0
  const completedRefs = references.filter((r) => r.status === 'completed').length
  const pendingRefs = references.filter((r) => r.status === 'pending').length

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-zinc-400">로딩 중...</div>
      </div>
    )
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white">
          안녕하세요, {user?.name || '사용자'}님! 👋
        </h1>
        <p className="text-zinc-400 mt-1">신뢰 프로필 현황을 확인하세요</p>
      </div>

      {/* Stats Grid */}
      <div className="grid md:grid-cols-4 gap-6 mb-8">
        <div className="card">
          <div className="text-zinc-400 text-sm mb-1">신뢰 점수</div>
          <div className="text-4xl font-bold text-primary-500">{trustScore}</div>
          <div className="text-zinc-500 text-sm mt-1">/ 100</div>
        </div>

        <div className="card">
          <div className="text-zinc-400 text-sm mb-1">완료된 레퍼런스</div>
          <div className="text-4xl font-bold text-green-500">{completedRefs}</div>
          <div className="text-zinc-500 text-sm mt-1">건</div>
        </div>

        <div className="card">
          <div className="text-zinc-400 text-sm mb-1">대기중 레퍼런스</div>
          <div className="text-4xl font-bold text-yellow-500">{pendingRefs}</div>
          <div className="text-zinc-500 text-sm mt-1">건</div>
        </div>

        <div className="card">
          <div className="text-zinc-400 text-sm mb-1">프로필 완성도</div>
          <div className="text-4xl font-bold text-white">
            {profile ? Math.round((profile.trust_score / 100) * 100) : 0}%
          </div>
          <div className="text-zinc-500 text-sm mt-1">완료</div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold text-white mb-4">빠른 시작</h2>
        <div className="grid md:grid-cols-3 gap-4">
          <Link
            to="/profile"
            className="card hover:border-primary-500/50 transition-colors group"
          >
            <div className="text-3xl mb-3">👤</div>
            <h3 className="text-white font-semibold group-hover:text-primary-500 transition-colors">
              프로필 완성하기
            </h3>
            <p className="text-zinc-400 text-sm mt-1">
              기본 정보와 인증을 완료하세요
            </p>
          </Link>

          <Link
            to="/references"
            className="card hover:border-primary-500/50 transition-colors group"
          >
            <div className="text-3xl mb-3">⭐</div>
            <h3 className="text-white font-semibold group-hover:text-primary-500 transition-colors">
              레퍼런스 요청
            </h3>
            <p className="text-zinc-400 text-sm mt-1">
              이전 집주인에게 평가를 요청하세요
            </p>
          </Link>

          <Link
            to="/ai-intro"
            className="card hover:border-primary-500/50 transition-colors group"
          >
            <div className="text-3xl mb-3">🤖</div>
            <h3 className="text-white font-semibold group-hover:text-primary-500 transition-colors">
              AI 자기소개 생성
            </h3>
            <p className="text-zinc-400 text-sm mt-1">
              AI가 작성하는 맞춤 자기소개
            </p>
          </Link>
        </div>
      </div>

      {/* Verification Status */}
      <div>
        <h2 className="text-xl font-semibold text-white mb-4">인증 현황</h2>
        <div className="card">
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className={`w-3 h-3 rounded-full ${profile?.employment_verified ? 'bg-green-500' : 'bg-zinc-600'}`}></span>
                <span className="text-white">재직 인증</span>
              </div>
              {profile?.employment_verified ? (
                <span className="text-green-500 text-sm">완료</span>
              ) : (
                <Link to="/profile" className="text-primary-500 text-sm hover:underline">
                  인증하기
                </Link>
              )}
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className={`w-3 h-3 rounded-full ${profile?.income_verified ? 'bg-green-500' : 'bg-zinc-600'}`}></span>
                <span className="text-white">소득 인증</span>
              </div>
              {profile?.income_verified ? (
                <span className="text-green-500 text-sm">완료</span>
              ) : (
                <Link to="/profile" className="text-primary-500 text-sm hover:underline">
                  인증하기
                </Link>
              )}
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className={`w-3 h-3 rounded-full ${profile?.credit_verified ? 'bg-green-500' : 'bg-zinc-600'}`}></span>
                <span className="text-white">신용 인증</span>
              </div>
              {profile?.credit_verified ? (
                <span className="text-green-500 text-sm">완료</span>
              ) : (
                <Link to="/profile" className="text-primary-500 text-sm hover:underline">
                  인증하기
                </Link>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
