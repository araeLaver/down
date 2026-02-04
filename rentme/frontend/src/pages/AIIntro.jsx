import { useEffect, useState } from 'react'
import api from '../api/client'
import toast from 'react-hot-toast'

export default function AIIntro() {
  const [intros, setIntros] = useState([])
  const [loading, setLoading] = useState(true)
  const [generating, setGenerating] = useState(false)
  const [selectedTone, setSelectedTone] = useState('professional')

  const tones = [
    { value: 'professional', label: '전문적', emoji: '💼', desc: '신뢰감 있고 격식있는 톤' },
    { value: 'friendly', label: '친근한', emoji: '😊', desc: '따뜻하고 친근한 톤' },
    { value: 'concise', label: '간결한', emoji: '📝', desc: '핵심만 담은 짧은 톤' },
  ]

  useEffect(() => {
    fetchIntros()
  }, [])

  const fetchIntros = async () => {
    try {
      const response = await api.get('/ai/intros')
      setIntros(response.data)
    } catch (error) {
      console.error('Failed to fetch intros:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleGenerate = async () => {
    setGenerating(true)
    try {
      const response = await api.post('/ai/generate', { tone: selectedTone })
      setIntros([response.data, ...intros])
      toast.success('AI 자기소개가 생성되었습니다!')
    } catch (error) {
      toast.error(error.response?.data?.detail || 'AI 자기소개 생성에 실패했습니다')
    } finally {
      setGenerating(false)
    }
  }

  const handleCopy = (text) => {
    navigator.clipboard.writeText(text)
    toast.success('클립보드에 복사되었습니다')
  }

  const handleDelete = async (id) => {
    try {
      await api.delete(`/ai/intros/${id}`)
      setIntros(intros.filter((i) => i.id !== id))
      toast.success('삭제되었습니다')
    } catch (error) {
      toast.error('삭제에 실패했습니다')
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
        <h1 className="text-3xl font-bold text-white">AI 자기소개</h1>
        <p className="text-zinc-400 mt-1">
          AI가 당신의 프로필을 바탕으로 맞춤 자기소개를 작성해드립니다
        </p>
      </div>

      {/* Generate Section */}
      <div className="card mb-8">
        <h2 className="text-xl font-semibold text-white mb-4">새 자기소개 생성</h2>
        <p className="text-zinc-400 text-sm mb-6">
          원하는 톤을 선택하고 AI가 작성하는 자기소개를 받아보세요
        </p>

        <div className="grid md:grid-cols-3 gap-4 mb-6">
          {tones.map((tone) => (
            <button
              key={tone.value}
              onClick={() => setSelectedTone(tone.value)}
              className={`p-4 rounded-xl border-2 text-left transition-all ${
                selectedTone === tone.value
                  ? 'border-primary-500 bg-primary-500/10'
                  : 'border-zinc-700 hover:border-zinc-600'
              }`}
            >
              <div className="text-2xl mb-2">{tone.emoji}</div>
              <div className="text-white font-medium">{tone.label}</div>
              <div className="text-zinc-500 text-sm">{tone.desc}</div>
            </button>
          ))}
        </div>

        <button
          onClick={handleGenerate}
          disabled={generating}
          className="btn-primary disabled:opacity-50"
        >
          {generating ? (
            <span className="flex items-center gap-2">
              <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                  fill="none"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
              AI가 작성 중...
            </span>
          ) : (
            '🤖 AI 자기소개 생성하기'
          )}
        </button>
      </div>

      {/* Generated Intros */}
      <div>
        <h2 className="text-xl font-semibold text-white mb-4">
          생성된 자기소개 ({intros.length})
        </h2>

        {intros.length === 0 ? (
          <div className="card text-center py-12">
            <div className="text-6xl mb-4">🤖</div>
            <h3 className="text-xl font-semibold text-white mb-2">
              아직 생성된 자기소개가 없습니다
            </h3>
            <p className="text-zinc-400">
              위에서 톤을 선택하고 AI 자기소개를 생성해보세요
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {intros.map((intro) => (
              <div key={intro.id} className="card">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-2">
                    <span className="text-lg">
                      {tones.find((t) => t.value === intro.tone)?.emoji || '📝'}
                    </span>
                    <span className="text-white font-medium">
                      {tones.find((t) => t.value === intro.tone)?.label || intro.tone}
                    </span>
                    <span className="text-zinc-500 text-sm">
                      {new Date(intro.created_at).toLocaleDateString('ko-KR')}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleCopy(intro.content)}
                      className="px-3 py-1 text-zinc-400 hover:text-white hover:bg-zinc-800 rounded-lg transition-colors text-sm"
                    >
                      복사
                    </button>
                    <button
                      onClick={() => handleDelete(intro.id)}
                      className="px-3 py-1 text-zinc-400 hover:text-red-500 hover:bg-zinc-800 rounded-lg transition-colors text-sm"
                    >
                      삭제
                    </button>
                  </div>
                </div>

                <div className="p-4 bg-zinc-800 rounded-xl">
                  <p className="text-zinc-300 whitespace-pre-wrap leading-relaxed">
                    {intro.content}
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
