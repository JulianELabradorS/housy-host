class Trm:
    def __init__(self,
                 jsonTrm):
        self.fromMonth = jsonTrm["fromMonth"] if "fromMonth" in jsonTrm else None
        self.toMonth = jsonTrm["toMonth"] if "toMonth" in jsonTrm else None
        self.trm = jsonTrm["trm"] if "trm" in jsonTrm else 4700
        self.fromYear = jsonTrm["fromYear"] if "fromYear" in jsonTrm else None
        self.toYear = jsonTrm["toYear"] if "toYear" in jsonTrm else None
