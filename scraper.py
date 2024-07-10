from dataclasses import dataclass
from typing import Optional


@dataclass
class Company:
    # From list
    name: str
    details_url: str
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    image_url: Optional[str] = None
    rate_value: Optional[float] = None
    rate_count: Optional[int] = None

    # From details
    street: Optional[str] = None
    postal_code: Optional[str] = None
    region: Optional[str] = None
    nip: Optional[str] = None
    description: Optional[str] = None
