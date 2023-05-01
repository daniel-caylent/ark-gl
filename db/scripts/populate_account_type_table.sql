INSERT INTO ARKGL.account_attribute 
(uuid, account_type, detail_type, created_at)
VALUES(UUID(), 'Assets', 'Balance Sheet', CURRENT_TIMESTAMP);

INSERT INTO ARKGL.account_attribute
(uuid, account_type, detail_type, created_at)
VALUES(UUID(), 'Liabilities', 'Balance Sheet', CURRENT_TIMESTAMP);

INSERT INTO ARKGL.account_attribute
(uuid, account_type, detail_type, created_at)
VALUES(UUID(), 'Partners Capital', 'Balance Sheet', CURRENT_TIMESTAMP);

INSERT INTO ARKGL.account_attribute
(uuid, account_type, detail_type, created_at)
VALUES(UUID(), 'Income', 'Balance Sheet', CURRENT_TIMESTAMP);

INSERT INTO ARKGL.account_attribute
(uuid, account_type, detail_type, created_at)
VALUES(UUID(), 'Expense', 'Balance Sheet', CURRENT_TIMESTAMP);

INSERT INTO ARKGL.account_attribute
(uuid, account_type, detail_type, created_at)
VALUES(UUID(), 'Gain/Loss', 'Balance Sheet', CURRENT_TIMESTAMP);