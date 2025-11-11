#!/usr/bin/env python3
"""
business_discovery.html에 네비게이션 메뉴 추가
"""

# 파일 읽기
with open('templates/business_discovery.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 네비게이션 HTML
nav_html = '''
        <!-- Navigation Menu -->
        <div style="margin-bottom: 1.5rem;">
            <a href="/business-discovery" style="display: inline-block; padding: 0.5rem 1rem; background: #6366f1; color: white; text-decoration: none; border-radius: 8px; margin-right: 0.5rem; border: 1px solid #6366f1; transition: all 0.2s;">
                <i class="fas fa-trophy"></i> 우수 사업 (80+)
            </a>
            <a href="/business-review" style="display: inline-block; padding: 0.5rem 1rem; background: white; color: #6b7280; text-decoration: none; border-radius: 8px; margin-right: 0.5rem; border: 1px solid var(--border-color); transition: all 0.2s;">
                <i class="fas fa-clipboard-check"></i> 검토 필요 (60-79)
            </a>
            <a href="/business-rejected" style="display: inline-block; padding: 0.5rem 1rem; background: white; color: #6b7280; text-decoration: none; border-radius: 8px; margin-right: 0.5rem; border: 1px solid var(--border-color); transition: all 0.2s;">
                <i class="fas fa-times-circle"></i> 부적합 (60 미만)
            </a>
        </div>

'''

# <!-- Filters --> 주석을 찾아서 그 앞에 네비게이션 삽입
new_lines = []
for i, line in enumerate(lines):
    if '<!-- Filters -->' in line:
        # 이 줄 앞에 네비게이션 추가
        new_lines.append(nav_html)
    new_lines.append(line)

# 파일 쓰기
with open('templates/business_discovery.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("✅ 네비게이션 메뉴 추가 완료!")
