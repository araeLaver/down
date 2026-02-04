import { useEffect, useState } from 'react'
import api from '../api/client'
import toast from 'react-hot-toast'

export default function References() {
  const [references, setReferences] = useState([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [creating, setCreating] = useState(false)
  const [formData, setFormData] = useState({
    landlord_name: '',
    landlord_email: '',
    landlord_phone: '',
    property_address: '',
    rental_period: '',
  })

  useEffect(() => {
    fetchReferences()
  }, [])

  const fetchReferences = async () => {
    try {
      const response = await api.get('/references/')
      setReferences(response.data)
    } catch (error) {
      console.error('Failed to fetch references:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setCreating(true)
    try {
      await api.post('/references/request', formData)
      toast.success('레퍼런스 요청이 전송되었습니다')
      setShowModal(false)
      setFormData({
        landlord_name: '',
        landlord_email: '',
        landlord_phone: '',
        property_address: '',
        rental_period: '',
      })
      fetchReferences()
    } catch (error) {
      toast.error('레퍼런스 요청에 실패했습니다')
    } finally {
      setCreating(false)
    }
  }

  const getStatusBadge = (status) => {
    const styles = {
      pending: 'bg-yellow-500/20 text-yellow-500',
      completed: 'bg-green-500/20 text-green-500',
      declined: 'bg-red-500/20 text-red-500',
    }
    const labels = {
      pending: '대기중',
      completed: '완료',
      declined: '거절됨',
    }
    return (
      <span className={`px-3 py-1 rounded-full text-sm ${styles[status]}`}>
        {labels[status]}
      </span>
    )
  }

  const renderStars = (rating) => {
    return Array(5).fill(0).map((_, i) => (
      <span key={i} className={i < rating ? 'text-yellow-500' : 'text-zinc-600'}>
        ★
      </span>
    ))
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
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-white">레퍼런스</h1>
          <p className="text-zinc-400 mt-1">이전 집주인의 평가를 관리하세요</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="btn-primary"
        >
          레퍼런스 요청
        </button>
      </div>

      {references.length === 0 ? (
        <div className="card text-center py-12">
          <div className="text-6xl mb-4">📝</div>
          <h3 className="text-xl font-semibold text-white mb-2">
            아직 레퍼런스가 없습니다
          </h3>
          <p className="text-zinc-400 mb-6">
            이전 집주인에게 레퍼런스를 요청해보세요
          </p>
          <button
            onClick={() => setShowModal(true)}
            className="btn-primary"
          >
            첫 레퍼런스 요청하기
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          {references.map((ref) => (
            <div key={ref.id} className="card">
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-lg font-semibold text-white">
                      {ref.landlord_name}
                    </h3>
                    {getStatusBadge(ref.status)}
                  </div>
                  <p className="text-zinc-400 text-sm mb-1">
                    📍 {ref.property_address}
                  </p>
                  <p className="text-zinc-500 text-sm">
                    거주기간: {ref.rental_period}
                  </p>
                </div>

                {ref.status === 'completed' && ref.rating && (
                  <div className="text-right">
                    <div className="text-lg">{renderStars(ref.rating)}</div>
                    <div className="text-zinc-500 text-sm mt-1">
                      {ref.rating}.0 / 5.0
                    </div>
                  </div>
                )}
              </div>

              {ref.status === 'completed' && ref.comment && (
                <div className="mt-4 p-4 bg-zinc-800 rounded-xl">
                  <p className="text-zinc-300 italic">"{ref.comment}"</p>
                </div>
              )}

              {ref.status === 'pending' && (
                <div className="mt-4 p-4 bg-zinc-800 rounded-xl">
                  <p className="text-zinc-400 text-sm">
                    요청 코드: <span className="text-primary-500 font-mono">{ref.request_code}</span>
                  </p>
                  <p className="text-zinc-500 text-xs mt-1">
                    집주인에게 이 코드를 전달하면 평가를 남길 수 있습니다
                  </p>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Request Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="card max-w-lg w-full max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-white">레퍼런스 요청</h2>
              <button
                onClick={() => setShowModal(false)}
                className="text-zinc-400 hover:text-white"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-5">
              <div>
                <label className="block text-zinc-300 text-sm font-medium mb-2">
                  집주인 이름 *
                </label>
                <input
                  type="text"
                  name="landlord_name"
                  value={formData.landlord_name}
                  onChange={handleChange}
                  className="input"
                  placeholder="홍길동"
                  required
                />
              </div>

              <div>
                <label className="block text-zinc-300 text-sm font-medium mb-2">
                  집주인 이메일
                </label>
                <input
                  type="email"
                  name="landlord_email"
                  value={formData.landlord_email}
                  onChange={handleChange}
                  className="input"
                  placeholder="landlord@example.com"
                />
              </div>

              <div>
                <label className="block text-zinc-300 text-sm font-medium mb-2">
                  집주인 전화번호
                </label>
                <input
                  type="tel"
                  name="landlord_phone"
                  value={formData.landlord_phone}
                  onChange={handleChange}
                  className="input"
                  placeholder="010-1234-5678"
                />
              </div>

              <div>
                <label className="block text-zinc-300 text-sm font-medium mb-2">
                  거주지 주소 *
                </label>
                <input
                  type="text"
                  name="property_address"
                  value={formData.property_address}
                  onChange={handleChange}
                  className="input"
                  placeholder="서울시 강남구 역삼동 123-45"
                  required
                />
              </div>

              <div>
                <label className="block text-zinc-300 text-sm font-medium mb-2">
                  거주 기간 *
                </label>
                <input
                  type="text"
                  name="rental_period"
                  value={formData.rental_period}
                  onChange={handleChange}
                  className="input"
                  placeholder="2023.01 - 2024.12"
                  required
                />
              </div>

              <div className="flex gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="flex-1 btn-secondary"
                >
                  취소
                </button>
                <button
                  type="submit"
                  disabled={creating}
                  className="flex-1 btn-primary disabled:opacity-50"
                >
                  {creating ? '요청 중...' : '요청 보내기'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
