from car import Car
from dd_file_reader import DDFileReader
from nltk import word_tokenize
from dao import VehicleDAO
from vauto_handler import VautoHandler
from craigslist_handler import CraigslistHandler

class ChevroletHandler(Car):

    models = DDFileReader.read_chevrolet_models()
    models_toskip = DDFileReader.read_chevrolet_models_toskip()
    series = DDFileReader.read_chevrolet_series()
    series_to_skip = DDFileReader.read_chevrolet_series_toskip()
    vehicle_dao = VehicleDAO()

    def __init__(self, car_data=None):
        if car_data != None:
            self.chevy_data = car_data

    def verify(self):
        if self.chevy_data["make"] == "chevy":
            self.chevy_data["make"] = "chevrolet"

        self.verify_drive()
        self.verify_model()
        self.verify_cylinders()
        self.verify_series()
        self.print_chevy_data()

        if self.check_void(self.chevy_data["title"], self.chevy_data["subtitle"], self.chevy_data["description"]):
            self.vehicle_dao.store_in_blacklist(self.chevy_data.copy())
            return None

        if self.vehicle_dao.is_unique(self.chevy_data["link"]):
            if self.vehicle_dao.duplicate_by_year_price_make_model_odometer_inrange(self.chevy_data.copy()):
                print "[+] Found duplicate based on year, price, make, model, and odometer in range. Skipping"
                return

            is_duplicate, original_link = self.vehicle_dao.duplicate_by_year_make_model_odometer_inrange_price_inrange(self.chevy_data.copy())

            if is_duplicate:
                print "[+] Found duplicate with odometer in range and price lowered. Storing in human assistance for testing and opening ads."
                self.vehicle_dao.store_duplicate_for_human_assistance(self.chevy_data.copy(), original_link)
                self.craigslist_handler.open_craigslist_url_for_duplicate(self.chevy_data["link"], original_link)
                self.vauto.handle_honda_bygui(self.chevy_data)

            else:
                self.vehicle_dao.store_in_all_vehicles(self.chevy_data.copy())
                self.craigslist_handler.open_craigslist_url(self.chevy_data["link"])
                self.vauto.handle_honda_bygui(self.chevy_data)

        else:
            print "[+] Link is not unique. Comparing ads. Showing what's changed in the ad. Opening the ad if the price has lowered"
            if self.chevy_data["price"] != None:
                new_price = int(self.chevy_data["price"])
                duplicate_row_data = self.vehicle_dao.get_duplicate_link(self.chevy_data["link"])
                duplicate_price = int(duplicate_row_data["price"])
                ad_differences = self.vehicle_dao.compare_ads(self.chevy_data.copy(), duplicate_row_data)
                print "[+] Showing What elements of the ad have been updated"
                print ad_differences
                if new_price < duplicate_price:
                    print "[+] Price on ad %s has lowered by %s" % (self.chevy_data["link"], duplicate_price - new_price)
                    self.craigslist_handler.open_craigslist_url(self.chevy_data["link"])
                    self.vauto.handle_honda_bygui(self.chevy_data, duplicate=True)

    def verify_drive(self):
        if self.chevy_data["drive"] == None:
            possible_drive = self.search_for_drive(self.chevy_data["title"], self.chevy_data["subtitle"], self.chevy_data["description"])
            if possible_drive != None:
                self.chevy_data["drive"] = possible_drive


    def verify_model(self):
        if self.chevy_data["model"] != None and self.chevy_data["model"] in self.models_toskip:
            print "[+] Skipping model %s" % self.chevy_data["model"]
            return False

        for model in self.models:

            if model == "avalanche 1500":
                if model in self.chevy_data["title"] or model in self.chevy_data["subtitle"] or model in self.chevy_data["description"]:
                    self.chevy_data["model"] = model
                    return

                if "avalanche" in self.chevy_data["title"] or "avalanche" in self.chevy_data["subtitle"] or "avalanche" in self.chevy_data["description"]:
                    self.chevy_data["model"] = model
                    return

            if model == "silverado 3500hd":
                if model in self.chevy_data["title"] or model in self.chevy_data["subtitle"] or model in self.chevy_data["description"]:
                    self.chevy_data["model"] = model
                    return

                if "silverado 3500" in self.chevy_data["title"] or "silverado 3500" in self.chevy_data["subtitle"] or "silverado 3500" in self.chevy_data["description"]:
                    self.chevy_data["model"] = model
                    return

                if "silverado" in self.chevy_data["title"] or "silverado" in self.chevy_data["subtitle"] or "silverado" in self.chevy_data["description"]:
                    self.chevy_data["model"] = "silverado 1500"
                    return

            if model == "silverado 2500hd":
                if model in self.chevy_data["title"] or model in self.chevy_data["subtitle"] or model in self.chevy_data["description"]:
                    self.chevy_data["model"] = model
                    return

                if "silverado 2500" in self.chevy_data["title"] or "silverado 2500" in self.chevy_data["subtitle"] or "silverado 2500" in self.chevy_data["description"]:
                    self.chevy_data["model"] = model
                    return

            if model == "suburban 1500":
                if model in self.chevy_data["title"] or model in self.chevy_data["subtitle"] or model in self.chevy_data["description"]:
                    self.chevy_data["model"] = model
                    return

            if model == "suburban 2500":
                if model in self.chevy_data["title"] or model in self.chevy_data["subtitle"] or model in self.chevy_data["description"]:
                    self.chevy_data["model"] = model
                    return

                if "suburban" in self.chevy_data["title"] or "suburban" in self.chevy_data["subtitle"] or "suburban" in self.chevy_data["description"]:
                    self.chevy_data["model"] = model
                    return



        for model in self.models:
            if model in self.chevy_data["title"] or model in self.chevy_data["subtitle"] or model in self.chevy_data["description"]:
                self.chevy_data["model"] = model
                return


    def verify_cylinders(self):
        if self.chevy_data["cylinders"] == None:
            return "4"

    def verify_series(self):
        title_parsed = word_tokenize(self.chevy_data["title"])
        subtitle_parsed = word_tokenize(self.chevy_data["subtitle"])
        description_parsed = word_tokenize(self.chevy_data["description"])

        for series in self.series:
            if series == "base" and (series in self.chevy_data["title"] or series in self.chevy_data["subtitle"]):
                self.chevy_data["series"] = series
                return

            if series == "work truck":
                for value in ["w/t", "worktruck", "work truck", "wt"]:
                    if value in self.chevy_data["title"] or value in self.chevy_data["subtitle"] or value in self.chevy_data["description"]:
                        self.chevy_data["series"] = "work truck"
                        self.chevy_data["type"] = "truck"
                        return

            if series == "sport":
                if series in self.chevy_data["title"] or series in self.chevy_data["subtitle"]:
                    self.chevy_data["series"] = series
                    return

            if series in title_parsed or series in subtitle_parsed or series in description_parsed:
                self.chevy_data["series"] = series
                return

    def print_chevy_data(self):
        for k, v in self.chevy_data.iteritems():
            if k != "html":
                print k
                print "\t", v





