INSERT INTO ARKGL.account_attribute 
(number, uuid, account_type, detail_type, created_at)
VALUES(1,UUID(), 'Assets', 'Balance Sheet', CURRENT_TIMESTAMP);

INSERT INTO ARKGL.account_attribute
(number, uuid, account_type, detail_type, created_at)
VALUES(2,UUID(), 'Liabilities', 'Balance Sheet', CURRENT_TIMESTAMP);

INSERT INTO ARKGL.account_attribute
(number, uuid, account_type, detail_type, created_at)
VALUES(3,UUID(), 'Partners Capital', 'Balance Sheet', CURRENT_TIMESTAMP);

INSERT INTO ARKGL.account_attribute
(number, uuid, account_type, detail_type, created_at)
VALUES(4,UUID(), 'Income', 'Income Statement', CURRENT_TIMESTAMP);

INSERT INTO ARKGL.account_attribute
(number, uuid, account_type, detail_type, created_at)
VALUES(5,UUID(), 'Expense', 'Income Statement', CURRENT_TIMESTAMP);

INSERT INTO ARKGL.account_attribute
(number, uuid, account_type, detail_type, created_at)
VALUES(6,UUID(), 'Gain/Loss', 'Income Statement', CURRENT_TIMESTAMP);