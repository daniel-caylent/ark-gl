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