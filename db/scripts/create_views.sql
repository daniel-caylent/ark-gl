CREATE OR REPLACE VIEW BALANCE_SHEET_VW AS 
SELECT fe.uuid fund_uuid,
fe.client_id,
fe.fund_id,
acc.uuid acc_uuid,
acc.account_no,
acc.parent_id,
acc.fs_mapping_id,
acc_att.account_type,
le.uuid le_uuid,
le.name le_name,
le.currency,
li.posting_type,
sum(li.amount)
FROM 
fund_entity fe
inner join account acc on fe.id = acc.fund_entity_id
inner join line_item li on li.account_id = acc.id
inner join ledger le on le.fund_entity_id = fe.id
inner join account_attribute acc_att on acc_att.id = account_attribute_id
-- where fe.client_id = ?
-- and le.uuid = ?
-- and account.post_date between ? and ?
group by 1,2,3,4,5,6,7,8,9,10,11,12;

CREATE OR REPLACE VIEW INCOME_STATEMENT_VW AS 
SELECT fe.uuid fund_uuid,
fe.client_id,
fe.fund_id,
acc.uuid acc_uuid,
acc.account_no,
acc.parent_id, 
acc.fs_mapping_id,
acc_att.account_type,
le.uuid le_uuid,
le.name le_name,
le.currency,
li.posting_type,
sum(li.amount)
FROM 
fund_entity fe
inner join account acc on fe.id = acc.fund_entity_id
inner join line_item li on li.account_id = acc.id
inner join ledger le on le.fund_entity_id = fe.id
inner join account_attribute acc_att on acc_att.id = account_attribute_id
where acc_att.account_type not in ('Assets', 'Liabilities','Partners Capital')
-- and fe.client_id = ?
-- and le.uuid = ?
-- and fe.fund_id = ?
-- and account.post_date between ? and ?
group by 1,2,3,4,5,6,7,8,9,10,11,12;

CREATE OR REPLACE VIEW TRIAL_BALANCE_VW AS
SELECT
fe.uuid fe_uuid,
acc.uuid acc_uuid,
acc.name name,
le.uuid le_uuid,
je.date je_date,
je.state je_state,
sum(case when li.posting_type = 'CREDIT' then li.amount else 0 end) as "CREDIT",
sum(case when li.posting_type = 'DEBIT' then li.amount else 0 end) as "DEBIT"
from 
fund_entity fe
inner join account acc on fe.id = acc.fund_entity_id
inner join line_item li on li.account_id = acc.id
inner join ledger le on le.fund_entity_id = fe.id
inner join account_attribute acc_att on acc_att.id = account_attribute_id
inner join journal_entry je on le.id = je.ledger_id
-- and fe.client_id = ?
-- and le.uuid = ?
-- and fe.fund_id = ?
-- and account.post_date between ? and ?
group by 1,2,3,4,5,6;