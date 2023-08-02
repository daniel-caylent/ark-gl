CREATE DATABASE ARKGL;

drop table if exists ARKGL.line_item;
drop table if exists ARKGL.account;
drop table if exists ARKGL.account_attribute;

drop table if exists ARKGL.attachment;
drop table if exists ARKGL.journal_entry;
drop table if exists ARKGL.ledger;
drop table if exists ARKGL.fund_entity;

drop table if exists ARKGL.FS;

CREATE TABLE IF NOT EXISTS ARKGL.fund_entity (
	id INT AUTO_INCREMENT PRIMARY KEY,
	`uuid` CHAR(36) UNIQUE,
	client_id CHAR(36),
	fund_id CHAR(36),
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS ARKGL.ledger  (
	id INT AUTO_INCREMENT PRIMARY KEY,
	`uuid` CHAR(36),
	fund_entity_id INT NOT NULL,
	name VARCHAR(256),
	description VARCHAR(256),
	state VARCHAR(30),
	currency VARCHAR(256),
	decimals INT,
	post_date TIMESTAMP,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (fund_entity_id) REFERENCES fund_entity (id)
);


CREATE TABLE IF NOT EXISTS ARKGL.journal_entry  (
	id INT AUTO_INCREMENT PRIMARY KEY,
	journal_entry_num INT,
	`uuid` CHAR(36),
	ledger_id INT NOT NULL,
	`date` date,
	reference VARCHAR(256),
	memo VARCHAR(256),
	adjusting_journal_entry BOOL,
	state VARCHAR(30),
	post_date TIMESTAMP,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (ledger_id) REFERENCES ledger (id),
	CONSTRAINT unique_no_and_ledger_id UNIQUE (journal_entry_num, ledger_id)
);



CREATE TABLE IF NOT EXISTS ARKGL.account_attribute (
	id INT AUTO_INCREMENT PRIMARY KEY,
	number int,
	`uuid` CHAR(36),
	account_type VARCHAR(256),
	detail_type VARCHAR(256),
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);




CREATE TABLE IF NOT EXISTS ARKGL.account (
	id INT AUTO_INCREMENT PRIMARY KEY,
	account_no VARCHAR(10),
	`uuid` CHAR(36),
	fund_entity_id INT NOT NULL,
	account_attribute_id INT NOT NULL,
	parent_id INT,
	name VARCHAR(256),
	description VARCHAR(256),
	fs_mapping_id CHAR(36),
	fs_mapping_status VARCHAR(15),
	state VARCHAR(30),
	is_taxable bool,
	is_entity_required bool,
	post_date TIMESTAMP,
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
	memo VARCHAR(256),
    entity_id CHAR(36),	
	posting_type VARCHAR(30),
	amount BIGINT,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (journal_entry_id) REFERENCES journal_entry(id),
	FOREIGN KEY (account_id) REFERENCES account(id)
);




CREATE TABLE IF NOT EXISTS ARKGL.attachment (
	id INT AUTO_INCREMENT PRIMARY KEY,
	`uuid` CHAR(36),
	journal_entry_id INT NOT NULL,
	memo VARCHAR(256),
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (journal_entry_id) REFERENCES journal_entry(id)
);

CREATE TABLE IF NOT EXISTS ARKGL.FS (
	fs_mapping_id CHAR(36) PRIMARY KEY,
	fs_name VARCHAR(256),
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);