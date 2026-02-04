-- 렌트미 Supabase 데이터베이스 스키마
-- Supabase 대시보드 SQL Editor에서 실행

-- 1. Users 테이블
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    user_type VARCHAR(20) DEFAULT 'tenant', -- tenant | landlord
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Profiles 테이블 (세입자 프로필)
CREATE TABLE IF NOT EXISTS profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE UNIQUE,

    -- 기본 정보
    birth_year INTEGER,
    gender VARCHAR(10), -- male | female | other

    -- 직업 정보
    occupation VARCHAR(100),
    company_name VARCHAR(100),
    employment_type VARCHAR(50), -- 정규직 | 계약직 | 프리랜서 | 학생 | 무직
    work_duration_months INTEGER,

    -- 소득 정보
    monthly_income INTEGER, -- 만원 단위
    income_type VARCHAR(50), -- 급여 | 사업 | 프리랜서 | 기타

    -- 라이프스타일
    has_pet BOOLEAN DEFAULT FALSE,
    pet_type VARCHAR(50),
    is_smoker BOOLEAN DEFAULT FALSE,
    living_alone BOOLEAN DEFAULT TRUE,
    move_in_date VARCHAR(20),

    -- 선호 조건
    preferred_area VARCHAR(100),
    max_deposit INTEGER, -- 만원 단위
    max_monthly_rent INTEGER, -- 만원 단위

    -- 자기소개
    introduction TEXT,
    ai_introduction TEXT,

    -- 인증 상태
    employment_verified VARCHAR(20) DEFAULT 'none', -- none | pending | verified | rejected
    income_verified VARCHAR(20) DEFAULT 'none',
    credit_verified VARCHAR(20) DEFAULT 'none',

    -- 공개 설정
    is_public BOOLEAN DEFAULT FALSE,

    -- 메타
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. References 테이블 (집주인 레퍼런스)
CREATE TABLE IF NOT EXISTS references (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES users(id) ON DELETE CASCADE,

    -- 집주인 정보
    landlord_name VARCHAR(100) NOT NULL,
    landlord_email VARCHAR(255),
    landlord_phone VARCHAR(20),

    -- 임대 정보
    address TEXT NOT NULL,
    rental_start VARCHAR(20) NOT NULL, -- YYYY-MM
    rental_end VARCHAR(20) NOT NULL,
    monthly_rent INTEGER,
    deposit INTEGER,

    -- 평가 (집주인이 작성)
    rating INTEGER, -- 1-5
    payment_punctuality INTEGER, -- 1-5
    property_care INTEGER, -- 1-5
    communication INTEGER, -- 1-5
    would_rent_again BOOLEAN,
    comment TEXT,

    -- 상태
    status VARCHAR(20) DEFAULT 'pending', -- pending | completed | declined | expired
    request_code VARCHAR(20) UNIQUE,

    -- 메타
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

-- 4. 인덱스 생성
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_profiles_user_id ON profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_profiles_is_public ON profiles(is_public);
CREATE INDEX IF NOT EXISTS idx_references_tenant_id ON references(tenant_id);
CREATE INDEX IF NOT EXISTS idx_references_request_code ON references(request_code);
CREATE INDEX IF NOT EXISTS idx_references_status ON references(status);

-- 5. RLS (Row Level Security) 정책
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE references ENABLE ROW LEVEL SECURITY;

-- Users: 본인만 조회/수정 가능
CREATE POLICY "Users can view own data" ON users
    FOR SELECT USING (auth.uid()::text = id::text);

CREATE POLICY "Users can update own data" ON users
    FOR UPDATE USING (auth.uid()::text = id::text);

-- Profiles: 본인 프로필은 모두 가능, 공개 프로필은 누구나 조회 가능
CREATE POLICY "Users can manage own profile" ON profiles
    FOR ALL USING (auth.uid()::text = user_id::text);

CREATE POLICY "Anyone can view public profiles" ON profiles
    FOR SELECT USING (is_public = TRUE);

-- References: 세입자는 본인 레퍼런스 관리, 집주인은 코드로 작성
CREATE POLICY "Tenants can manage own references" ON references
    FOR ALL USING (auth.uid()::text = tenant_id::text);

-- Note: 집주인의 레퍼런스 작성은 백엔드 서비스 키로 처리
