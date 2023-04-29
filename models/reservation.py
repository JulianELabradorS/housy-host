from datetime import datetime
from utils.dates import normalize_date
from utils.dates import calculate_nights_by_month
import repositories.budgeted_trm_repository as budgeted_trm_repository
import repositories.real_trm_repository as real_trm_repository
import repositories.property_repository as property_repository


class Reservation:
    def __init__(self,
                 id: str,
                 channelReservationId:    str,
                 channelId: int,
                 channelName: str,
                 source: str or None,
                 confirmationCode: str,
                 totalPrice: float,
                 currency: str,
                 nights: int,
                 numberOfGuests: int,
                 guestName: str,
                 listingName: str,
                 listingMapId: int,
                 cleaningFee: float,
                 channelCommissionAmount: float,
                 hostawayCommissionAmount: float,
                 airbnbExpectedPayoutAmount: float or None,
                 airbnbListingBasePrice: float or None,
                 airbnbListingCancellationHostFee: float or None,
                 airbnbListingCleaningFee: float or None,
                 airbnbTotalPaidAmount: float or None,
                 reservationDate: datetime,
                 arrivalDate: datetime or None,
                 departureDate: datetime or None,
                 previousArrivalDate: datetime or None,
                 previousDepartureDate: datetime or None,
                 cancellationDate: datetime or None,
                 insertedOn: datetime,
                 updatedOn: datetime,
                 latestActivityOn: datetime,
                 status: str,
                 ):
        self.id = id
        self.channelReservationId = channelReservationId
        self.channelId = channelId
        self.channelName = channelName
        self.source = source
        self.confirmationCode = confirmationCode
        self.totalPrice = totalPrice
        self.currency = currency
        self.nights = nights
        self.numberOfGuests = numberOfGuests
        self.guestName = guestName
        self.listingName = listingName
        self.listingMapId = listingMapId
        self.cleaningFee = cleaningFee or 0
        self.channelCommissionAmount = channelCommissionAmount
        self.hostawayCommissionAmount = hostawayCommissionAmount
        self.airbnbExpectedPayoutAmount = airbnbExpectedPayoutAmount
        self.airbnbListingBasePrice = airbnbListingBasePrice
        self.airbnbListingCancellationHostFee = airbnbListingCancellationHostFee
        self.airbnbListingCleaningFee = airbnbListingCleaningFee
        self.airbnbTotalPaidAmount = airbnbTotalPaidAmount
        self.reservationDate = reservationDate
        self.arrivalDate = arrivalDate
        self.departureDate = departureDate
        self.insertedOn = insertedOn
        self.updatedOn = updatedOn
        self.latestActivityOn = latestActivityOn
        self.previousArrivalDate = previousArrivalDate
        self.previousDepartureDate = previousDepartureDate
        self.cancellationDate = cancellationDate
        self.status = status
        self.foundCommisionAmount = self.get_commission_amount()
        self.ownerpayoutwc = self.calculate_ownerpayoutwc()
        self.arrivalDateMonth = arrivalDate.month
        self.arrivalDateYear = arrivalDate.year
        self.realValueReceived = 0
        self.realCleaningFee = 0
        self.realValueReceived = 0
        self.realCleaningFee = 0
        self.realValuesCurrency = ""

    def get_commission_amount(self):
        if (self.channelName == 'airbnbOfficial'):
            base_price = self.airbnbListingBasePrice or 0
            expected = self.airbnbExpectedPayoutAmount or 0
            return base_price - expected
        else:
            return self.channelCommissionAmount or 0

    def calculate_ownerpayoutwc(self):
        if (self.status == 'new' or self.status == 'modified'):
            if self.channelName == 'airbnbOfficial':
                return self.airbnbExpectedPayoutAmount - self.cleaningFee
            if self.channelName == 'bookingcom' or self.channelName == 'marriott':
                return self.totalPrice - self.foundCommisionAmount - self.cleaningFee
            if (self.channelName == 'expedia'):
                commission = self.totalPrice * 0.16
                if (self.currency == 'USD'):
                    return self.totalPrice - self.cleaningFee - commission
                else:
                    return self.totalPrice - 160.000 - commission
            if self.channelName == 'homeaway':
                commission = self.totalPrice * 0.05
                return self.totalPrice - self.cleaningFee - commission
            if (self.channelName == 'bookingengine' or self.channelName == 'direct'):
                return self.totalPrice
            return 0
        else:
            return 0

        # marriot => total price - cleaning - channel comission
        # expedia (totalprice)- cleaning -16%
        # booking total price- cleaning - comission
        # source:VRBO - channelName homeaway total price - cleaning - comission 5%

    def get_prorated_data_of_reservation(self):
        tabulatedData = []
        if (self.status == 'new' or self.status == 'modified'):
            calculated_nights, total_nights = calculate_nights_by_month(
                self.arrivalDate, self.departureDate)
            for index, calculated_night in enumerate(calculated_nights):
                budgeted_trm = 0
                real_trm = 0
                nigths = calculated_night['nights']
                month = calculated_night['month']
                year = calculated_night['year']
                price_by_night = self.ownerpayoutwc / total_nights
                total_calculated = price_by_night * nigths
                cleaning = self.cleaningFee if index  == 0 and self.cleaningFee else 0
                budgeted_total = total_calculated
                budgeted_cleaning_fee = cleaning 
                property_commission_percentage = property_repository.get_property_commission_percentage(
                    self.listingMapId)
                if (self.currency == 'USD'):
                    budgeted_trm = budgeted_trm_repository.get_budgeted_trm_of_month(month, year)
                    real_trm = real_trm_repository.get_real_trm_of_date(self.arrivalDate)
                    budgeted_total = budgeted_total * budgeted_trm
                    budgeted_cleaning_fee = budgeted_cleaning_fee * budgeted_trm
                    
                tabulatedData.append({
                    "id": f'{self.id}-{index}',
                    "reservationId": self.id,
                    "currency": self.currency,
                    "listingName": self.listingName,
                    "listingMapId": self.listingMapId,
                    "guestName": self.guestName,
                    "status": self.status,
                    "channelName": self.channelName,
                    "baseTotalPaid": self.ownerpayoutwc,
                    "baseCleaningFee": cleaning,
                    "PricePerNight": price_by_night,
                    "totalCalculated": total_calculated,
                    "budgetedTrm": budgeted_trm,
                    "realTrm": real_trm,
                    "budgetedTotal": budgeted_total,
                    "budgetedCleaningFee": budgeted_cleaning_fee,
                    "realValueReceived": 0,
                    "realCleaningFee": 0,
                    "realValuesCurrency": "",
                    "convertedRealValueReceived": 0,
                    "convertedRealCleaningFee": 0,
                    "budgetedCommission": budgeted_total * property_commission_percentage,
                    "realCommission": 0,
                    "netProprietary": 0,
                    "nights": nigths,
                    "totalNights": self.nights,
                    "monthNumber": month,
                    "year": year,
                    "arrivalDate": self.arrivalDate,
                    "departureDate": self.departureDate,
                    "listingCommissionPercentage" : property_commission_percentage
                })
        return tabulatedData

    def to_dict(self):
        return {
            "id": self.id,
            "channelReservationId": self.channelReservationId,
            "channelId": self.channelId,
            "channelName": self.channelName,
            "confirmationCode": self.confirmationCode,
            "totalPrice": self.totalPrice,
            "currency": self.currency,
            "nights": self.nights,
            "numberOfGuests": self.numberOfGuests,
            "guestName": self.guestName,
            "listingName": self.listingName,
            "listingMapId": self.listingMapId,
            "cleaningFee": self.cleaningFee,
            "channelCommissionAmount": self. channelCommissionAmount,
            "hostawayCommissionAmount": self.hostawayCommissionAmount,
            "airbnbExpectedPayoutAmount": self.airbnbExpectedPayoutAmount,
            "airbnbListingBasePrice": self.airbnbListingBasePrice,
            "airbnbListingCancellationHostFee": self.airbnbListingCancellationHostFee,
            "airbnbListingCleaningFee": self.airbnbListingCleaningFee,
            "airbnbTotalPaidAmount": self.airbnbTotalPaidAmount,
            "reservationDate": self.reservationDate,
            "arrivalDate": self.arrivalDate,
            "departureDate": self.departureDate,
            "insertedOn": self.insertedOn,
            "updatedOn": self.updatedOn,
            "latestActivityOn": self.latestActivityOn,
            "previousArrivalDate": self.previousArrivalDate,
            "previousDepartureDate": self.previousDepartureDate,
            "cancellationDate": self.cancellationDate,
            "status": self.status,
            "ownerpayoutwc": self.ownerpayoutwc,
            "arrivalDateMonth": self.arrivalDateMonth,
            "arrivalDateYear": self.arrivalDateYear,
            "realValueReceived": self.realValueReceived,
            "realCleaningFee": self.realCleaningFee,
            "realValuesCurrency": self.realValuesCurrency
        }


