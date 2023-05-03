import requests

from .validate_new_account import validate_new_account

def download_from_s3(signed_s3_url: str) -> str:
    response = requests.get(signed_s3_url)

    return response.content.decode('utf-8')

def convert_csv_to_dicts(csv_str: str) -> list[dict]:
    rows = csv_str.split("\n")

    # Get the header row
    header = rows[0].split(",")

    dict_list = []
    for row in rows[1:]:
        values = row.split(",")
        row_dict = {}

        # Loop through the values and add them to the dictionary
        for i in range(len(values)):
            value = values[i].strip()
            if value == '':
                value = None
            if value == 'N':
                value = False
            if value == 'Y':
                value = True

            row_dict[header[i].strip()] = value
        dict_list.append(row_dict)
  
    return dict_list

def import_account_dicts(accounts, fund_id):
    for account in accounts:
        code, detail, post = validate_new_account(account)

def upload(signed_s3_url, fund_id):
    csv_str = download_from_s3(signed_s3_url)
