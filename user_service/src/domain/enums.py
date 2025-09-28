from enum import Enum

class Status(str, Enum):
    pending = "pending"
    paid  = "paid"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"
    