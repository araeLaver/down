"""
1인 창업/스타트업 지원 정책 크롤러
- K-Startup, 중소벤처기업부, 창업진흥원 등 주요 지원사업 수집
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time


class StartupSupportCrawler:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def get_k_startup_programs(self):
        """K-Startup 지원사업 정보"""
        programs = [
            {
                'name': '예비창업패키지',
                'organization': '창업진흥원',
                'target': '3년 이내 예비창업자',
                'support_amount': '최대 1억원',
                'support_type': '사업화 자금',
                'application_period': '연 2회 (상반기/하반기)',
                'website': 'https://www.k-startup.go.kr',
                'description': '사업화 자금, 멘토링, 창업교육 등 종합 지원',
                'requirements': [
                    '만 39세 이하 (일부 예외)',
                    '사업자등록 3년 이내',
                    '기술성, 사업성 평가 통과'
                ],
                'category': '창업 초기'
            },
            {
                'name': '초기창업패키지',
                'organization': '창업진흥원',
                'target': '3년~7년 창업기업',
                'support_amount': '최대 1억원',
                'support_type': '사업화 자금',
                'application_period': '연 2회',
                'website': 'https://www.k-startup.go.kr',
                'description': '제품/서비스 고도화, 마케팅 지원',
                'requirements': [
                    '사업자등록 3년~7년',
                    '업력 대비 성장 가능성',
                    '시제품 개발 완료'
                ],
                'category': '성장 단계'
            },
            {
                'name': '청년창업사관학교',
                'organization': '중소벤처기업부',
                'target': '만 39세 이하 예비/초기창업자',
                'support_amount': '1억원 내외',
                'support_type': '공간, 자금, 멘토링',
                'application_period': '연 1회',
                'website': 'https://www.k-startup.go.kr',
                'description': '1년간 전문 보육 및 사업화 지원',
                'requirements': [
                    '만 39세 이하',
                    '3개월 이상 전일제 입교 가능',
                    '팀 구성 필수 (1인 불가)'
                ],
                'category': '창업 초기'
            },
            {
                'name': 'TIPS 프로그램',
                'organization': '중소벤처기업부',
                'target': '기술창업 기업',
                'support_amount': '최대 5억원',
                'support_type': '기술개발 자금, 투자 연계',
                'application_period': '상시',
                'website': 'https://www.tips.or.kr',
                'description': '민간 투자사 주도 기술창업 지원',
                'requirements': [
                    '혁신적 기술 보유',
                    'TIPS 운영사 추천',
                    '민간 투자 유치 가능성'
                ],
                'category': '기술창업'
            },
            {
                'name': '1인 창조기업 지원센터',
                'organization': '소상공인시장진흥공단',
                'target': '1인 창업자',
                'support_amount': '무료',
                'support_type': '공간, 교육, 컨설팅',
                'application_period': '상시',
                'website': 'https://www.semas.or.kr',
                'description': '전국 150개 센터에서 1인 창업 지원',
                'requirements': [
                    '1인 사업자',
                    '예비창업자 포함',
                    '지역별 센터 신청'
                ],
                'category': '1인 창업'
            }
        ]
        return programs

    def get_regional_support(self):
        """지역별 창업 지원사업"""
        regional = [
            {
                'name': '서울시 청년창업센터',
                'region': '서울',
                'organization': '서울산업진흥원',
                'support_amount': '최대 5천만원',
                'support_type': '공간, 자금, 멘토링',
                'website': 'https://sba.seoul.kr',
                'description': '서울 소재 청년 창업자 종합 지원',
                'category': '지역 특화'
            },
            {
                'name': '경기도 청년 창업지원',
                'region': '경기',
                'organization': '경기도',
                'support_amount': '최대 3천만원',
                'support_type': '사업화 자금',
                'website': 'https://www.gg.go.kr',
                'description': '경기도 청년 창업자 사업화 지원',
                'category': '지역 특화'
            },
            {
                'name': '부산 창업지원센터',
                'region': '부산',
                'organization': '부산테크노파크',
                'support_amount': '최대 5천만원',
                'support_type': '공간, 자금',
                'website': 'https://www.btp.or.kr',
                'description': '부산 지역 창업자 인큐베이팅',
                'category': '지역 특화'
            }
        ]
        return regional

    def get_tech_support(self):
        """기술/IT 분야 특화 지원"""
        tech = [
            {
                'name': 'ICT 이노베이션스퀘어',
                'organization': '정보통신산업진흥원',
                'target': 'ICT 창업자',
                'support_amount': '무료',
                'support_type': '공간, 멘토링, 네트워킹',
                'website': 'https://www.nipa.kr',
                'description': 'ICT 분야 창업자 전용 공간 및 교육',
                'category': 'IT/기술'
            },
            {
                'name': 'SW마에스트로',
                'organization': '과학기술정보통신부',
                'target': '만 34세 이하 SW인재',
                'support_amount': '월 100만원 + 프로젝트 비용',
                'support_type': '연수비, 개발비',
                'website': 'https://www.swmaestro.org',
                'description': '고급 SW인재 양성 및 창업 연계',
                'requirements': [
                    '만 34세 이하',
                    'SW 개발 능력',
                    '1년 전일제 과정'
                ],
                'category': 'IT/기술'
            },
            {
                'name': 'AI 바우처 지원사업',
                'organization': '정보통신산업진흥원',
                'target': 'AI 활용 기업',
                'support_amount': '최대 7천만원',
                'support_type': 'AI 개발비',
                'website': 'https://www.ai-korea.kr',
                'description': 'AI 기술 개발 및 적용 지원',
                'category': 'IT/기술'
            }
        ]
        return tech

    def get_funding_support(self):
        """투자/융자 지원"""
        funding = [
            {
                'name': '청년창업특별자금',
                'organization': '중소벤처기업진흥공단',
                'target': '만 39세 이하 창업자',
                'support_amount': '최대 1억원',
                'support_type': '저금리 융자 (2%대)',
                'application_period': '상시',
                'website': 'https://www.kosmes.or.kr',
                'description': '청년 창업자 운영자금 저금리 대출',
                'category': '융자'
            },
            {
                'name': '모태펀드 투자',
                'organization': '중소벤처기업진흥공단',
                'target': '스타트업',
                'support_amount': '기업당 상이',
                'support_type': '투자',
                'website': 'https://www.kvic.or.kr',
                'description': '정책펀드를 통한 초기 투자 지원',
                'category': '투자'
            },
            {
                'name': '신용보증 지원',
                'organization': '신용보증기금',
                'target': '창업 7년 이내',
                'support_amount': '최대 30억원',
                'support_type': '보증',
                'website': 'https://www.kodit.co.kr',
                'description': '담보 부족 창업자 신용보증',
                'category': '보증'
            }
        ]
        return funding

    def get_tax_benefits(self):
        """세제/경영 지원"""
        benefits = [
            {
                'name': '창업중소기업 세액감면',
                'organization': '국세청',
                'target': '창업 5년 이내 중소기업',
                'support_amount': '소득세/법인세 50~100% 감면',
                'support_type': '세제 혜택',
                'description': '수도권 외 창업 시 5년간 세액 100% 감면',
                'requirements': [
                    '창업 5년 이내',
                    '중소기업',
                    '업종 제한 있음'
                ],
                'category': '세제 혜택'
            },
            {
                'name': '4대보험 지원',
                'organization': '고용노동부',
                'target': '5인 미만 소상공인',
                'support_amount': '두루누리 최대 80% 지원',
                'support_type': '사회보험료 지원',
                'description': '소상공인 4대보험료 부담 경감',
                'category': '사회보험'
            },
            {
                'name': '벤처기업 인증',
                'organization': '벤처확인기관',
                'target': '기술력 보유 기업',
                'support_amount': '무료',
                'support_type': '인증',
                'description': '세제, 금융, 입지 등 다양한 혜택',
                'benefits': [
                    '세액 감면',
                    '정책자금 우대',
                    '병역특례 가능',
                    '규제 샌드박스'
                ],
                'category': '인증'
            }
        ]
        return benefits

    def get_all_support_programs(self):
        """모든 지원사업 통합 조회"""
        all_programs = {
            'startup_packages': self.get_k_startup_programs(),
            'regional_support': self.get_regional_support(),
            'tech_support': self.get_tech_support(),
            'funding': self.get_funding_support(),
            'tax_benefits': self.get_tax_benefits(),
            'last_updated': datetime.now().isoformat()
        }

        # 통계 추가
        total_count = sum([
            len(all_programs['startup_packages']),
            len(all_programs['regional_support']),
            len(all_programs['tech_support']),
            len(all_programs['funding']),
            len(all_programs['tax_benefits'])
        ])

        all_programs['statistics'] = {
            'total_programs': total_count,
            'by_category': {
                'startup_packages': len(all_programs['startup_packages']),
                'regional_support': len(all_programs['regional_support']),
                'tech_support': len(all_programs['tech_support']),
                'funding': len(all_programs['funding']),
                'tax_benefits': len(all_programs['tax_benefits'])
            }
        }

        return all_programs

    def search_programs(self, keyword=None, category=None, max_amount=None):
        """지원사업 검색"""
        all_programs = self.get_all_support_programs()
        results = []

        # 모든 프로그램을 하나의 리스트로
        for program_type, programs in all_programs.items():
            if program_type in ['statistics', 'last_updated']:
                continue
            for program in programs:
                program['program_type'] = program_type
                results.append(program)

        # 필터링
        if keyword:
            keyword = keyword.lower()
            results = [
                p for p in results
                if keyword in p.get('name', '').lower()
                or keyword in p.get('description', '').lower()
                or keyword in p.get('target', '').lower()
            ]

        if category:
            results = [p for p in results if p.get('category') == category]

        return {
            'results': results,
            'count': len(results),
            'search_params': {
                'keyword': keyword,
                'category': category,
                'max_amount': max_amount
            }
        }

    def get_recommended_programs(self, user_profile):
        """사용자 프로필에 맞는 추천 지원사업"""
        age = user_profile.get('age', 30)
        business_age = user_profile.get('business_age', 0)  # 0: 예비창업
        industry = user_profile.get('industry', 'IT')
        region = user_profile.get('region', '서울')

        recommendations = []
        all_programs = self.get_all_support_programs()

        # 나이 기준 필터링
        if age <= 39:
            recommendations.extend([
                p for p in all_programs['startup_packages']
                if '39세 이하' in p.get('target', '')
            ])

        # 업력 기준 필터링
        if business_age < 3:
            recommendations.extend([
                p for p in all_programs['startup_packages']
                if '예비' in p.get('target', '') or '3년 이내' in p.get('target', '')
            ])

        # IT/기술 분야
        if industry in ['IT', '기술', 'SW']:
            recommendations.extend(all_programs['tech_support'])

        # 지역 기반
        regional = [
            p for p in all_programs['regional_support']
            if p.get('region') == region
        ]
        recommendations.extend(regional)

        # 중복 제거
        unique_recommendations = []
        seen = set()
        for rec in recommendations:
            if rec['name'] not in seen:
                unique_recommendations.append(rec)
                seen.add(rec['name'])

        return {
            'recommendations': unique_recommendations,
            'count': len(unique_recommendations),
            'user_profile': user_profile
        }


if __name__ == '__main__':
    crawler = StartupSupportCrawler()

    # 전체 조회
    all_programs = crawler.get_all_support_programs()
    print(f"[INFO] 전체 지원사업: {all_programs['statistics']['total_programs']}개")

    # 1인 창업자 추천
    profile = {
        'age': 32,
        'business_age': 0,  # 예비창업
        'industry': 'IT',
        'region': '서울'
    }

    recommended = crawler.get_recommended_programs(profile)
    print(f"\n[RECOMMEND] 추천 지원사업: {recommended['count']}개")
    for rec in recommended['recommendations'][:5]:
        print(f"  - {rec['name']} ({rec['organization']})")
