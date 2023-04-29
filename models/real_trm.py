from datetime import datetime


class RealTrm:
    def __init__(self,
                 value: float,
                 startDate: datetime,
                 endDate: int,
                 creationYear: int,
                 ):
        self.value = value
        self.startDate = startDate
        self.endDate = endDate
        self.creationYear = creationYear

    def to_dict(self):
        return {
            "value": self.value,
            "startDate": self.startDate,
            "endDate": self.endDate,
            "creationYear": self.creationYear,
        }
