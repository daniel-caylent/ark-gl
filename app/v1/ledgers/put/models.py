"""Models for Ledgers PUT"""

from dataclasses import dataclass

from shared.dataclass_validators import validate_str, validate_int # pylint: disable=import-error; Lambda layer dependency


@dataclass
class LedgerPut:
    """Model for ledger PUT request"""

    # pylint: disable=invalid-name; API standard
    glName: str = None
    glDescription: str = None
    currencyName: str = None
    currencyDecimal: int = None
    isHidden: bool = False
    # pylint: enable=invalid-name

    def __post_init__(self):
        self.glName = (
            None
            if self.glName is None
            else validate_str(self.glName, "glName", min_len=3, max_len=128)
        )
        self.currencyDecimal = (
            None
            if self.currencyDecimal is None
            else validate_int(
                self.currencyDecimal, "currencyDecimal", allowed=[0, 2, 3, 4]
            )
        )
        self.currencyName = (
            None
            if self.currencyName is None
            else validate_str(self.currencyName, "currencyName", min_len=3, max_len=3)
        )
        self.glDescription = (
            None
            if self.glDescription is None
            else validate_str(
                self.glDescription, "glDescription"
            )
        )
        self.isHidden = None if self.isHidden is None else bool(self.isHidden)
