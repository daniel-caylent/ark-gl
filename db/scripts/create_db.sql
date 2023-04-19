CREATE DATABASE ARKGL;

drop table if exists ARKGL.line_item;
drop table if exists ARKGL.account;
drop table if exists ARKGL.account_attribute;
drop table if exists ARKGL.account_type;

drop table if exists ARKGL.attachment;
drop table if exists ARKGL.journal_entry;
drop table if exists ARKGL.ledger;
drop table if exists ARKGL.fund_entity;



CREATE TABLE IF NOT EXISTS ARKGL.fund_entity (
	id INT AUTO_INCREMENT PRIMARY KEY,
	`uuid` CHAR(36),
	client_id CHAR(36),
	fund_id CHAR(36),
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS ARKGL.ledger  (
	id INT AUTO_INCREMENT PRIMARY KEY,
	`uuid` CHAR(36),
	fund_entity_id INT NOT NULL,
	name VARCHAR(255),
	description VARCHAR(255),
	state VARCHAR(30),
	is_hidden BOOL,
	currency VARCHAR(255),
	`decimal` INT,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (fund_entity_id) REFERENCES fund_entity (id)
);


CREATE TABLE IF NOT EXISTS ARKGL.journal_entry  (
	id INT AUTO_INCREMENT PRIMARY KEY,
	`uuid` CHAR(36),
	ledger_id INT NOT NULL,
	`date` TIMESTAMP,
	reference VARCHAR(255),
	memo VARCHAR(255),
	adjusting_journal_entry BOOL,
	state VARCHAR(30),
	is_hidden BOOL,
	post_date TIMESTAMP,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (ledger_id) REFERENCES ledger (id)
);

CREATE TABLE IF NOT EXISTS ARKGL.account_type (
	id INT AUTO_INCREMENT PRIMARY KEY,
	`uuid` CHAR(36),
	name VARCHAR(255),
	description VARCHAR(255),
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	
);


CREATE TABLE IF NOT EXISTS ARKGL.account_attribute (
	id INT AUTO_INCREMENT PRIMARY KEY,
	`uuid` CHAR(36),
	fund_entity_id INT NOT NULL,
	account_type_id INT NOT NULL,
	detail_type VARCHAR(255),
	description VARCHAR(255),
	state VARCHAR(30),
	is_hidden BOOL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (fund_entity_id) REFERENCES fund_entity(id),
	FOREIGN KEY (account_type_id) REFERENCES account_type(id)
);




CREATE TABLE IF NOT EXISTS ARKGL.account (
	id INT AUTO_INCREMENT PRIMARY KEY,
	account_no INT,
	`uuid` CHAR(36),
	fund_entity_id INT NOT NULL,
	account_attribute_id INT NOT NULL,
	parent_id INT,
	name VARCHAR(255),
	description VARCHAR(255),
	fs_mapping_id VARCHAR(255),
    fs_name VARCHAR(255),
	state VARCHAR(30),
	is_hidden bool,
	is_taxable bool,
	is_vendor_customer_partner_required bool,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (fund_entity_id) REFERENCES fund_entity(id),
	FOREIGN KEY (account_attribute_id) REFERENCES account_attribute(id),
	FOREIGN KEY (parent_id) REFERENCES account(id) 
);

CREATE TABLE IF NOT EXISTS ARKGL.line_item (
	id INT AUTO_INCREMENT PRIMARY KEY,
	`uuid` CHAR(36),
	account_id INT NOT NULL,
	journal_entry_id INT NOT NULL,
	line_number INT,
	memo VARCHAR(255),
	vendor_customer_partner_type VARCHAR(255),
	vendor_customer_partner_id VARCHAR(255),
	posting_type VARCHAR(30),
	amount DOUBLE,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (journal_entry_id) REFERENCES journal_entry(id),
	FOREIGN KEY (account_id) REFERENCES account(id)
);




CREATE TABLE IF NOT EXISTS ARKGL.attachment (
	id INT AUTO_INCREMENT PRIMARY KEY,
	`uuid` CHAR(36),
	journal_entry_id INT NOT NULL,
	location VARCHAR(255),
	memo VARCHAR(255),
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (journal_entry_id) REFERENCES journal_entry(id)
);
