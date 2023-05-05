from dataclasses import dataclass
def get(url):
    return CsvResponse()

@dataclass
class CsvResponse:
    content: str = b"""accountNo,parentAccountNo,accountName,accountDescription,accountType,fsMappingId,fsName,arkTransaction,isTaxable,isEntityRequired
1010000,,Cash & Cash Equivalents,description,Assets,2882beed-33f0-47a0-a3f2-aa935ff937f4,Do Not Map,,N,N
1010100,,Cash & Cash Equivalents-child,description,Assets,2882beed-33f0-47a0-a3f2-aa935ff937f4,Do Not Map,,N,N
1010200,,Cash Money Market,description,Assets,2882beed-33f0-47a0-a3f2-aa935ff937f4,Do Not Map,,N,N
1010300,,Restricted Cash,description,Assets,2882beed-33f0-47a0-a3f2-aa935ff937f4,Do Not Map,,N,N
1020000,,Accounts Receivable,description,Assets,2882beed-33f0-47a0-a3f2-aa935ff937f4,Do Not Map,,N,N
1020100,,Due From Portfolio Company,description,Assets,2882beed-33f0-47a0-a3f2-aa935ff937f4,Do Not Map,,N,N"""
    status_code: int = 200
    