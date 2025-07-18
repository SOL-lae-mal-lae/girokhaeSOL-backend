ALTER TABLE accounts ADD COLUMN is_primary BOOLEAN NOT NULL DEFAULT FALSE;

-- 기존 데이터가 있다면 첫 번째 계좌를 대표계좌로 설정 (선택사항)
UPDATE accounts 
SET is_primary = TRUE 
WHERE id IN (
    SELECT id FROM (
        SELECT id, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY id ASC) as rn
        FROM accounts
    ) ranked 
    WHERE rn = 1
);

-- 인덱스 추가 (성능 향상)
CREATE INDEX idx_accounts_user_primary ON accounts(user_id, is_primary);
