import { useEffect, useState } from 'react'
import { useAuthStore } from '../store/authStore'
import api from '../api/client'
import toast from 'react-hot-toast'

export default function Profile() {
  const { user } = useAuthStore()
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [formData, setFormData] = useState({
    occupation: '',
    company: '',
    annual_income: '',
    bio: '',
  })

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await api.get('/profiles/me')
        setProfile(response.data)
        setFormData({
          occupation: response.data.occupation || '',
          company: response.data.company || '',
          annual_income: response.data.annual_income || '',
          bio: response.data.bio || '',
        })
      } catch (error) {
        console.error('Failed to fetch profile:', error)
      } finally {
        setLoading(false)
      }
    }
    fetchProfile()
  }, [])

  const handleChange = (e) => {
    const value = e.target.name === 'annual_income'
      ? parseInt(e.target.value) || ''
      : e.target.value
    setFormData({ ...formData, [e.target.name]: value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSaving(true)
    try {
      const response = await api.put('/profiles/me', formData)
      setProfile(response.data)
      toast.success('프로필이 저장되었습니다')
    } catch (error) {
      toast.error('프로필 저장에 실패했습니다')
    } finally {
      setSaving(false)
    }
  }

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
        <h1 className="text-3xl font-bold text-white">내 프로필</h1>
        <p className="text-zinc-400 mt-1">신뢰 프로필 정보를 관리하세요</p>
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Profile Form */}
        <div className="lg:col-span-2">
          <div className="card">
            <h2 className="text-xl font-semibold text-white mb-6">기본 정보</h2>
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-zinc-300 text-sm font-medium mb-2">
                    이름
                  </label>
                  <input
                    type="text"
                    value={user?.name || ''}
                    className="input bg-zinc-800"
                    disabled
                  />
                </div>

                <div>
                  <label className="block text-zinc-300 text-sm font-medium mb-2">
                    이메일
                  </label>
                  <input
                    type="email"
                    value={user?.email || ''}
                    className="input bg-zinc-800"
                    disabled
                  />
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-zinc-300 text-sm font-medium mb-2">
                    직업
                  </label>
                  <input
                    type="text"
                    name="occupation"
                    value={formData.occupation}
                    onChange={handleChange}
                    className="input"
                    placeholder="예: 소프트웨어 엔지니어"
                  />
                </div>

                <div>
                  <label className="block text-zinc-300 text-sm font-medium mb-2">
                    회사명
                  </label>
                  <input
                    type="text"
                    name="company"
                    value={formData.company}
                    onChange={handleChange}
                    className="input"
                    placeholder="예: (주)테크컴퍼니"
                  />
                </div>
              </div>

              <div>
                <label className="block text-zinc-300 text-sm font-medium mb-2">
                  연간 소득 (만원)
                </label>
                <input
                  type="number"
                  name="annual_income"
                  value={formData.annual_income}
                  onChange={handleChange}
                  className="input"
                  placeholder="예: 5000"
                />
              </div>

              <div>
                <label className="block text-zinc-300 text-sm font-medium mb-2">
                  자기소개
                </label>
                <textarea
                  name="bio"
                  value={formData.bio}
                  onChange={handleChange}
                  className="input min-h-[120px] resize-none"
                  placeholder="간단한 자기소개를 작성해주세요"
                />
              </div>

              <button
                type="submit"
                disabled={saving}
                className="btn-primary disabled:opacity-50"
              >
                {saving ? '저장 중...' : '프로필 저장'}
              </button>
            </form>
          </div>

          {/* Verification Section */}
          <div className="card mt-6">
            <h2 className="text-xl font-semibold text-white mb-6">인증 관리</h2>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-zinc-800 rounded-xl">
                <div>
                  <div className="text-white font-medium">재직 인증</div>
                  <div className="text-zinc-400 text-sm">재직증명서를 통한 인증</div>
                </div>
                {profile?.employment_verified ? (
                  <span className="px-3 py-1 bg-green-500/20 text-green-500 rounded-full text-sm">
                    인증완료
                  </span>
                ) : (
                  <button className="btn-secondary text-sm py-2">
                    인증하기
                  </button>
                )}
              </div>

              <div className="flex items-center justify-between p-4 bg-zinc-800 rounded-xl">
                <div>
                  <div className="text-white font-medium">소득 인증</div>
                  <div className="text-zinc-400 text-sm">소득증명서를 통한 인증</div>
                </div>
                {profile?.income_verified ? (
                  <span className="px-3 py-1 bg-green-500/20 text-green-500 rounded-full text-sm">
                    인증완료
                  </span>
                ) : (
                  <button className="btn-secondary text-sm py-2">
                    인증하기
                  </button>
                )}
              </div>

              <div className="flex items-center justify-between p-4 bg-zinc-800 rounded-xl">
                <div>
                  <div className="text-white font-medium">신용 인증</div>
                  <div className="text-zinc-400 text-sm">신용점수 연동</div>
                </div>
                {profile?.credit_verified ? (
                  <span className="px-3 py-1 bg-green-500/20 text-green-500 rounded-full text-sm">
                    인증완료
                  </span>
                ) : (
                  <button className="btn-secondary text-sm py-2">
                    인증하기
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Trust Score Card */}
        <div>
          <div className="card sticky top-8">
            <h2 className="text-xl font-semibold text-white mb-6">신뢰 점수</h2>
            <div className="flex flex-col items-center">
              <div className="w-40 h-40 rounded-full border-4 border-primary-500 flex items-center justify-center mb-6">
                <div className="text-center">
                  <div className="text-5xl font-bold text-primary-500">
                    {profile?.trust_score || 0}
                  </div>
                  <div className="text-zinc-500">/ 100</div>
                </div>
              </div>

              <div className="w-full space-y-3">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-zinc-400">프로필 완성도</span>
                    <span className="text-white">30%</span>
                  </div>
                  <div className="h-2 bg-zinc-800 rounded-full overflow-hidden">
                    <div className="h-full bg-primary-500 rounded-full" style={{ width: '30%' }}></div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-zinc-400">인증 점수</span>
                    <span className="text-white">
                      {(profile?.employment_verified ? 33 : 0) +
                       (profile?.income_verified ? 33 : 0) +
                       (profile?.credit_verified ? 34 : 0)}%
                    </span>
                  </div>
                  <div className="h-2 bg-zinc-800 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-green-500 rounded-full"
                      style={{
                        width: `${(profile?.employment_verified ? 33 : 0) +
                                 (profile?.income_verified ? 33 : 0) +
                                 (profile?.credit_verified ? 34 : 0)}%`
                      }}
                    ></div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-zinc-400">레퍼런스</span>
                    <span className="text-white">0%</span>
                  </div>
                  <div className="h-2 bg-zinc-800 rounded-full overflow-hidden">
                    <div className="h-full bg-yellow-500 rounded-full" style={{ width: '0%' }}></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
