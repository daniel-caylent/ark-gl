def select_by_fund_id(fund_id):
    return [
    {
      "fundId": "17d67c61-e9de-11ed-9a6e-0a3efd619f29",
      "glName": "ledger nam",
      "glDescription": "ledger description",
      "ledgerId": "a762d273-eaa5-11ed-9a6e-0a3efd619f29",
      "state": "ok",
      "currencyName": "USD",
      "currencyDecimal": 3,
      "isHidden": False,
      "postDate": None
    },
    {
      "fundId": "17d67c61-e9de-11ed-9a6e-0a3efd619f29",
      "glName": "duplicate",
      "glDescription": "ledger description",
      "ledgerId": "b2122123-eaa5-11ed-9a6e-0a3efd619f29",
      "state": "ok",
      "currencyName": "USD",
      "currencyDecimal": 3,
      "isHidden": False,
      "postDate": None
    },
    {
      "fundId": "17d67c61-e9de-11ed-9a6e-0a3efd619f29",
      "glName": "ledger nam",
      "glDescription": "ledger description",
      "ledgerId": "b7e84f41-eaa5-11ed-9a6e-0a3efd619f29",
      "state": "ok",
      "currencyName": "USD",
      "currencyDecimal": 3,
      "isHidden": False,
      "postDate": None
    }
  ]

def select_by_client_id(client_id):
    return select_by_fund_id(None)

def select_by_id(id, translate=True):
    if id == "a92bde1e-7825-429d-aaae-909f2d7a8df2":
        return None

    return {
      "fundId": "17d67c61-e9de-11ed-9a6e-0a3efd619f29",
      "glName": "ledger nam",
      "glDescription": "ledger description",
      "ledgerId": "b7e84f41-eaa5-11ed-9a6e-0a3efd619f29",
      "state": "ok",
      "currencyName": "USD",
      "currencyDecimal": 3,
      "isHidden": False,
      "postDate": None
    }

def select_by_fund_and_name(fund, name):
    
    return {
      "fundId": "17d67c61-e9de-11ed-9a6e-0a3efd619f29",
      "glName": "ledger nam",
      "glDescription": "ledger description",
      "ledgerId": "b7e84f41-eaa5-11ed-9a6e-0a3efd619f29",
      "state": "ok",
      "currencyName": "USD",
      "currencyDecimal": 3,
      "isHidden": False,
      "postDate": None
    }

def update_by_id(id, dict):
    return None

def create_new(*args):
    return None

def delete_by_id(*args):
    return None