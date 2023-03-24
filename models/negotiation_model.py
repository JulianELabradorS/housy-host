class Negotiation:
    def __init__(self,
                 jsonNegotiation):
        self.fromMonth = jsonNegotiation["fromMonth"] if "fromMonth" in jsonNegotiation else None
        self.toMonth = jsonNegotiation["toMonth"] if "toMonth" in jsonNegotiation else None
        self.fromYear = jsonNegotiation["fromYear"] if "fromYear" in jsonNegotiation else None
        self.toYear = jsonNegotiation["toYear"] if "toYear" in jsonNegotiation else None
        self.percentage = jsonNegotiation["percentage"] if "percentage" in jsonNegotiation else None
