-- 입주해(Ipjuhae) 초기 DB 테이블 생성 SQL
-- PostgreSQL 기준

-- 1. 사용자 테이블
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    user_type VARCHAR(20) NOT NULL, -- 'TENANT' or 'LANDLORD'
    trust_score INTEGER DEFAULT 0,
    trust_grade VARCHAR(20) DEFAULT 'Bronze',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. 스크래핑 데이터 테이블 (암호화 필드는 애플리케이션 레벨에서 처리 권장)
CREATE TABLE IF NOT EXISTS scrap_data (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    income_annual BIGINT DEFAULT 0,
    job_type VARCHAR(50),
    employment_months INTEGER DEFAULT 0,
    credit_rating INTEGER DEFAULT 0,
    is_authenticated BOOLEAN DEFAULT FALSE,
    last_scraped_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. 임대인 평판(레퍼런스) 테이블
CREATE TABLE IF NOT EXISTS tenant_references (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES users(id) ON DELETE CASCADE,
    landlord_id UUID REFERENCES users(id) ON DELETE SET NULL,
    rent_punctuality INTEGER CHECK (rent_punctuality BETWEEN 1 AND 5),
    facility_care INTEGER CHECK (facility_care BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
