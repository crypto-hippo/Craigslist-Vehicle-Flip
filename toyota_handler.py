from car import Car 

class ToyotaHandler(Car):

    def __init__(self, ad_data):
        super(Car, self).__init__()
        self.toyota_data = ad_data

    
