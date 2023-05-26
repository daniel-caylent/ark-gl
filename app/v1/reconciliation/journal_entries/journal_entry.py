from ark_qldb import qldb
from arkdb import journal_entries


def handler(event, context) -> tuple[int, dict]:
    journal_uuids = event["uuids"]

    driver = qldb.Driver("ARKGL", region_name="us-east-1")
    buffered_cursor = driver.read_documents(
        "journal_entry", "uuid IN (" + journal_uuids.split(",") + ")"
    )
    processed_list = []
    processed_succesfully = []
    processed_failure = []

    for current_row in buffered_cursor:
        processed_success = True
        current_uuid = current_row["uuid"]

        aurora_record = journal_entries.select_by_id(current_uuid)
        if aurora_record is None:
            print(
                "Error"
            )  # record exists in QLDB and not in Aurora. Someone deleted it
            processed_success = False
        else:
            for current_key in current_row.keys():
                if current_key == "line_items":
                    continue
                if aurora_record.get(current_key) is None:
                    print(
                        "Key " + current_key + " does not exist in Aurora "
                    )  # key does not exist in Aurora
                    processed_success = False
                else:
                    if aurora_record[current_key] != current_row[current_key]:
                        print(
                            "Error on value for key " + current_key
                        )  # record value mistmatch. Someone tampered with the DB
                        processed_success = False

            id = current_row.get("id")
            qldb_line_records = current_row.get("line_items")

            for line_item in qldb_line_records:
                line_number = line_item.get("lineItemNo")
                aurora_line_record = journal_entries.select_line_by_number_journal(
                    line_number, id
                )
                if aurora_line_record is None:
                    print(
                        "Error"
                    )  # record exists in QLDB and not in Aurora. Someone deleted it
                    processed_success = False
                else:
                    for line_current_key in line_item.keys():
                        if line_current_key == "line_items":
                            continue
                        if aurora_line_record.get(line_current_key) is None:
                            print(
                                "Key " + line_current_key + " does not exist in Aurora "
                            )  # key does not exist in Aurora
                            processed_success = False
                        else:
                            if (
                                aurora_line_record[line_current_key]
                                != line_item[line_current_key]
                            ):
                                print(
                                    "Error on value for key " + line_current_key
                                )  # record value mistmatch. Someone tampered with the DB
                                processed_success = False

        processed_list.append(current_row)
        if processed_success:
            processed_succesfully.append(current_row)
        else:
            processed_failure.append(current_row)

    journal_count = journal_entries.select_count_commited_journals()
    if journal_count["count(*)"] != len(processed_list):
        print(
            "Error on amount of records on Aurora "
            + str(journal_count["count(*)"])
            + " vs QLDB "
            + str(len(processed_list))
        )  # distinct amount of journals in the QLDB than the DB

    return 200, {}