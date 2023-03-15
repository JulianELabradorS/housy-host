class Negotiation:
    def __init__(self,
                 jsonNegotiation):
        self.fromMonth = jsonNegotiation["fromMonth"]
        self.toMonth = jsonNegotiation["toMonth"]
        self.fromYear = jsonNegotiation["fromYear"]
        self.toYear = jsonNegotiation["toYear"]
        self.percentage = jsonNegotiation["percentage"]
