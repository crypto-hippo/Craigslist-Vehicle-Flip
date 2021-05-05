from nltk import word_tokenize

from car import Car
from craigslist_handler import CraigslistHandler
from dao import VehicleDAO
from dd_file_reader import DDFileReader
from vauto_handler import VautoHandler


class FordHandler(Car):


    # Read in all the subaru models as a list
    models = DDFileReader.read_ford_models()

    # Read in the series as a list of series
    series = DDFileReader.read_ford_series()
    series_no_description = ["limited", "fx4", "sport", "base", "platinum"]
    # Store our instance of our dao for all subaru handlers to use
    vehicle_dao = VehicleDAO()

    def __init__(self, car_data=None):
        if car_data != None:
            self.ford_data = car_data

    def set_ford_data(self, car_data):
        self.ford_data = car_data

    # Check if the ad is void
    def is_void(self):
        # Filtering car data through blacklist applies to every make, so return a boolean value representing whether to void the ad
        return self.check_void(
            self.ford_data["title"],
            self.ford_data["subtitle"],
            self.ford_data["description"]
        )

    def verify_series(self):
        t, s, d = self.ford_data["title"], self.ford_data["subtitle"], self.ford_data["description"]
        for series in self.series:
            if series not in self.series_no_description:
                if series.count(" ") > 0:
                    if series in t or series in s or series in d:
                        self.ford_data["series"] = series
                        return
                else:
                    if series in word_tokenize(t) or series in word_tokenize(s) or series in word_tokenize(d):
                        self.ford_data["series"] = series
                        return

            else:
                if series.count(" ") > 0:
                    if series in t or series in s:
                        self.ford_data["series"] = series
                        return
                else:
                    if series in word_tokenize(t) or series in word_tokenize(s):
                        self.ford_data["series"] = series
                        return

    def verify_model(self):
        if self.ford_data["model"] == None or self.ford_data["model"] not in self.models:
            title, subtitle, description = self.ford_data["title"], self.ford_data["subtitle"], self.ford_data["description"]
            for model in self.models:
                if model == "f-150":
                    if "150" in title or "150" in subtitle or "150" in description:
                        self.ford_data["model"] = model
                        return

                    elif "f150" in title or "f150" in subtitle or "f150" in description:
                        self.ford_data["model"] = model
                        return

                    elif "f 150" in title or "f 150" in subtitle or "f 150" in description:
                        self.ford_data["model"] = model
                        return

                    elif "f-150" in title or "f-150" in subtitle or "f-150" in description:
                        self.ford_data["model"] = model
                        return

                elif model == "f-250sd":
                    if "f-250" in title or "f-250" in subtitle or "f-250" in description:
                        self.ford_data["model"] = model
                        return

                    elif "f250" in title or "f250" in subtitle or "f250" in description:
                        self.ford_data["model"] = model
                        return

                elif model == "f-350sd":
                    if "f-350" in title or "f-350" in subtitle or "f-350" in description:
                        self.ford_data["model"] = model
                        return

                    elif "f350" in title or "f350" in subtitle or "f350" in description:
                        self.ford_data["model"] = model
                        return

                elif model == "f-450sd":
                    if "f-450" in title or "f-450" in subtitle or "f-450" in description:
                        self.ford_data["model"] = model
                        return

                    elif "f450" in title or "f450" in subtitle or "f450" in description:
                        self.ford_data["model"] = model
                        return

                elif model == "f-550sd":
                    if "f-550" in title or "f-550" in subtitle or "f-550" in description:
                        self.ford_data["model"] = model
                        return

                    elif "f550" in title or "f550" in subtitle or "f550" in description:
                        self.ford_data["model"] = model
                        return

                elif model in title or model in subtitle or model in description:
                    self.ford_data["model"] = model
                    return

    def verify_cylinders(self):
        if self.ford_data["cylinders"] == None:
            self.ford_data["cylinders"] = "4"

    def verify_drive(self):
        if self.ford_data["drive"] == None:
            drive = self.search_for_drive(self.ford_data["title"], self.ford_data["subtitle"], self.ford_data["description"])
            if drive != None:
                self.ford_data["drive"] = "idk"

    def verify_type(self):
        if self.ford_data["type"] == None:
            self.ford_data["type"] = "truck"

    def verify(self):
        print "[+] Verifying Ford"
        self.verify_model()
        self.verify_series()
        self.verify_cylinders()
        self.verify_type()
        self.verify_drive()
        self.print_ford_data()

        if self.is_void():
            self.vehicle_dao.store_in_blacklist(self.ford_data.copy())
            return None

        if self.vehicle_dao.is_unique(self.ford_data["link"]):
            if self.vehicle_dao.duplicate_by_year_price_make_model_odometer_inrange(self.ford_data.copy()):
                print "[+] Found duplicate based on year, price, make, model, and odometer in range. Skipping"
                return

            is_duplicate, original_link = self.vehicle_dao.duplicate_by_year_make_model_odometer_inrange_price_inrange(self.ford_data.copy())

            if is_duplicate:
                print "[+] Found duplicate with odometer in range and price lowered. Storing in human assistance for testing and opening ads."
                self.vehicle_dao.store_duplicate_for_human_assistance(self.ford_data.copy(), original_link)
                self.craigslist_handler.open_craigslist_url_for_duplicate(self.ford_data["link"], original_link)
                self.vauto.handle_honda_bygui(self.ford_data)

            else:
                self.vehicle_dao.store_in_all_vehicles(self.ford_data.copy())
                self.craigslist_handler.open_craigslist_url(self.ford_data["link"])
                self.vauto.handle_honda_bygui(self.ford_data)

        else:
            print "[+] Link is not unique. Comparing Updated ad. Ya. Showing what's changed in the ad. Opening the ad if the price has lowered"
            if self.ford_data["price"] == None:
                print "[+] Ad does not contain price. Continuing"
            else:
                new_price = int(self.ford_data["price"])
                duplicate_row_data = self.vehicle_dao.get_duplicate_link(self.ford_data["link"])
                duplicate_price = int(duplicate_row_data["price"])
                ad_differences = self.vehicle_dao.compare_ads(self.ford_data.copy(), duplicate_row_data)
                print "[+] Showing What elements of the ad have been updated"
                print ad_differences
                if new_price < duplicate_price:
                    print "[+] Price on ad %s has lowered by %s" % (
                    self.ford_data["link"], duplicate_price - new_price)
                    self.craigslist_handler.open_craigslist_url(self.ford_data["link"])
                    self.vauto.handle_honda_bygui(self.ford_data)

    def print_ford_data(self):
        for k, v in self.ford_data.iteritems():
            if k != "html":
                print k
                print "\t", v