def get_reservation_object(reservation) -> Reservation:
    return Reservation(
        reservation["id"],
        reservation["channelReservationId"],
        reservation["channelId"],
        reservation["channelName"],
        reservation["source"],
        reservation["confirmationCode"],
        reservation["totalPrice"],
        reservation["currency"],
        reservation["nights"],
        reservation["numberOfGuests"],
        reservation["guestName"],
        reservation["listingName"],
        reservation["listingMapId"],
        reservation["cleaningFee"],
        reservation["channelCommissionAmount"],
        reservation["hostawayCommissionAmount"],
        reservation["airbnbExpectedPayoutAmount"],
        reservation["airbnbListingBasePrice"],
        reservation["airbnbListingCancellationHostFee"],
        reservation["airbnbListingCleaningFee"],
        reservation["airbnbTotalPaidAmount"],
        normalize_date(reservation["reservationDate"]),
        normalize_date(reservation["arrivalDate"]),
        normalize_date(reservation["departureDate"]),
        normalize_date(reservation["previousArrivalDate"]),
        normalize_date(reservation["previousDepartureDate"]),
        normalize_date(reservation["cancellationDate"]),
        normalize_date(reservation["insertedOn"]),
        normalize_date(reservation["updatedOn"]),
        normalize_date(reservation["latestActivityOn"]),
        reservation["status"],
    )
