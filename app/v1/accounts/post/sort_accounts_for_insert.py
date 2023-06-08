"""Sorting for Accounts POST"""

def sort_accounts_for_insert(
    source_accounts: list[dict],
    parent_id_field="parentAccountId",
    child_id_field="accountId",
) -> list[dict]:
    """
    Sort accounts into an order where children are inserted
    immedietly after their parent
    """
    parent_child_dict = {}
    for account in source_accounts:
        parent_id = account.get(parent_id_field)

        if parent_id not in parent_child_dict:
            parent_child_dict[parent_id] = []

        parent_child_dict[parent_id].append(account)

    def build_sorted_list(parent_id):
        sorted_list = []
        child_items = parent_child_dict.get(parent_id, [])
        for child_item in child_items:
            sorted_list.append(child_item)
            sorted_list += build_sorted_list(child_item.get(child_id_field))
        return sorted_list

    return build_sorted_list(None)
