from datetime import datetime


class BudgetedTrm:
    def __init__(self,
                 value: float,
                 startDate: datetime,
                 monthNumber: int,
                 year: int,
                 ):
        self.value = value
        self.startDate = startDate
        self.monthNumber = monthNumber
        self.year = year

    def to_dict(self):
        return {
            "value": self.value,
            "startDate": self.startDate,
            "monthNumber": self.monthNumber,
            "year": self.year,
        }
