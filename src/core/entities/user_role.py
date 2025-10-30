from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    SELLER = "seller"
    STOCK_MANAGER = "stock_manager"