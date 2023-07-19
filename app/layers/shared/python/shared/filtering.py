from dataclasses import dataclass

from .dataclass_validators import validate_date, validate_list, validate_str, check_uuid

@dataclass
class FilterInput:
    startDate: str = None
    endDate: str = None
    clientId: str = None
    fundId: str = None
    journalEntryState: str = None
    accountIds: list = None
    ledgerIds: list = None
    entityIds: list = None
    fundIds: list = None

    # Control fields that dictates if serialization is necessary,
    # this one is not returned in the get_dict method
    parse: bool = False

    def __post_init__(self):
        self.startDate = (
            None if self.startDate is None else
            validate_date(self.startDate, "startDate")
        )
        self.endDate = (
            None if self.endDate is None else
            validate_date(self.endDate, "endDate")
        )
        self.clientId = (
            None if self.clientId is None else
            check_uuid(self.clientId, "clientId")
        )
        self.fundId = (
            None if self.fundId is None else
            check_uuid(self.fundId, "fundId")
        )
        self.journalEntryState = (
            None if self.journalEntryState is None else
            validate_str(self.journalEntryState, "journalEntryState", allowed=["DRAFT"])
        )
        self.accountIds = (
            None if self.accountIds is None else
            validate_list(self.accountIds, "accountIds", min_len=1, parse=self.parse)
        )
        self.ledgerIds = (
            None if self.ledgerIds is None else
            validate_list(self.ledgerIds, "ledgerIds", min_len=1, parse=self.parse)
        )

        self.fundIds = (
            None if self.fundIds is None else
            validate_list(self.fundIds, "fundIds", min_len=1, parse=self.parse)
        )
        self.entityIds = (
            None if self.entityIds is None else
            validate_list(self.entityIds, "entityIds", min_len=1, parse=self.parse)
        )

        # validate UUIDs for accounts and ledgers if supplied
        if self.accountIds is not None:
            for id_ in self.accountIds:
                check_uuid(id_, f"accountId: {id_}")

        if self.ledgerIds is not None:
            for id_ in self.ledgerIds:
                check_uuid(id_, f"ledgerId: {id_}")

        if self.fundIds is not None:
            for id_ in self.fundIds:
                check_uuid(id_, f"fundIds: {id_}")

        if not (self.accountIds or self.ledgerIds or self.clientId or self.fundId or self.fundIds):
            raise Exception("Search criteria is too broad. Include one of: accountIds, ledgerIds, clientId, or fundId")


    def get_dict(self):
        fields = self.__dict__
        del fields['parse']
        return fields