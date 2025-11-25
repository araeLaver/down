#!/usr/bin/env python3
"""
business_discovery.html에 점수별 탭 추가
"""

with open('templates/business_discovery.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 탭 HTML 추가
tab_html = '''        </div>

        <!-- Score Tabs -->
        <div style="background: white; border-radius: 12px; margin-bottom: 1.5rem; border: 1px solid var(--border-color); overflow: hidden;">
            <div style="display: flex; border-bottom: 2px solid var(--border-color);">
                <button class="score-tab active" onclick="switchTab('excellent')" id="tab-excellent" style="flex: 1; padding: 1rem 1.5rem; background: white; border: none; cursor: pointer; font-weight: 600; font-size: 0.95rem; color: #6366f1; border-bottom: 3px solid #6366f1; transition: all 0.2s;">
                    <i class="fas fa-trophy"></i> 우수 사업 (80+)
                    <span style="display: inline-block; background: #6366f1; color: white; padding: 0.125rem 0.5rem; border-radius: 12px; font-size: 0.75rem; margin-left: 0.5rem;" id="badge-excellent">0</span>
                </button>
                <button class="score-tab" onclick="switchTab('review')" id="tab-review" style="flex: 1; padding: 1rem 1.5rem; background: white; border: none; cursor: pointer; font-weight: 600; font-size: 0.95rem; color: #6b7280; border-bottom: 3px solid transparent; transition: all 0.2s;">
                    <i class="fas fa-clipboard-check"></i> 검토 필요 (60-79)
                    <span style="display: inline-block; background: #e5e7eb; color: #6b7280; padding: 0.125rem 0.5rem; border-radius: 12px; font-size: 0.75rem; margin-left: 0.5rem;" id="badge-review">0</span>
                </button>
                <button class="score-tab" onclick="switchTab('rejected')" id="tab-rejected" style="flex: 1; padding: 1rem 1.5rem; background: white; border: none; cursor: pointer; font-weight: 600; font-size: 0.95rem; color: #6b7280; border-bottom: 3px solid transparent; transition: all 0.2s;">
                    <i class="fas fa-times-circle"></i> 부적합 (60미만)
                    <span style="display: inline-block; background: #e5e7eb; color: #6b7280; padding: 0.125rem 0.5rem; border-radius: 12px; font-size: 0.75rem; margin-left: 0.5rem;" id="badge-rejected">0</span>
                </button>
            </div>
        </div>

        <!-- Filters -->'''

# Stats 다음에 탭 추가
content = content.replace('        </div>\n\n        <!-- Filters -->', tab_html)

# JavaScript 변수 추가
js_addition = '''        let allBusinesses = [];
        let filteredBusinesses = [];
        let currentFilter = 'all';
        let currentTab = 'excellent'; // 현재 탭

        // 탭 전환
        function switchTab(tab) {
            currentTab = tab;

            // 탭 버튼 스타일 업데이트
            document.querySelectorAll('.score-tab').forEach(btn => {
                btn.style.color = '#6b7280';
                btn.style.borderBottomColor = 'transparent';
                const badge = btn.querySelector('span');
                badge.style.background = '#e5e7eb';
                badge.style.color = '#6b7280';
            });

            const activeTab = document.getElementById(`tab-${tab}`);
            activeTab.style.color = '#6366f1';
            activeTab.style.borderBottomColor = '#6366f1';
            const activeBadge = activeTab.querySelector('span');
            activeBadge.style.background = '#6366f1';
            activeBadge.style.color = 'white';

            // 데이터 로드
            loadBusinessesByTab(tab);
        }

        // 탭별 데이터 로드
        async function loadBusinessesByTab(tab) {
            try {
                document.getElementById('business-list').innerHTML = `
                    <div class="loading-state">
                        <div class="spinner"></div>
                        <p style="color: #6b7280;">사업 아이디어를 불러오는 중...</p>
                    </div>
                `;

                let scoreFilter;
                if (tab === 'excellent') {
                    scoreFilter = '80+'; // API에 맞게 조정 필요
                } else if (tab === 'review') {
                    scoreFilter = '60-79';
                } else {
                    scoreFilter = '60-';
                }

                // business-history API 사용
                const response = await fetch(`/api/business-history/list?score=${scoreFilter}&period=30d&limit=100`);
                const data = await response.json();

                allBusinesses = data.map(item => ({
                    id: item.id,
                    name: item.business_name,
                    type: item.business_type,
                    score: item.total_score,
                    market_score: item.market_score,
                    revenue_score: item.revenue_score,
                    created_at: item.discovered_at,
                    description: `시장 점수: ${item.market_score}/100, 수익 점수: ${item.revenue_score}/100`,
                    revenue_model: item.category,
                    priority: item.saved_to_db ? 'high' : 'medium',
                    feasibility: (item.total_score / 10).toFixed(1),
                    risk: item.total_score >= 80 ? 'low' : item.total_score >= 60 ? 'medium' : 'high',
                    revenue_12m: 0,
                    investment: 0,
                    details: {
                        analysis_score: item.total_score,
                        market_score: item.market_score,
                        revenue_score: item.revenue_score,
                        market_keyword: item.keyword
                    }
                }));

                filteredBusinesses = allBusinesses;

                // 배지 업데이트
                document.getElementById(`badge-${tab}`).textContent = allBusinesses.length;

                // 표시
                displayBusinesses(filteredBusinesses);

                document.getElementById('last-update').textContent =
                    `마지막 업데이트: ${new Date().toLocaleTimeString('ko-KR')}`;

            } catch (error) {
                console.error('Error loading businesses:', error);
                document.getElementById('business-list').innerHTML = `
                    <div class="empty-state">
                        <i class="fas fa-exclamation-triangle"></i>
                        <h4>데이터 로딩 실패</h4>
                        <p>잠시 후 다시 시도해주세요.</p>
                    </div>
                `;
            }
        }

        // 초기 Stats 로드 (모든 탭 개수)
        async function loadStats() {
            try {
                // 각 탭별 개수 로드
                const [excellent, review, rejected] = await Promise.all([
                    fetch('/api/business-history/list?score=80+&period=30d&limit=1000').then(r => r.json()),
                    fetch('/api/business-history/list?score=60-79&period=30d&limit=1000').then(r => r.json()),
                    fetch('/api/business-history/list?score=60-&period=30d&limit=1000').then(r => r.json())
                ]);

                document.getElementById('badge-excellent').textContent = excellent.length;
                document.getElementById('badge-review').textContent = review.length;
                document.getElementById('badge-rejected').textContent = rejected.length;

                document.getElementById('stat-total').textContent = excellent.length + review.length + rejected.length;

                // 오늘/이번주는 API에서 가져오기 (기존 유지)
                const response = await fetch('/api/discovered-businesses');
                const data = await response.json();
                document.getElementById('stat-today').textContent = data.stats.today;
                document.getElementById('stat-week').textContent = data.stats.this_week;
                document.getElementById('stat-highscore').textContent = data.stats.high_score;
            } catch (error) {
                console.error('Error loading stats:', error);
            }
        }

        // Load data'''

# 기존 JavaScript 변수 선언 부분을 새로운 것으로 교체
content = content.replace('''        let allBusinesses = [];
        let filteredBusinesses = [];
        let currentFilter = 'all';

        // Load data''', js_addition)

# 초기 로드 함수 수정
old_load = '''        // Auto refresh every 5 minutes
        setInterval(() => {
            loadBusinesses();
        }, 300000);

        // Initial load
        loadBusinesses();'''

new_load = '''        // Auto refresh every 5 minutes
        setInterval(() => {
            loadStats();
            loadBusinessesByTab(currentTab);
        }, 300000);

        // Initial load
        loadStats();
        loadBusinessesByTab(currentTab);'''

content = content.replace(old_load, new_load)

# 파일 저장
with open('templates/business_discovery.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("[OK] 탭 추가 완료!")
