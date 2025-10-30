from enum import Enum

class PaymentType(Enum):
    MONEY = 'Money'
    DEBIT = 'Debit'
    CREDIT = 'Credit'
    PIX = 'PIX'
    OTHER = 'Other'
