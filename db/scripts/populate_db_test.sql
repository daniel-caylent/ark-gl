INSERT INTO ARKGL.fund_entity (uuid, client_id, fund_id)
		VALUES
			('d4b26dc7-e51a-11ed-aede-0247c1ed2eeb',UUID(),'d4b26dc7-e51a-11ed-aede-0247c1ed2eeb');

INSERT INTO ARKGL.account_type  (uuid, name, description)
		VALUES(UUID(), 'my account type', 'my account type description');
		
INSERT INTO ARKGL.account_attribute 
(uuid, fund_entity_id, account_type_id, detail_type, description, state, is_hidden)
		VALUES (UUID(),1,1,'account detail type', 'account attribute description', 'OK', False);
	
INSERT INTO ARKGL.account 
            (uuid, account_no, fund_entity_id, account_attribute_id, parent_id, name, description,
            state, is_hidden, is_taxable, is_vendor_customer_partner_required)
        VALUES
            (UUID(), '1234', 1, 1, NULL, 'account name', 'account description',
            'account state', False, True, True);
           
INSERT INTO ARKGL.ledger
            (uuid, fund_entity_id, name, description, state, is_hidden, currency,  `decimal`)
        VALUES
            (UUID(), 1, 'ledger nam', 'ledge description', 'ok', False,
            'USD', 3);
            
			
INSERT INTO ARKGL.journal_entry (uuid, ledger_id, date, reference, memo, adjusting_journal_entry, state, is_hidden,post_date)
		VALUES
			(UUID(), 1, CURDATE(), 'journal reference', 'journal memo', 1, 'OK', FALSE, CURDATE());

INSERT INTO ARKGL.line_item (uuid, account_id,journal_entry_id, line_number, memo, vendor_customer_partner_type,vendor_customer_partner_id,posting_type,amount)
		VALUES
			(UUID(), 1,1,1,'entry memo','vendor type', 'vendor id', 'credit', 3000);

INSERT INTO ARKGL.attachment (uuid, journal_entry_id, location, memo)
		VALUES 
			(UUID(),1, 'attachment location', 'attachment memo');