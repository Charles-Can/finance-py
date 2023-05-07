from .stock import Stock

class Bond(Stock):

    _coupon = 0
    _bond_yield = 0

    def __init__(self, symbol='', shares=0, purchase_price=0, current_value=0, purchase_date='', coupon=0, bond_yield=0):
        super().__init__(symbol, shares, purchase_price,
                         current_value, purchase_date)
        self.coupon = coupon
        self.bond_yield = bond_yield


    @property
    def coupon(self):
        return self._coupon
    
    @coupon.setter
    def coupon(self,value):
        self._coupon = float(value)

    @property
    def bond_yield(self):
        return self._bond_yield
    
    @bond_yield.setter
    def bond_yield(self, value):
        self._bond_yield = float(value)
