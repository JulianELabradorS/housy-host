import repositories.property_repository as property_repository


def get_all_properties():
    return property_repository.get_all_properties()

def update_percentage_negotiated(propertyId,data):
    percentage = data.get("percentageNegotiated")
    return property_repository.update_property_percentage_negociated(propertyId,percentage)
