import datetime

def select_by_fund_id(fund_id):
    return [
    {
      "fundId": "17d67c61-e9de-11ed-9a6e-0a3efd619f29",
      "glName": "ledger nam",
      "glDescription": "ledger description",
      "ledgerId": "a762d273-eaa5-11ed-9a6e-0a3efd619f29",
      "state": "POSTED",
      "currencyName": "USD",
      "currencyDecimal": 3,
      "postDate": None
    },
    {
      "fundId": "17d67c61-e9de-11ed-9a6e-0a3efd619f29",
      "glName": "duplicate",
      "glDescription": "ledger description",
      "ledgerId": "b2122123-eaa5-11ed-9a6e-0a3efd619f29",
      "state": "POSTED",
      "currencyName": "USD",
      "currencyDecimal": 3,
      "postDate": None
    },
    {
      "fundId": "17d67c61-e9de-11ed-9a6e-0a3efd619f29",
      "glName": "ledger nam",
      "glDescription": "ledger description",
      "ledgerId": "b7e84f41-eaa5-11ed-9a6e-0a3efd619f29",
      "state": "POSTED",
      "currencyName": "USD",
      "currencyDecimal": 3,
      "postDate": None
    }
  ]

def select_by_client_id(client_id):
    return select_by_fund_id(None)

def select_by_id(id, translate=True):
    if id == "a92bde1e-7825-429d-aaae-909f2d7a8df2":
        return None
    elif id == "d9bc1a3f-0bb7-11ee-b49c-0a3efd619f29":
        return {
                    "id": 130,
                    "uuid": "d9bc1a3f-0bb7-11ee-b49c-0a3efd619f29",
                    "fund_entity_id": "b5e9488f-24cb-4881-87df-b05f76cbe1b9",
                    "name": "Franco - Parent fdsfdfdas",
                    "description": "Franco parent, sub sub test",
                    "post_date": "2023-06-15 20:04:51",
                    "state": "POSTED",
                    "is_hidden": 0,
                    "currency": "USD",
                    "decimals": 2,
                    "created_at": datetime.datetime.strptime("2023-06-15 20:04:35", "%Y-%m-%d %H:%M:%S")
                }

    if not translate:
        return {
          "fund_entity_id": "17d67c61-e9de-11ed-9a6e-0a3efd619f29",
          "name": "ledger nam",
          "description": "ledger description",
          "uuid": "b7e84f41-eaa5-11ed-9a6e-0a3efd619f29",
          "state": "DRAFT",
          "currency": "USD",
          "decimals": 3,
          "hidden": False,
          "post_date": None
        }
    if id == "p7e84f41-eaa5-11ed-9a6e-0a3efd619f29":
        return {
          "fundId": "17d67c61-e9de-11ed-9a6e-0a3efd619f29",
          "glName": "ledger nam",
          "glDescription": "ledger description",
          "ledgerId": "p7e84f41-eaa5-11ed-9a6e-0a3efd619f29",
          "state": "POSTED",
          "currencyName": "USD",
          "currencyDecimal": 3,
          "postDate": None
        }
        
    return {
      "fundId": "17d67c61-e9de-11ed-9a6e-0a3efd619f29",
      "glName": "ledger nam",
      "glDescription": "ledger description",
      "ledgerId": "b7e84f41-eaa5-11ed-9a6e-0a3efd619f29",
      "state": "DRAFT",
      "currencyName": "USD",
      "currencyDecimal": 3,
      "postDate": None
    }

def select_by_fund_and_name(fund, name, translate=True):
    if translate is False:
        return {
          "id": 1,
          "fund_id": "17d67c61-e9de-11ed-9a6e-0a3efd619f29",
          "name": "ledger nam",
          "decription": "ledger description",
          "uuid": "b7e84f41-eaa5-11ed-9a6e-0a3efd619f29",
          "state": "POSTED",
          "currency": "USD",
          "decimals": 0,
          "postDate": None
        }
        
    if "ZERO" in name:
        return {
          "fundId": "17d67c61-e9de-11ed-9a6e-0a3efd619f29",
          "glName": "ledger nam",
          "glDescription": "ledger description",
          "ledgerId": "b7e84f41-eaa5-11ed-9a6e-0a3efd619f29",
          "state": "POSTED",
          "currencyName": "USD",
          "currencyDecimal": 0,
          "postDate": None
        }
    return {
      "fundId": "17d67c61-e9de-11ed-9a6e-0a3efd619f29",
      "glName": "ledger nam",
      "glDescription": "ledger description",
      "ledgerId": "b7e84f41-eaa5-11ed-9a6e-0a3efd619f29",
      "state": "POSTED",
      "currencyName": "USD",
      "currencyDecimal": 3,
      "postDate": None
    }

def update_by_id(id, dict):
    return None

def create_new(*args):
    return None

def delete_by_id(*args):
    return None

def commit_by_id(*args):
    return None

def bulk_delete(ids_):
    return None

def select_count_commited_ledgers():
    return {"count(*)": 1}