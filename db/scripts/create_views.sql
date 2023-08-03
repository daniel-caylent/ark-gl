-- TODO: Remove any unused views

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
je.post_date je_post_date,
je.state je_state,
je.date je_date,
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
where acc_att.detail_type = 'Balance Sheet'
-- and le.uuid = ?
-- and account.post_date between ? and ?
group by 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15;

CREATE OR REPLACE VIEW INCOME_STATEMENT_VW AS 
SELECT 
fe.uuid fe_uuid,
fe.client_id, 
acc.uuid acc_uuid,
le.uuid le_uuid,
acc.account_no,
acc_att.account_type,
le.currency,
je.state je_state,
CONCAT(QUARTER(je.date), " ", YEAR(je.date)) as "QUARTER",
sum(case when li.posting_type = 'CREDIT' then li.amount else li.amount*(-1) end) as "TOTAL"
FROM 
line_item li 
inner join journal_entry je on li.journal_entry_id  = je.id
 inner join ledger le on le.id = je.ledger_id  
 inner join fund_entity fe on le.fund_entity_id = fe.id
 inner join account acc on acc.id = li.account_id 
 inner join account_attribute acc_att on acc_att.id = acc.account_attribute_id
where acc_att.detail_type  like ('Income Statement')
-- and fe.client_id = ?
-- and le.uuid = ?
-- and fe.fund_id = ?
-- and account.post_date between ? and ?
group by 1,2,3,4,5,6,7,8,9;

CREATE OR REPLACE VIEW 1099_VW AS
SELECT
fe.uuid fe_uuid,
le.uuid le_uuid,
li.entity_id li_entity_id,
je.post_date je_post_date,
je.state je_state,
je.date je_date,
sum(case when li.posting_type = 'CREDIT' then li.amount else 0 end)+
sum(case when li.posting_type = 'DEBIT' then li.amount*(-1) else 0 end) as "TOTAL"
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

CREATE OR REPLACE VIEW TRIAL_BALANCE_VW AS
SELECT
fe.uuid fe_uuid,
acc.uuid acc_uuid,
acc.name name,
acc.account_no,
concat(acc.name, ' ', acc.account_no) acc_app_name,
le.uuid le_uuid,
je.post_date je_post_date,
je.state je_state,
je.date je_date,
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
group by 1,2,3,4,5,6,7,8,9;

CREATE OR REPLACE VIEW DETAILED_TRIAL_BALANCE_VW AS
SELECT
fe.uuid fund_uuid,
acc.uuid account_uuid,
je.journal_entry_num,
acc.name account_name,
acc.account_no,
acc.is_taxable,
acc.is_entity_required,
acc.post_date account_post_date,
acc.state account_state,
fs.fs_mapping_id,
fs.fs_name,
concat(acc.name, ' ', acc.account_no) account_app_name,
acc_att.uuid attribute_uuid,
acc_att.account_type,
acc_att.detail_type,
li.id line_item_id,
li.line_number,
li.memo,
li.entity_id,
le.uuid ledger_uuid,
le.currency,
le.decimals,
le.name ledger_name,
je.post_date journal_entry_post_date,
je.adjusting_journal_entry,
je.state journal_entry_state,
je.date journal_entry_date,
parent_acc.uuid parent_uuid,
case when li.posting_type = 'CREDIT' then li.amount else li.amount*(-1)  end as "amount"
from 
line_item li 
inner join journal_entry je on li.journal_entry_id  = je.id
 inner join ledger le on le.id = je.ledger_id  
 inner join fund_entity fe on le.fund_entity_id = fe.id
 inner join account acc on acc.id = li.account_id
 left join FS fs on acc.fs_mapping_id = fs.fs_mapping_id
 inner join account_attribute acc_att on acc_att.id = acc.account_attribute_id
 left join account parent_acc on parent_acc.id = acc.parent_id
-- and fe.client_id = ?
-- and le.uuid = ?
-- and fe.fund_id = ?
-- and account.post_date between ? and ?
GROUP BY line_item_id;


CREATE OR REPLACE VIEW DETAILED_1099_VW AS
SELECT
fe.uuid fe_uuid,
le.uuid le_uuid,
je.journal_entry_num,
li.memo,
li.entity_id li_entity_id,
je.post_date je_post_date,
je.adjusting_journal_entry,
je.state je_state,
je.date je_date,
case when li.posting_type = 'CREDIT' then li.amount else li.amount*(-1)  end as "Amount"
from 
line_item li 
inner join journal_entry je on li.journal_entry_id  = je.id
 inner join ledger le on le.id = je.ledger_id  
 inner join fund_entity fe on le.fund_entity_id = fe.id
 inner join account acc on acc.id = li.account_id 
 inner join account_attribute acc_att on acc_att.id = acc.account_attribute_id;
 
CREATE OR REPLACE VIEW BALANCE_FOR_DETAILED_1099_VW AS
SELECT
le.uuid le_uuid,
je.post_date je_post_date,
je.date je_date,
sum(case when li.posting_type = 'CREDIT' then li.amount else li.amount*(-1)  end ) as "TOTAL"
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
 group by 1,2,3;

CREATE OR REPLACE VIEW DETAILED_BALANCE_SHEET_VW AS 
SELECT fe.uuid fund_uuid,
fe.client_id,
acc.uuid acc_uuid,
acc.name,
acc.account_no,
concat(acc.name, ' ', acc.account_no) acc_name,
acc.parent_id,
acc.fs_mapping_id,
le.uuid le_uuid,
le.name le_name,
le.currency,
je.journal_entry_num,
je.adjusting_journal_entry ,
je.post_date je_post_date,
je.state je_state,
je.date je_date,
li.amount 
FROM 
line_item li 
inner join journal_entry je on li.journal_entry_id  = je.id
 inner join ledger le on le.id = je.ledger_id  
 inner join fund_entity fe on le.fund_entity_id = fe.id
 inner join account acc on acc.id = li.account_id;

CREATE OR REPLACE VIEW ARKGL.DETAILED_INCOME_STATEMENT_VW AS 
select 
acc.uuid acc_uuid,
je.`date` date,
le.uuid le_uuid,
le.name  le_name,
je.journal_entry_num,
fe.uuid ,
li.memo,
CONCAT(acc.name, ' ', acc.account_no) acc_name,
case when li.posting_type = 'CREDIT' then li.amount else li.amount*(-1) end as "AMOUNT"
from 
line_item li 
inner join journal_entry je on li.journal_entry_id  = je.id
 inner join ledger le on le.id = je.ledger_id  
 inner join fund_entity fe on le.fund_entity_id = fe.id
 inner join account acc on acc.id = li.account_id 
 inner join account_attribute acc_att on acc_att.id = acc.account_attribute_id
where acc_att.detail_type  like ('Income Statement'); 