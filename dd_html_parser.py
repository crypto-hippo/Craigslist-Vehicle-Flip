from bs4 import BeautifulSoup
from dao import VehicleDAO
import time
import sys
import traceback
from nltk.tokenize import sent_tokenize, word_tokenize

# The html parser. Don't waste time with regexp, just use something beautiful ^
class DTDHtmlParser(object):

    def __init__(self):
        self.subtitle = None

    def set_parser(self, html):
        self.html_parser = BeautifulSoup(html, 'html.parser')

    def get_ad_links(self, html):
        self.set_parser(html)
        links = []
        ad_links = self.html_parser.find_all('a', class_="result-image")
        for ad in ad_links:
            try:
                links.append({
                    "link": str(ad["href"]),
                    "price": ad.find("span", class_="result-price").text.split("$")[1]
                })

            except Exception as e:
                print str(e)
                print "[+] Ad does not have correct price. Continuing"
                continue

        return links

    def get_title(self):
        title_only_tag = self.html_parser.find("span", {"id": "titletextonly"})
        return str(title_only_tag.getText().encode("utf-8")).lower() if title_only_tag != None else None

    def get_price(self):
        price_tag = self.html_parser.find("span", {"class": "price"})
        return str(price_tag.getText().encode("utf-8")).split("$")[1] if price_tag != None else None

    def get_image_links(self):
        img_thumbs_container = self.html_parser.find("div", {"id":"thumbs"})
        if img_thumbs_container is None:
            return None 

        images = img_thumbs_container.find_all("a", {"class":"thumb"})
        return ",".join([ str(link["href"]) for link in images ])

    def get_city(self, url):
        city_from_url = url.split("//")[1].split(".")[0]
        return city_from_url.lower()

    def is_valid_year(self, string):
        try:
            year = int(string[:4])
            return True

        except Exception as e:
            return False

    def get_year_make_model(self, subtitle):
        args = subtitle.split(" ")
        year, make, model = None, None, None
        if len(args) > 2:
            year = args[0]
            make = args[1].lower()
            model = args[2].lower()
        elif len(args) == 2:
            year = args[0]
            make = args[1].lower()
        elif len(args) == 1:
            print "[-] Subtitle only contains 1 element %s" % args[0]

        return (year, make, model)

    def organize_attr_group_data(self):
        self.current_attr_groups = {}
        try:
            attr_groups = self.html_parser.find_all("p", {"class": "attrgroup"})
            for ptag in attr_groups:
                span_tags = ptag.find_all("span")

                for stag in span_tags:
                    inner_string = str(stag.getText().encode("utf-8")).lower()
                    inner_string_args = inner_string.split(": ")

                    if len(inner_string_args) == 1 and self.is_valid_year(inner_string):
                        year, make, model = self.get_year_make_model(inner_string)

                        self.subtitle = inner_string
                        self.current_attr_groups["year"] = year 
                        self.current_attr_groups["make"] = make
                        self.current_attr_groups["model"] = model
                        self.current_attr_groups["subtitle"] = self.subtitle 

                    elif len(inner_string_args) == 2:

                        data_label, data_value = inner_string_args
                        print data_label, data_value

                        if data_label == "condition":
                            self.current_attr_groups["vehicle_condition"] = data_value.lower()

                        elif data_label == "fuel":
                            self.current_attr_groups["fuel"] = data_value.lower()

                        elif data_label == "odometer":
                            self.current_attr_groups["odometer"] = data_value

                        elif data_label == "paint color":
                            self.current_attr_groups["paint_color"] = data_value.lower()

                        elif data_label == "vin":
                            self.current_attr_groups["vin"] = data_value.lower()

                        elif data_label == "cylinders":
                            self.current_attr_groups["cylinders"] = ''.join([ letter for letter in data_value if letter.isdigit() ])

                        elif data_label == "transmission":
                            self.current_attr_groups["transmission"] = data_value.lower()

                        elif data_label == "title status":
                            self.current_attr_groups["title_status"] = data_value.lower()

                        elif data_label == "type":
                            self.current_attr_groups["type"] = data_value.lower()

                        elif data_label == "size":
                            self.current_attr_groups["size"] = data_value.lower()

                        elif data_label == "drive":
                            self.current_attr_groups["drive"] = data_value.lower()

                        else:
                            print "[+] craigslist ad label condition not being tested for. html_parser 125"
                            print (data_label, data_value)

        except Exception as e:
            print str(e)
            pass

    def get_description(self):
        description = self.html_parser.find("section", {"id":"postingbody"})
        if description is None:
            return None 

        description_encoded = description.getText().encode('utf-8')
        split_by_newline = str(description_encoded).split("\n")
        clean_text = " ".join(split_by_newline).strip()

        return clean_text.lower()


    def prepare_data_for_db(self, data):
        for value in VehicleDAO.vehicles_columns:
            if not data.has_key(value):
                data[value] = None
        return data

    def get_ad_data(self, html, link):
        self.set_parser(html)
        self.organize_attr_group_data()
        current_time = int(time.time())
        data = {
            "price": self.get_price(),
            "title": self.get_title(),
            "images": self.get_image_links(),
            "description": self.get_description(),
            "city": self.get_city(link),
            "html": str(self.html_parser),
            "link": link,
            "time_added": current_time,
            "last_modified": current_time
        }
        data.update(self.current_attr_groups)

        # The html parser grabs all the data it can in a way suited for craigslist.
        # Variable 'data' above is the beginning data stored in the database The keys in data match up the colums of the vehicle db
        # This data is passed on and manipulated further based on each Type of car handler modifying it
        # Therefore any columns in VehicleDao.columns that don't exist as keys in data will be added and set to None. Cheers
        # This reduces code for future development
        data = self.prepare_data_for_db(data)
        return data
