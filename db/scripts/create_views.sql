CREATE OR REPLACE VIEW BALANCE_SHEET_VW AS 
SELECT fe.uuid fund_uuid,
fe.client_id,
fe.fund_id,
acc.id acc_id,
acc.uuid acc_uuid,
acc.account_no,
acc.parent_id,
acc.fs_mapping_id,
acc_att.account_type,
le.uuid le_uuid,
le.name le_name,
le.currency,
je.date,
je.state je_state,
sum(case when li.posting_type = 'CREDIT' then li.amount else 0 end) as "CREDIT",
sum(case when li.posting_type = 'DEBIT' then li.amount*(-1) else 0 end) as "DEBIT",
sum(case when li.posting_type = 'CREDIT' then li.amount else 0 end) +
sum(case when li.posting_type = 'DEBIT' then li.amount*(-1) else 0 end) as "TOTAL"
FROM 
line_item li 
inner join journal_entry je on li.journal_entry_id  = je.id
 inner join ledger le on le.id = je.ledger_id  
 inner join fund_entity fe on le.fund_entity_id = fe.id
 inner join account acc on acc.id = li.account_id 
 inner join account_attribute acc_att on acc_att.id = acc.account_attribute_id
-- and le.uuid = ?
-- and account.post_date between ? and ?
group by 1,2,3,4,5,6,7,8,9,10,11,12,13,14;

CREATE OR REPLACE VIEW INCOME_STATEMENT_VW AS 
SELECT fe.uuid fund_uuid,
fe.client_id,
fe.fund_id,
acc.id as acc_id,
acc.uuid acc_uuid,
acc.account_no,
acc.parent_id, 
acc.fs_mapping_id,
acc_att.account_type,
le.uuid le_uuid,
le.name le_name,
le.currency,
li.posting_type,
je.date,
CONCAT(QUARTER(je.date), " ", YEAR(je.date)) as "QUARTER",
sum(li.amount)
FROM 
line_item li 
inner join journal_entry je on li.journal_entry_id  = je.id
 inner join ledger le on le.id = je.ledger_id  
 inner join fund_entity fe on le.fund_entity_id = fe.id
 inner join account acc on acc.id = li.account_id 
 inner join account_attribute acc_att on acc_att.id = acc.account_attribute_id
where acc_att.account_type not in ('Assets', 'Liabilities','Partners Capital')
-- and fe.client_id = ?
-- and le.uuid = ?
-- and fe.fund_id = ?
-- and account.post_date between ? and ?
group by 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15;

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
line_item li 
inner join journal_entry je on li.journal_entry_id  = je.id
 inner join ledger le on le.id = je.ledger_id  
 inner join fund_entity fe on le.fund_entity_id = fe.id
 inner join account acc on acc.id = li.account_id 
 inner join account_attribute acc_att on acc_att.id = acc.account_attribute_id
-- and fe.client_id = ?
-- and le.uuid = ?
-- and fe.fund_id = ?
-- and account.post_date between ? and ?
group by 1,2,3,4,5,6;