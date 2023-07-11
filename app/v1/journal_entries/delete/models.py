from dataclasses import dataclass

from shared.dataclass_validators import validate_date, validate_list, validate_str, check_uuid

@dataclass
class FilterInput:
    startDate: str = None
    endDate: str = None
    clientId: str = None
    fundId: str = None
    accountIds: list = None
    ledgerIds: list = None
    entityIds: list = None

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
        self.accountIds = (
            None if self.accountIds is None else
            validate_list(self.accountIds, "accountIds", min_len=1, parse=True)
        )
        self.ledgerIds = (
            None if self.ledgerIds is None else 
            validate_list(self.ledgerIds, "ledgerIds", min_len=1, parse=True)
        )
        self.entityIds = (
            None if self.entityIds is None else
            validate_list(self.entityIds, "entityIds", min_len=1, parse=True)
        )

        # validate UUIDs for accounts and ledgers if supplied
        if self.accountIds is not None:
            for id_ in self.accountIds:
                check_uuid(id_, f"accountId: {id_}")

        if self.ledgerIds is not None:
            for id_ in self.ledgerIds:
                check_uuid(id_, f"ledgerId: {id_}")
