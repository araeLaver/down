import { Link } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'

export default function Landing() {
  const { isAuthenticated } = useAuthStore()

  return (
    <div className="min-h-screen bg-zinc-950">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-zinc-950/80 backdrop-blur-lg border-b border-zinc-800">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold text-white">
            렌트<span className="text-primary-500">미</span>
          </h1>
          <div className="flex items-center gap-4">
            {isAuthenticated ? (
              <Link to="/dashboard" className="btn-primary">
                대시보드
              </Link>
            ) : (
              <>
                <Link to="/login" className="text-zinc-400 hover:text-white transition-colors">
                  로그인
                </Link>
                <Link to="/register" className="btn-primary">
                  무료 시작
                </Link>
              </>
            )}
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="pt-32 pb-20 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-block px-4 py-2 bg-primary-500/10 rounded-full text-primary-400 text-sm font-medium mb-6">
            세입자의 LinkedIn
          </div>
          <h2 className="text-5xl md:text-6xl font-bold text-white mb-6 leading-tight">
            신뢰로 증명하는<br />
            <span className="text-primary-500">나의 임차 이력</span>
          </h2>
          <p className="text-xl text-zinc-400 mb-10 max-w-2xl mx-auto">
            이전 집주인의 레퍼런스, 검증된 신원 정보, AI 자기소개로
            집주인에게 신뢰를 전달하세요
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/register" className="btn-primary text-lg px-8 py-4">
              무료로 프로필 만들기
            </Link>
            <a href="#how-it-works" className="btn-secondary text-lg px-8 py-4">
              자세히 알아보기
            </a>
          </div>
        </div>
      </section>

      {/* Problem */}
      <section className="py-20 px-6 bg-zinc-900/50">
        <div className="max-w-6xl mx-auto">
          <h3 className="text-3xl font-bold text-white text-center mb-12">
            이런 경험 있으신가요?
          </h3>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                emoji: '😰',
                title: '매번 새로운 증명',
                desc: '집을 옮길 때마다 처음부터 신뢰를 쌓아야 하는 피로감',
              },
              {
                emoji: '📝',
                title: '복잡한 서류',
                desc: '소득증명, 재직증명, 신분증... 반복되는 서류 준비',
              },
              {
                emoji: '🏠',
                title: '좋은 집 놓침',
                desc: '신뢰 증명이 늦어 원하는 매물을 다른 사람에게 뺏김',
              },
            ].map((item, i) => (
              <div key={i} className="card text-center">
                <div className="text-5xl mb-4">{item.emoji}</div>
                <h4 className="text-xl font-semibold text-white mb-2">{item.title}</h4>
                <p className="text-zinc-400">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section id="how-it-works" className="py-20 px-6">
        <div className="max-w-6xl mx-auto">
          <h3 className="text-3xl font-bold text-white text-center mb-4">
            어떻게 작동하나요?
          </h3>
          <p className="text-zinc-400 text-center mb-12">
            3단계로 신뢰 프로필을 완성하세요
          </p>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                step: '01',
                title: '프로필 작성',
                desc: '기본 정보와 재직/소득 정보를 입력하고 인증받으세요',
              },
              {
                step: '02',
                title: '레퍼런스 수집',
                desc: '이전 집주인에게 레퍼런스를 요청하고 평가를 받으세요',
              },
              {
                step: '03',
                title: 'AI 자기소개',
                desc: 'AI가 당신의 정보를 바탕으로 신뢰감 있는 자기소개를 작성해드려요',
              },
            ].map((item, i) => (
              <div key={i} className="relative">
                <div className="text-7xl font-bold text-primary-500/20 absolute -top-4 -left-2">
                  {item.step}
                </div>
                <div className="relative pt-8 pl-4">
                  <h4 className="text-xl font-semibold text-white mb-2">{item.title}</h4>
                  <p className="text-zinc-400">{item.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Trust Score */}
      <section className="py-20 px-6 bg-zinc-900/50">
        <div className="max-w-4xl mx-auto text-center">
          <h3 className="text-3xl font-bold text-white mb-6">
            신뢰 점수로 한눈에
          </h3>
          <p className="text-zinc-400 mb-10">
            프로필 완성도, 인증 현황, 레퍼런스 평점을 종합한 신뢰 점수로
            집주인에게 어필하세요
          </p>
          <div className="card inline-block">
            <div className="flex items-center gap-8">
              <div className="w-32 h-32 rounded-full border-4 border-primary-500 flex items-center justify-center">
                <div>
                  <div className="text-4xl font-bold text-primary-500">85</div>
                  <div className="text-zinc-500 text-sm">Trust Score</div>
                </div>
              </div>
              <div className="text-left">
                <div className="flex items-center gap-2 mb-2">
                  <span className="w-3 h-3 rounded-full bg-green-500"></span>
                  <span className="text-zinc-300">신원 인증 완료</span>
                </div>
                <div className="flex items-center gap-2 mb-2">
                  <span className="w-3 h-3 rounded-full bg-green-500"></span>
                  <span className="text-zinc-300">재직 확인 완료</span>
                </div>
                <div className="flex items-center gap-2 mb-2">
                  <span className="w-3 h-3 rounded-full bg-green-500"></span>
                  <span className="text-zinc-300">레퍼런스 3건</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full bg-yellow-500"></span>
                  <span className="text-zinc-300">소득 확인 대기</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <h3 className="text-4xl font-bold text-white mb-6">
            지금 바로 시작하세요
          </h3>
          <p className="text-zinc-400 text-xl mb-10">
            무료로 신뢰 프로필을 만들고, 다음 이사를 더 쉽게 준비하세요
          </p>
          <Link to="/register" className="btn-primary text-lg px-10 py-4 inline-block">
            무료 회원가입
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 px-6 border-t border-zinc-800">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="text-zinc-500">
            © 2026 렌트미. All rights reserved.
          </div>
          <div className="flex gap-6 text-zinc-500">
            <a href="#" className="hover:text-white transition-colors">이용약관</a>
            <a href="#" className="hover:text-white transition-colors">개인정보처리방침</a>
            <a href="#" className="hover:text-white transition-colors">문의하기</a>
          </div>
        </div>
      </footer>
    </div>
  )
}
