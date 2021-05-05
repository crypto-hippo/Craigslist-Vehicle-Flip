from nltk import word_tokenize

from car import Car
from dao import VehicleDAO
from dd_file_reader import DDFileReader


class GMCHandler(Car):

    series = DDFileReader.read_gmc_series()
    models = DDFileReader.read_gmc_models()

    # Store our instance of our dao for all subaru handlers to use
    vehicle_dao = VehicleDAO()

    def __init__(self, car_data=None):
        if car_data != None:
            self.gmc_data = car_data

    def set_gmc_data(self, car_data):
        self.gmc_data = car_data

    # Check if the ad is void
    def is_void(self):
        # Filtering car data through blacklist applies to every make, so return a boolean value representing whether to void the ad
        return self.check_void(
            self.gmc_data["title"],
            self.gmc_data["subtitle"],
            self.gmc_data["description"]
        )

    def verify_series(self):
        t, s, d = self.gmc_data["title"], self.gmc_data["subtitle"], self.gmc_data["description"]
        for series in self.series:
            if series.count(" ") > 0 and (series in t or series in s or series in d):
                self.gmc_data["series"] = series
                return

            else:
                if series in word_tokenize(t) or series in word_tokenize(s) or series in word_tokenize(d):
                    self.gmc_data["series"] = series
                    return

    def verify_model(self):
        t, s, d = self.gmc_data["title"], self.gmc_data["subtitle"], self.gmc_data["description"]
        t1 = word_tokenize(self.gmc_data["title"])
        s1 = word_tokenize(self.gmc_data["subtitle"])
        d1 = word_tokenize(self.gmc_data["description"])

        for model in self.models:
            if model.count(" ") > 0:
                if model in t or model in s or model in d:
                    self.gmc_data["model"] = model
                    return

            else:
                if model in t1 or model in s1 or model in d1:
                    self.gmc_data["model"] = model
                    return

        if "1500 sierra" in t or "1500 sierra" in s or "1500 sierra":
            self.gmc_data["model"] = "sierra 1500"
            return

        if "2500 sierra" in t or "2500 sierra" in s or "2500 sierra" in d:
            self.gmc_data["model"] = "sierra 2500hd"
            return

        if "2500hd sierra" in t or "2500hd sierra" in s or "2500hd sierra" in d:
            self.gmc_data["model"] = "sierra 2500hd"
            return

        if "2500 hd sierra" in t or "2500 hd sierra" in s or "2500 hd sierra" in d:
            self.gmc_data["model"] = "sierra 2500hd"
            return

        if "3500 sierra" in t or "3500 sierra" in s or "3500 sierra" in d:
            self.gmc_data["model"] = "sierra 3500hd"
            return

        if "3500hd sierra" in t or "3500hd sierra" in s or "3500hd sierra" in d:
            self.gmc_data["model"] = "sierra 3500hd"
            return

        if "3500 hd sierra" in t or "3500 hd sierra" in s or "3500 hd sierra" in d:
            self.gmc_data["model"] = "sierra 3500hd"
            return

    def verify_cylinders(self):
        if self.gmc_data["cylinders"] == None:
            self.gmc_data["cylinders"] = "4"

    def verify_drive(self):
        if self.gmc_data["drive"] == None:
            drive = self.search_for_drive(self.gmc_data["title"], self.gmc_data["subtitle"],self.gmc_data["description"])
            if drive != None:
                self.gmc_data["drive"] = drive
            else:
                self.gmc_data["drive"] = "idk"

    def verify_type(self):
        if self.gmc_data["type"] == None:
            self.gmc_data["type"] = "truck"

    def verify(self):
        print "[+] Verifying Ford"
        self.verify_model()
        self.verify_series()
        self.verify_cylinders()
        self.verify_type()
        self.verify_drive()
        self.print_gmc_data()

        if self.is_void():
            self.vehicle_dao.store_in_blacklist(self.gmc_data.copy())
            return None

        if self.vehicle_dao.is_unique(self.gmc_data["link"]):
            if self.vehicle_dao.duplicate_by_year_price_make_model_odometer_inrange(self.gmc_data.copy()):
                print "[+] Found duplicate based on year, price, make, model, and odometer in range. Skipping"
                return

            is_duplicate, original_link = self.vehicle_dao.duplicate_by_year_make_model_odometer_inrange_price_inrange(
                self.gmc_data.copy())

            if is_duplicate:
                print "[+] Found duplicate with odometer in range and price lowered. Storing in human assistance for testing and opening ads."
                self.vehicle_dao.store_duplicate_for_human_assistance(self.gmc_data.copy(), original_link)
                self.craigslist_handler.open_craigslist_url_for_duplicate(self.gmc_data["link"], original_link)
                self.vauto.handle_honda_bygui(self.gmc_data)

            else:
                self.vehicle_dao.store_in_all_vehicles(self.gmc_data.copy())
                self.craigslist_handler.open_craigslist_url(self.gmc_data["link"])
                self.vauto.handle_honda_bygui(self.gmc_data)

        else:
            print "[+] Link is not unique. Comparing Updated ad. Ya. Showing what's changed in the ad. Opening the ad if the price has lowered"
            if self.gmc_data["price"] == None:
                print "[+] Ad does not contain price. Continuing"
            else:
                new_price = int(self.gmc_data["price"])
                duplicate_row_data = self.vehicle_dao.get_duplicate_link(self.gmc_data["link"])
                duplicate_price = int(duplicate_row_data["price"])
                ad_differences = self.vehicle_dao.compare_ads(self.gmc_data.copy(), duplicate_row_data)
                print "[+] Showing What elements of the ad have been updated"
                print ad_differences
                if new_price < duplicate_price:
                    print "[+] Price on ad %s has lowered by %s" % (
                        self.gmc_data["link"], duplicate_price - new_price)
                    self.craigslist_handler.open_craigslist_url(self.gmc_data["link"])
                    self.vauto.handle_honda_bygui(self.gmc_data)

    def print_gmc_data(self):
        for k, v in self.gmc_data.iteritems():
            if k != "html":
                print k
                print "\t", v