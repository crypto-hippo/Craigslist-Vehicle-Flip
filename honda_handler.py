from car                import Car
from vauto_handler      import VautoHandler
from nltk.tokenize      import word_tokenize
from dd_file_reader     import DDFileReader
from craigslist_handler import CraigslistHandler
from dao                import VehicleDAO

class HondaHandler(Car):
    sedan_identifiers                   = DDFileReader.read_sedan_identifiers()
    coupe_identifiers                   = DDFileReader.read_coupe_identifiers()
    honda_basic_series                  = DDFileReader.read_honda_basic_series()
    honda_rare_series                   = DDFileReader.read_honda_rare_series()
    honda_rare_series_extended          = DDFileReader.read_honda_rare_series_extended()
    is_leather_terms                    = DDFileReader.read_is_leather_terms()
    is_sunroof_terms                    = DDFileReader.read_is_sunroof_terms()
    is_sunroof_wildcard_terms           = DDFileReader.read_is_sunroof_wildcard_terms()
    leather_terms_to_nullify            = DDFileReader.read_leather_terms_to_nullify()
    leather_wildcard_terms_to_nullify   = DDFileReader.read_leather_wildcard_terms_to_nullify()
    sunroof_terms_to_nullify            = DDFileReader.read_sunroof_terms_to_nullify()
    vehicle_dao                         = VehicleDAO()

    # The constructor
    def __init__(self, car_data=None):
        if car_data != None:
            self.honda_data = car_data

    # In test case that we want to instantiate the HondaHandler without passing a dictionary of car data
    # We can instead create an instance and set the car data manually
    def set_honda_data(self, honda_car_data):
        self.honda_data = honda_car_data

    # Check if the ad is void
    def is_void(self):

        # Filtering car data through blacklist applies to every make, so return a boolean value representing whether to void the ad
        return self.check_void(
            self.honda_data["title"], 
            self.honda_data["subtitle"], 
            self.honda_data["description"]
        )
        

    # Verify type
    def verify_type(self):
        if self.honda_data["type"] == None:
            print "[+] Honda has no type. Verifying type"
            self.honda_data["type"] = self.find_type()
            print "[+] Figured out type %s" % self.honda_data["type"] 

    # Verify cylinders
    def verify_cylinders(self):
        if self.honda_data["cylinders"] == None:
            self.honda_data["cylinders"] = self.find_cylinders()

    # Verify the drive train
    def verify_drive(self):
        if self.honda_data["drive"] == None:
            self.honda_data["drive"] = self.find_drive()

    # Verify the series
    def verify_series(self):
        self.honda_data["series"], self.honda_data["series_type"] = self.handle_series()

    def verify_model(self):
        if self.honda_data["model"] == None:
            return
        elif self.honda_data["model"] in self.words_notto_hyphenize:
            return
        else:
            self.honda_data["model"] = self.check_missing_hyphen(self.honda_data["model"])

    # Before program execution reaches this point, we will have extracted all the data that was possible for the honda
    # It is here we verify the data we got from the ad.
    def verify(self):
        print "[+] Verifying Honda"
        self.verify_type()
        self.verify_cylinders()
        self.verify_drive()
        self.verify_series()
        self.verify_model()
        self.print_honda_data()

        try:
            if self.is_void():
                self.vehicle_dao.store_in_blacklist(self.honda_data.copy())
                return None
        except Exception as e:
            print "[+] line 92 honda"
            return None

        if self.vehicle_dao.is_unique(self.honda_data["link"]):
            if self.vehicle_dao.duplicate_by_year_price_make_model_odometer_inrange(self.honda_data.copy()):
                print "[+] Found duplicate based on year, price, make, model, and odometer in range. Skipping"
                return

            is_duplicate, original_link = self.vehicle_dao.duplicate_by_year_make_model_odometer_inrange_price_inrange(self.honda_data.copy())

            if is_duplicate:
                print "[+] Found duplicate with odometer in range and price lowered. Storing in human assistance for testing and opening ads."
                self.vehicle_dao.store_duplicate_for_human_assistance(self.honda_data.copy(), original_link)
                self.craigslist_handler.open_craigslist_url_for_duplicate(self.honda_data["link"], original_link)
                self.vauto.handle_honda_bygui(self.honda_data)

            else:
                self.vehicle_dao.store_in_all_vehicles(self.honda_data.copy())
                self.craigslist_handler.open_craigslist_url(self.honda_data["link"])
                self.vauto.handle_honda_bygui(self.honda_data)

        else:
            print "[+] Link is not unique. Comparing ads. Showing what's changed in the ad. Opening the ad if the price has lowered"
            if self.honda_data["price"] == None:
                for i in range(20): print "This should never ever be getting run. Price should always be found from the ad"
            else:
                new_price = int(self.honda_data["price"])
                duplicate_row_data = self.vehicle_dao.get_duplicate_link(self.honda_data["link"])
                duplicate_price = int(duplicate_row_data["price"])
                ad_differences = self.vehicle_dao.compare_ads(self.honda_data.copy(), duplicate_row_data)
                print "[+] Showing What elements of the ad have been updated"
                print ad_differences
                if new_price < duplicate_price:
                    print "[+] Price on ad %s has lowered by %s" % (self.honda_data["link"], duplicate_price - new_price)
                    self.craigslist_handler.open_craigslist_url(self.honda_data["link"])
                    self.vauto.handle_honda_bygui(self.honda_data)






    # Attempts to find the right drive type. Program execution gets here if the drive is not picked up from html parser
    # Meaning if the drive is not picked up from the labels on the right side of the craigslist ad under the subtitle,
    # Then perform a different search
    def find_drive(self):

        # self.search_for_drive is located in the parent car class, and is meant to be usable for all cars.
        # just pass in the title, subtitle, and description of the ad
        drive = self.search_for_drive(
            self.honda_data["title"], 
            self.honda_data["subtitle"], 
            self.honda_data["description"]
        )

        # If the drive is found, return it, otherwise continue on
        if drive != None:
            return drive

        return "fwd"

    # Needs Fix. Implement the cylinder searching
    def find_cylinders(self):
        return "4"

    # Search the title, subtitle, description
    def find_type(self):
        title_args = word_tokenize(self.honda_data["title"])
        subtitle_args = word_tokenize(self.honda_data["subtitle"])
        description_args = word_tokenize(self.honda_data["description"])

        sedan, coupe = "sedan", "coupe"
        for value in self.sedan_identifiers:
            if value in title_args or value in subtitle_args or value in description_args:
                return sedan 

        for v in self.coupe_identifiers:
            if v in title_args or v in subtitle_args or v in description_args:
                return coupe 

        # Default to sedan
        return sedan

    def extract_basic_series_fromlink(self, link):
        url_args = link.split("/")
        for arg in url_args:
            if "-" in arg: 
                title_args = arg.split("-")
                for targ in title_args:
                    if targ in self.honda_basic_series:
                        return targ 
        return None 

    def extract_rare_series_fromlink(self, link):
        url_args = link.split("/")
        for arg in url_args:
            if "-" in arg: 
                title_args = arg.split("-")
                for targ in title_args:
                    if targ in self.honda_rare_series or targ in self.honda_rare_series_extended:
                        return targ 
        return None

    # Search the title, subtitle, and description for a basic series and return it, else return None
    def get_honda_basic_series(self, title, subtitle, description):
        for text in [title, subtitle, description]:
            if text != None:
                basic_series = self.honda_extract_basic_series(text)
                if basic_series != None: return basic_series
       
        return None

    def honda_extract_basic_series(self, string):
        args = word_tokenize(string)
        for i in range(len(args)-1):
            possible_match = args[i] + " " + args[i+1]
            if possible_match in self.honda_basic_series:
                return possible_match.replace(" ", "-").lower()

        for arg in self.honda_basic_series:
            if arg in args:
                return arg

        return None

    # Search title and subtitle for a rare series
    def get_honda_rare_series(self, title, subtitle):
        for text in [title, subtitle]:
            rare_series = self.honda_extract_rare_series(text)
            if rare_series != None: return rare_series 

        return None

    def honda_extract_rare_series(self, string):
        args = word_tokenize(string)
        for rare_series in self.honda_rare_series:
            if rare_series in args:
                return rare_series
        return None

    # Parse the title, subtitle, and description of ad for the series
    # First we search for basic series, if basic_series is not found, then search for rare series.
    # If rare series is none then search for rare_extended series
    def handle_series(self):
        title, subtitle, description = (self.honda_data["title"], self.honda_data["subtitle"], self.honda_data["description"])
        basic_series = self.get_honda_basic_series(title, subtitle, description)
        s, s_type = None, None
        if basic_series != None:
            s, s_type = basic_series, "basic"
        elif basic_series == None:
            rare_series = self.get_honda_rare_series(title, subtitle)
            if rare_series != None:
                s, s_type = rare_series, "rare"
            else:
                rare_series_extended = self.get_honda_rare_series_extended(title, subtitle, description)
                if rare_series_extended != None:
                    s, s_type = rare_series_extended, "rare_series_extended"

        if s == None and s_type == None:

            # Will nullify title, subtitle, and description and search for certain identifiers that mean series
            return self.find_series(title, subtitle, description)
        return s, s_type

    def find_series(self, title, subtitle, description):
        nullified_title = self.nullify_for_series(title)
        nullified_subtitle = self.nullify_for_series(subtitle)
        nullified_description = self.nullify_for_series(description)

        series, series_type = None, None

        print "[+] Original Title: %s" % title
        print "\t[+] Nullified Title: %s" % nullified_title

        print "[+] Original Subtitle: %s" % subtitle
        print "\t[+] Nullified Subtitle: %s" % nullified_subtitle

        print "[+] Original Description: %s" % description
        print "\t[+] Nullified Description: %s" % nullified_description

        is_sunroof_term_present = self.search_for_sunroof(nullified_title, nullified_subtitle, nullified_description)
        is_leather_term_present = self.search_for_leather(nullified_title, nullified_subtitle, nullified_description)

        if is_leather_term_present and is_sunroof_term_present:
            series, series_type = "ex-l", "basic"

        elif is_leather_term_present:
            series, series_type = "ex-l", "basic"

        elif is_sunroof_term_present and not is_leather_term_present:
            series, series_type = "ex", "basic"

        elif not is_sunroof_term_present and not is_leather_term_present:
            print "[+] Did not find sunroof or leather terms. Defaulting to lx"
            series, series_type = "lx", "basic"

        if series == None:
            return None, None

        series = self.check_missing_hyphen(series)
        return series, series_type
    # Use the nltk library to break up the title, subtitle, and description into arrays of words
    # Title, Subtitle, Description are lowercase
    # Then search through the list of words to see if any of the rare extended series words are contained
    def get_honda_rare_series_extended(self, t, s, d):
        args1, args2, args3, = word_tokenize(t), word_tokenize(s), word_tokenize(d)
        for term in self.honda_rare_series_extended:
            if term in args1 or term in args2 or term in args3:
                print "[+] Found rare extended series: %s" % term 
                return term 

        return None

    # Takes in a string and searches the string for leather and sunroof terms to nullify
    # Therefore we can search for proper terms that mean its leather or sunroof, which in return will reveal a series
    def nullify_for_series(self, string):
        for term in self.leather_terms_to_nullify:
            if term in string:
                string = string.replace(term, '')

        for term in self.leather_wildcard_terms_to_nullify:
            if term in string:
                string = string.replace(term, '')

        for term in self.sunroof_terms_to_nullify:
            if term in string:
                string = string.replace(term, '')

        return string

    # Search for terms that mean sunroof in title, subtitle, description
    def search_for_sunroof(self, t, s, d):
        for sunroof_term in self.is_sunroof_terms:
            if sunroof_term in t or sunroof_term in s or sunroof_term in d:
                return True
        return False

    # Search for terms that mean leather in title, subtitle, description
    def search_for_leather(self, t, s, d):
        for term in self.is_leather_terms:
            if term in t or term in s or term in d:
                return True
        return False 

    def print_honda_data(self):
        for k, v in self.honda_data.iteritems():
            if k != "html":
                print k
                print "\t", v
        print "\n"