"""Utility file for JournalEntries"""

def calculate_attachments(att_list, journal_entry_id):
    """Combine attachments and journal entries"""
    return [
        {
            key: value
            for key, value in entry.items()
            if key != "journal_entry_id"
        }
        for entry in list(
            filter(
                lambda att: att["journal_entry_id"] == journal_entry_id,
                att_list,
            )
        )
    ]


def calculate_line_items(lines_list, journal_entry_id):
    "Combine line_items and journal entries"
    return [
        {
            key: value
            for key, value in entry.items()
            if key != "journal_entry_id"
        }
        for entry in list(
            filter(
                lambda line: line["journal_entry_id"] == journal_entry_id,
                lines_list,
            )
        )
    ]
