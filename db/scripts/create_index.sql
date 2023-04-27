CREATE INDEX line_item_uuid_idx ON ARKGL.line_item(uuid);
CREATE INDEX account_uuid_idx ON ARKGL.account(uuid);
CREATE INDEX account_accountno_idx ON ARKGL.account(account_no);
CREATE INDEX account_attribute_uuid_idx ON ARKGL.account_attribute(uuid);
CREATE INDEX account_type_uuid_idx ON ARKGL.account_type(uuid);

CREATE INDEX attachment_uuid_idx ON ARKGL.attachment(uuid);
CREATE INDEX journal_entry_uuid_idx ON ARKGL.journal_entry(uuid);
CREATE INDEX ledger_uuid_idx ON ARKGL.ledger(uuid);
CREATE INDEX fund_entity_uuid_idx ON ARKGL.fund_entity(uuid);