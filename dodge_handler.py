from car import Car
from craigslist_handler import CraigslistHandler
from dao import VehicleDAO
from dd_file_reader import DDFileReader
from nltk import word_tokenize

from vauto_handler import VautoHandler


class DodgeHandler(Car):

    models = DDFileReader.read_dodge_models()
    series = DDFileReader.read_dodge_series()

    # Store our instance of our dao for all subaru handlers to use
    vehicle_dao = VehicleDAO()

    def __init__(self, car_data=None):
        if car_data != None:
            self.dodge_data = car_data

    def verify_cylinders(self):
        if self.dodge_data["cylinders"] == None:
            self.dodge_data["cylinders"] = "4"

    def verify_drive(self):
        if self.dodge_data["drive"] == None:
            drive = self.search_for_drive(self.dodge_data["title"], self.dodge_data["subtitle"], self.dodge_data["description"])
            if drive != None:
                self.dodge_data["drive"] = drive


    def verify_type(self):
        if self.dodge_data["type"] == None:
            self.dodge_data["type"] = "truck"

    def verify_model(self):
        t, s, d = self.dodge_data["title"], self.dodge_data["subtitle"], self.dodge_data["description"]
        t1 = word_tokenize(self.dodge_data["title"])
        s1 = word_tokenize((self.dodge_data["subtitle"]))
        d1 = word_tokenize(self.dodge_data["description"])

        for model in self.models:

            if self.dodge_data["make"] == "dodge":
                if model == "ram 1500":
                    if "1500" in t or "1500" in s or "1500" in d:
                        self.dodge_data["model"] = model
                        return

                if model == "ram 2500":
                    if "2500" in t or "2500" in s or "2500" in d:
                        self.dodge_data["model"] = model
                        return

                if model == "ram 3500hd":
                    if "ram" in t1 or "ram" in s1 or "ram" in d1:
                        if "3500hd" in t or "3500hd" in s or "3500hd" in d:
                            self.dodge_data["model"] = model
                            return

                        if "3500 hd" in t or "3500 hd" in s or "3500 hd" in d:
                            self.dodge_data["model"] = model
                            return

                        if "3500" in t or "3500" in s or "3500" in d:
                            self.dodge_data["model"] = model
                            return

                if model == "ram 4500hd":
                    if "ram" in t1 or "ram" in s1 or "ram" in d1:
                        if "4500hd" in t or "4500hd" in s or "4500hd" in d:
                            self.dodge_data["model"] = model
                            return

                        if "4500 hd" in t or "4500 hd" in s or "4500 hd" in d:
                            self.dodge_data["model"] = model
                            return

                        if "4500" in t or "4500" in s or "4500" in d:
                            self.dodge_data["model"] = model
                            return

                if model == "ram 5500hd":
                    if "ram" in t1 or "ram" in s1 or "ram" in d1:
                        if "5500hd" in t or "5500hd" in s or "5500hd" in d:
                            self.dodge_data["model"] = model
                            return

                        if "5500 hd" in t or "5500 hd" in s or "5500 hd" in d:
                            self.dodge_data["model"] = model
                            return

                        if "5500" in t or "5500" in s or "5500" in d:
                            self.dodge_data["model"] = model
                            return

            elif self.dodge_data["make"] == "ram":
                if model == "ram 1500":
                    if "1500" in t or "1500" in s or "1500" in d:
                        self.dodge_data["model"] = "1500"
                        return

                if model == "ram 2500":
                    if "2500" in t or "2500" in s or "2500" in d:
                        self.dodge_data["model"] = "2500"
                        return

                if model == "ram 3500hd":
                    if "ram" in t1 or "ram" in s1 or "ram" in d1:
                        if "3500hd" in t or "3500hd" in s or "3500hd" in d:
                            self.dodge_data["model"] = "3500hd"
                            return

                        if "3500 hd" in t or "3500 hd" in s or "3500 hd" in d:
                            self.dodge_data["model"] = "3500hd"
                            return

                        if "3500" in t or "3500" in s or "3500" in d:
                            self.dodge_data["model"] = "3500"
                            return


                if model == "ram 4500hd":
                    if "ram" in t1 or "ram" in s1 or "ram" in d1:
                        if "4500hd" in t or "4500hd" in s or "4500hd" in d:
                            self.dodge_data["model"] = "4500hd"
                            return

                        if "4500 hd" in t or "4500 hd" in s or "4500 hd" in d:
                            self.dodge_data["model"] = "4500hd"
                            return

                        if "4500" in t or "4500" in s or "4500" in d:
                            self.dodge_data["model"] = "4500hd"
                            return

                if model == "ram 5500hd":
                    if "ram" in t1 or "ram" in s1 or "ram" in d1:
                        if "5500hd" in t or "5500hd" in s or "5500hd" in d:
                            self.dodge_data["model"] = "5500hd"
                            return

                        if "5500 hd" in t or "5500 hd" in s or "5500 hd" in d:
                            self.dodge_data["model"] = "5500hd"
                            return

                        if "5500" in t or "5500" in s or "5500" in d:
                            self.dodge_data["model"] = "5500hd"
                            return

            if model.count(" ") > 0:
                if model in t or model in s or model in d:
                    self.dodge_data["model"] = model
                    return

            if model.count(" ") == 0:
                if model in t1 or model in s1 or model in d1:
                    self.dodge_data["model"] = model
                    return

    def verify_series(self):
        title = word_tokenize(self.dodge_data["title"])
        subtitle = word_tokenize(self.dodge_data["subtitle"])
        description = word_tokenize(self.dodge_data["description"])

        t, s, d = self.dodge_data["title"], self.dodge_data["subtitle"], self.dodge_data["description"]

        for series in self.series:
            if series == "r/t":
                if series in title or series in subtitle or series in description:
                    self.dodge_data["series"] = series
                    return

                if "rt" in title or "rt" in subtitle or "rt" in description:
                    self.dodge_data["series"] = series
                    return

            if series == "tradesmen":
                if "express" in title or "express" in subtitle or "express" in description:
                    self.dodge_data["series"] = series
                    return

                if "work truck" in title or "work truck" in subtitle or "work truck" in description:
                    self.dodge_data["series"] = series
                    return

                if "w/t" in title or "w/t" in subtitle or "w/t" in description:
                    self.dodge_data["series"] = series
                    return

            if series == "laramie longhorn":
                if "longhorn laramie" in t or "longhorn laramie" in s or "longhorn laramie" in d:
                    self.dodge_data["series"] = series
                    return

            if series == "slt":
                if "big horn" in t or "big horn" in s or "big horn" in d:
                    self.dodge_data["series"] = series
                    return

                if "lone star" in t or "lone star" in s or "lone star" in d:
                    self.dodge_data["series"] = series
                    return

                if "outdoorsman" in t or "outdoorsman" in s or "outdoorsman" in d:
                    self.dodge_data["series"] = series
                    return

            if series == "limited hybrid":
                if series in t or series in s or series in d:
                    self.dodge_data["series"] = series
                    return

            if series == "sport" or series == "limited":
                if series in t or series in s:
                    self.dodge_data["series"] = series
                    return

            if series in title or series in subtitle or series in description:
                self.dodge_data["series"] = series
                return

    def verify(self):
        if self.dodge_data["year"] >= '2011' and ("ram" in self.dodge_data["title"] or "ram" in self.dodge_data["subtitle"]):
            self.dodge_data["make"] = "ram"

        self.verify_cylinders()
        self.verify_drive()
        self.verify_type()
        self.verify_model()
        self.verify_series()
        self.print_dodge_data()

        if self.check_void(self.dodge_data["title"], self.dodge_data["subtitle"], self.dodge_data["description"]):
            self.vehicle_dao.store_in_blacklist(self.dodge_data.copy())
            return None

        if self.vehicle_dao.is_unique(self.dodge_data["link"]):
            if self.vehicle_dao.duplicate_by_year_price_make_model_odometer_inrange(self.dodge_data.copy()):
                print "[+] Found duplicate based on year, price, make, model, and odometer in range. Skipping"
                return

            is_duplicate, original_link = self.vehicle_dao.duplicate_by_year_make_model_odometer_inrange_price_inrange(
                self.dodge_data.copy())

            if is_duplicate:
                print "[+] Found duplicate with odometer in range and price lowered. Storing in human assistance for testing and opening ads."
                self.vehicle_dao.store_duplicate_for_human_assistance(self.dodge_data.copy(), original_link)
                self.craigslist_handler.open_craigslist_url_for_duplicate(self.dodge_data["link"], original_link)
                self.vauto.handle_honda_bygui(self.dodge_data)

            else:
                self.vehicle_dao.store_in_all_vehicles(self.dodge_data.copy())
                self.craigslist_handler.open_craigslist_url(self.dodge_data["link"])
                self.vauto.handle_honda_bygui(self.dodge_data)

        else:
            print "[+] Link is not unique. Comparing Updated ad. Ya. Showing what's changed in the ad. Opening the ad if the price has lowered"
            if self.dodge_data["price"] == None:
                print "[+] Ad does not contain price. Continuing"
            else:
                new_price = int(self.dodge_data["price"])
                duplicate_row_data = self.vehicle_dao.get_duplicate_link(self.dodge_data["link"])
                duplicate_price = int(duplicate_row_data["price"])
                ad_differences = self.vehicle_dao.compare_ads(self.dodge_data.copy(), duplicate_row_data)
                print "[+] Showing What elements of the ad have been updated"
                print ad_differences
                if new_price < duplicate_price:
                    print "[+] Price on ad %s has lowered by %s" % (
                        self.dodge_data["link"], duplicate_price - new_price)
                    self.craigslist_handler.open_craigslist_url(self.dodge_data["link"])
                    self.vauto.handle_honda_bygui(self.dodge_data)

    def print_dodge_data(self):
        for k, v in self.dodge_data.iteritems():
            if k != "html":
                print k
                print "\t", v


