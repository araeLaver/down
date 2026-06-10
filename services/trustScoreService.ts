/**
 * 입주해(Ipjuhae) Trust Score 계산 서비스
 * 
 * [가중치]
 * 1. 경제적 신용 (40%): 연소득(20) + 재직기간(20)
 * 2. 금융 신뢰도 (30%): 신용점수
 * 3. 주거 평판 (20%): 이전 임대인 리뷰 평균
 * 4. 인증 가점 (10%): 본인인증 여부
 */

export const calculateTrustScore = (data) => {
    let score = 0;

    // 1. 경제적 신용 (Max 40)
    // 연소득 4,000만원 이상 시 만점(20), 이하는 비례
    const incomeScore = Math.min(20, (data.incomeAnnual / 40000000) * 20);
    // 재직 24개월 이상 시 만점(20), 이하는 비례
    const employmentScore = Math.min(20, (data.employmentMonths / 24) * 20);
    score += (incomeScore + employmentScore);

    // 2. 금융 신뢰도 (Max 30)
    // 신용점수 1000점 기준 비례 배분
    const creditScore = (data.creditRating / 1000) * 30;
    score += creditScore;

    // 3. 주거 평판 (Max 20)
    // 평점 5점 만점 기준 비례 배분 (데이터 없을 시 기본 10점)
    if (data.referenceAvg && data.referenceAvg > 0) {
        score += (data.referenceAvg / 5) * 20;
    } else {
        score += 10;
    }

    // 4. 인증 가점 (Max 10)
    if (data.isAuthenticated) {
        score += 10;
    }

    const finalScore = Math.round(score);
    
    // 등급 판정
    let grade = 'Bronze';
    if (finalScore >= 90) grade = 'Platinum';
    else if (finalScore >= 80) grade = 'Gold';
    else if (finalScore >= 70) grade = 'Silver';

    return {
        score: finalScore,
        grade: grade
    };
};
