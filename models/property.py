from typing import List
from .trm_model import Trm
from .negotiation_model import Negotiation


class Property:
    def __init__(self,
                 jsonProperty):
        self.listingName = jsonProperty["listingName"]

        if ("negotiations" not in jsonProperty):
            self.negotiations = []
        elif ("negotiations" in jsonProperty):
            if (any(neg is None for neg in jsonProperty['negotiations'])):
                self.negotiations = []
            else:
                self.negotiations = [Negotiation(
                    neg) for neg in jsonProperty['negotiations']]

        if ("trms" not in jsonProperty):
            self.trms = []
        elif ("trms" in jsonProperty):
            if (any(trm is None for trm in jsonProperty['trms'])):
                self.trms = []
            else:
                self.trms = [Trm(trm) for trm in jsonProperty['trms']]
