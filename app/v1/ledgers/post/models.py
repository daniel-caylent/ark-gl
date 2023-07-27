"""Models for Ledgers POST"""

from dataclasses import dataclass

from shared.dataclass_validators import check_uuid, validate_str, validate_int # pylint: disable=import-error; Lambda layer dependency


@dataclass
class LedgerPost:
    """Ledger POST model"""

    # pylint: disable=invalid-name; API standard
    fundId: str
    clientId: str
    glName: str
    currencyName: str
    currencyDecimal: int
    glDescription: str = None
    # pylint: enable=invalid-name

    def __post_init__(self):
        self.fundId = check_uuid(self.fundId, "fundId")
        self.clientId = check_uuid(self.clientId, "clientId")
        self.glName = validate_str(self.glName, "glName", min_len=3, max_len=128)
        self.currencyDecimal = validate_int(
            self.currencyDecimal, "currencyDecimal", allowed=[0, 2, 3, 4]
        )
        self.currencyName = validate_str(
            self.currencyName, "currencyName", min_len=3, max_len=3
        )
        self.glDescription = (
            None
            if self.glDescription is None
            else validate_str(self.glDescription, "glDescription")
        )
