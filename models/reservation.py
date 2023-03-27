class Reservation:
    def __init__(self,
                 idReserva: str,
                 reserva: str,
                 presupuesto: str,
                 aseoPpto: str,
                 comisionPpto: str,
                 comisionReal: str,
                 netoPropietario: str,
                 presupuestoReal: str,
                 aseoReal: str,
                 noches: str,
                 origen: str,
                 negociacion: str,
                 mes: str,
                 anio: str,
                 listingName: str,
                 currency: str,
                 trm: str,
                 totalPriceCOP: str,
                 aseoPptoCOP,
                 comisionPptoCOP,
                 comisionRealCOP,
                 netoPropietarioCOP,
                 presupuestoRealCOP,
                 aseoRealCOP):
        self.id = idReserva
        self.guestName = reserva
        self.totalPrice = presupuesto
        self.aseoPpto = aseoPpto
        self.comisionPpto = comisionPpto
        self.comisionReal = comisionReal
        self.netoPropietario = netoPropietario
        self.presupuestoReal = presupuestoReal
        self.aseoReal = aseoReal
        self.nights = noches
        self.channelName = origen
        self.negociacion = negociacion
        self.mes = mes
        self.anio = anio
        self.listingName = listingName
        self.currency = currency
        self.trm = trm
        self.totalPriceCOP = totalPriceCOP
        self.aseoPptoCOP = aseoPptoCOP
        self.comisionPptoCOP = comisionPptoCOP
        self.comisionRealCOP = comisionRealCOP
        self.netoPropietarioCOP = netoPropietarioCOP
        self.presupuestoRealCOP = presupuestoRealCOP
        self.aseoRealCOP = aseoRealCOP
