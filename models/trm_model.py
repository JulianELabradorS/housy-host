class Trm:
    def __init__(self,
                 jsonTrm):
        self.fromMonth = jsonTrm["fromMonth"]
        self.toMonth = jsonTrm["toMonth"]
        self.trm = jsonTrm["trm"]
        self.fromYear = jsonTrm["fromYear"]
        self.toYear = jsonTrm["toYear"]
