from datetime import datetime


class Property:
    def __init__(self,
                 id: int,
                 internalListingName: str,
                 country: str,
                 countryCode: str,
                 state: str,
                 city: str,
                 percentageNegotiated: int
                 ):
        self.id = id
        self.internalListingName = internalListingName
        self.country = country
        self.countryCode = countryCode
        self.countryCode = countryCode
        self.state = state
        self.city = city
        self.percentageNegotiated = percentageNegotiated
        self.isNew = True

    def to_dict(self):
        return {
            "id": self.id,
            "internalListingName": self.internalListingName,
            "country": self.country,
            "countryCode": self.countryCode,
            "state": self.state,
            "city": self.city,
            "percentageNegotiated": self.percentageNegotiated,
            "isNew": self.isNew
        }


def get_property_object(json_property):
    return Property(
        json_property["id"],
        json_property["internalListingName"],
        json_property["country"],
        json_property["countryCode"],
        json_property["state"],
        json_property["city"],
        0
    )
