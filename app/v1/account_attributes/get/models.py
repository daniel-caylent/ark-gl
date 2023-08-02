"""Models for AccountAttributes GET"""

from dataclasses import dataclass
from typing import Literal


@dataclass
class Attribute:
    """Account attribute model"""

    # pylint: disable=invalid-name; API standard
    attributeId: str
    accountType: Literal[
        "Assets", "Liabilities", "Partner's Capital", "Income", "Expense", "Gain/Loss"
    ]
    detailType: Literal["Balance Sheet"]
    # pylint: enable=invalid-name
