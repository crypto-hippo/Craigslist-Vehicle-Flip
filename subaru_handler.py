import crawler
from car                import Car
from craigslist_handler import CraigslistHandler
from dd_file_reader     import DDFileReader
from dao                import VehicleDAO
from nltk               import word_tokenize
from vauto_handler      import VautoHandler


class SubaruHandler(Car):

    # Read in the possible subaru mispellings for 'subaru'
    subaru_mispellings = DDFileReader.read_subaru_mispellings()

    # Read in all the subaru models as a list
    models             = DDFileReader.read_subaru_models()

    # Read in a dictionary of models as keys each keys value will be an array of all possible mispellings of the model
    models_mispellings = DDFileReader.read_subaru_models_mispellings_intodict()

    # Read in the series as a list of series
    series             = DDFileReader.read_subaru_series()

    # Read in series to skip for subaru. Some series we don't even want to look at
    series_to_skip = DDFileReader.read_subaru_series_toskip()

    # Store our instance of our dao for all subaru handlers to use
    vehicle_dao        = VehicleDAO()

    def __init__(self, car_data=None):
        if car_data != None:
            self.subaru_data = car_data

    def set_subaru_data(self, subaru_car_data):
        self.subaru_data = subaru_car_data

    # Check if the ad is void
    def is_void(self):
        # Filtering car data through blacklist applies to every make, so return a boolean value representing whether to void the ad
        return self.check_void(
            self.subaru_data["title"],
            self.subaru_data["subtitle"],
            self.subaru_data["description"]
        )


    def verify_series(self):
        if self.subaru_data["series"] == None:
            original_title, original_subtitle, original_description = self.subaru_data["title"], self.subaru_data["subtitle"], self.subaru_data["description"]
            title = word_tokenize(original_title)
            subtitle = word_tokenize(original_subtitle)
            description = word_tokenize(original_description)

            for series in self.series:
                num_words_in_series = series.count(" ") + 1
                if num_words_in_series == 1:
                    if series in title or series in subtitle or series in description:
                        self.subaru_data["series"] = series
                        print "[+] Determined Series: %s" % series
                        return

                elif num_words_in_series == 2 or num_words_in_series == 3:
                    if series in original_title or series in original_subtitle or series in original_description:
                        self.subaru_data["series"] = series
                        print "[+] Determined Series: %s" % series
                        return

            # if self.subaru_data["series"] == None:
            #     try:
            #         if self.subaru_data["model"] == "wrx" and ("wrx limited" in self.subaru_data["title"] or "wrx limited" in self.subaru_data["subtitle"] or "wrx limited" in self.subaru_data["description"]):
            #             self.subaru_data["series"] = "limited"
            #
            #         elif self.subaru_data["model"] == "impreza" and ("rs" in word_tokenize(self.subaru_data["title"]) or "rs" in word_tokenize(self.subaru_data["subtitle"])):
            #             self.subaru_data["series"] = "2.5rs"
            #
            #         elif self.subaru_data["model"] == "forester" and ("l" in word_tokenize(self.subaru_data["title"]) or "l" in word_tokenize(self.subaru_data["subtitle"])):
            #             self.subaru_data["series"] = "l"
            #
            #         elif self.subaru_data["model"] == "forester" and ("s" in word_tokenize(self.subaru_data["title"]) or "s" in word_tokenize(self.subaru_data["subtitle"])):
            #             self.subaru_data["series"] = "s"
            #
            #         elif self.subaru_data["model"] == "forester":
            #             self.subaru_data["series"] = "2.5x"
            #
            #     except Exception as e:
            #         pass

    def verify_model(self):
        if self.subaru_data["model"] == None or self.subaru_data["model"] not in self.models:
            print "[+] Searching craigslist title, subtitle, description for correct subaru models"
            title, subtitle, description = self.subaru_data["title"], self.subaru_data["subtitle"], self.subaru_data["description"]
            t, s, d = word_tokenize(title), word_tokenize(subtitle), word_tokenize(description)

            for word_args in [t, s, d]:
                for model in self.models_mispellings:
                    for arg in word_args:
                        if arg == model or arg in self.models_mispellings[model]:
                            self.subaru_data["model"] = model
                            print "[+] Determined subaru model %s" % model
                            return

        if self.subaru_data["model"].startswith("for"):
            self.subaru_data["model"] = "forester"

    def verify_cylinders(self):
        if self.subaru_data["cylinders"] == None:
            self.subaru_data["cylinders"] = "4"

    def verify_drive(self):
        if self.subaru_data["drive"] == None:
            self.subaru_data["drive"] = "awd"

        # if self.subaru_data["drive"] != None:
        #     drive = self.search_for_drive(
        #         self.subaru_data["title"],
        #         self.subaru_data["subtitle"],
        #         self.subaru_data["description"]
        #     )
        #
        #     if drive != None:
        #         self.subaru_data["drive"] = drive
        #         return
        #
        # self.subaru_data["drive"] = "awd"


    def verify_type(self):
        pass
        # if self.subaru_data["type"] == None:
        #     if self.subaru_data["model"] == "forester":
        #         self.subaru_data["type"] = "suv"
        #         return
        #
        #     elif self.subaru_data["model"] == "impreza":
        #         if "hatchback" in self.subaru_data["title"] or "hatchback" in self.subaru_data["subtitle"] or "hatchback" in self.subaru_data["description"]:
        #             self.subaru_data["type"] = "hatchback"
        #
        #
        #         elif "sedan" in self.subaru_data["title"] or "sedan" in self.subaru_data["subtitle"] or "sedan" in self.subaru_data["description"]:
        #             self.subaru_data["type"] = "sedan"
        #
        #         else:
        #             print "[+] Add more search functionality for impreza line 119"


    def verify(self):
        print "[+] Verifying Subaru"
        self.verify_model()
        self.verify_series()
        if self.subaru_data["series"] in self.series_to_skip:
            self.subaru_data["series"] = None

        self.verify_cylinders()
        self.verify_type()
        self.verify_drive()
        self.print_subaru_data()

        if self.is_void():
            self.vehicle_dao.store_in_blacklist(self.subaru_data.copy())
            return None

        if self.vehicle_dao.is_unique(self.subaru_data["link"]):
            if self.vehicle_dao.duplicate_by_year_price_make_model_odometer_inrange(self.subaru_data.copy()):
                print "[+] Found duplicate based on year, price, make, model, and odometer in range. Skipping"
                return

            is_duplicate, original_link = self.vehicle_dao.duplicate_by_year_make_model_odometer_inrange_price_inrange(self.subaru_data.copy())

            if is_duplicate:
                print "[+] Found duplicate with odometer in range and price lowered. Storing in human assistance for testing and opening ads."
                self.vehicle_dao.store_duplicate_for_human_assistance(self.subaru_data.copy(), original_link)
                self.craigslist_handler.open_craigslist_url_for_duplicate(self.subaru_data["link"], original_link)
                self.vauto.handle_honda_bygui(self.subaru_data)

            else:
                self.vehicle_dao.store_in_all_vehicles(self.subaru_data.copy())
                self.craigslist_handler.open_craigslist_url(self.subaru_data["link"])
                self.vauto.handle_honda_bygui(self.subaru_data)

        else:
            print "[+] Link is not unique. Comparing Updated ad. Ya. Showing what's changed in the ad. Opening the ad if the price has lowered"
            if self.subaru_data["price"] == None:
                print "[+] Ad does not contain price. Continuing"
            else:
                new_price = int(self.subaru_data["price"])
                duplicate_row_data = self.vehicle_dao.get_duplicate_link(self.subaru_data["link"])
                duplicate_price = int(duplicate_row_data["price"])
                ad_differences = self.vehicle_dao.compare_ads(self.subaru_data.copy(), duplicate_row_data)
                print "[+] Showing What elements of the ad have been updated"
                print ad_differences
                if new_price < duplicate_price:
                    print "[+] Price on ad %s has lowered by %s" % (self.subaru_data["link"], duplicate_price - new_price)
                    self.craigslist_handler.open_craigslist_url(self.subaru_data["link"])
                    self.vauto.handle_honda_bygui(self.subaru_data)


    def print_subaru_data(self):
        for k, v in self.subaru_data.iteritems():
            if k != "html":
                print k
                print "\t", v










