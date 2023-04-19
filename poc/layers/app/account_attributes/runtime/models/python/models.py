from dataclasses import dataclass
from typing import Literal

@dataclass
class Attribute:
    attributeNo: int
    accountType: Literal["Assets", "Liabilities", "Partner's Capital", "Income", "Expense", "Gain/Loss"]
    detailType: Literal["Balance Sheet"]
