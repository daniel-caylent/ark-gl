from dataclasses import dataclass
def get(url):
    return Response()

@dataclass
class Response:
    content: str = b"""{
  "journalEntries": [
    {
      "fundId": "e6a9ebc1-59e3-4cd7-b16c-45ae6e0e05ba",
      "clientId": "90b25612-955c-40b6-961a-c15f977d3062",
      "ledgerName": "Unique Ledger Name",
      "date": "2017-01-01",
      "memo": "These charges describe catered lunches.",
      "adjustingJournalEntry": true,
      "reference": "",
      "journalEntryNum": 13455,
      "lineItems": [
        {
          "accountName": "account name-2",
          "memo": "These charges describe catered Pizza.",
          "entityId": "fb84c7c6-9f62-11ed-8cf5-0ed4c7ff8d52",
          "amount": 10012,
          "type": "CREDIT"
        },
        {
          "accountName": "account name",
          "memo": "These charges describe catered Pizza.",
          "entityId": "fb84c7c6-9f62-11ed-8cf5-0ed4c7ff8d52",
          "amount": 10012,
          "type": "DEBIT"
        }
      ]
    }
  ]
}"""
    status_code: int = 200
    