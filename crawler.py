import requests
import re
import time
import random
import selenium
import sys
import traceback
import timeit
import threading
import editdistance

from selenium import webdriver
from dao import VehicleDAO
from dodge_handler import DodgeHandler
from regexp import RegexpHandler
from dd_html_parser import DTDHtmlParser
from dd_logger import DDLogger 
from honda_handler import HondaHandler
from vauto_handler import VautoHandler
from subaru_handler import SubaruHandler
from chevrolet_handler import ChevroletHandler
from ford_handler import FordHandler
from gmc_handler import GMCHandler

regexp_handler = RegexpHandler()
chrome_driver_executable = "c:/users/dylan/desktop/chromedriver.exe"

# The Engine
class Crawler(object):

    """ Web Crawler """
    def __init__(self):

        # Objects that the crawler depends on
        self.handler = None
        self.vehicle_dao = VehicleDAO()
        self.html_parser = DTDHtmlParser()
        self.logger = DDLogger()

        # Declare variables used in searching so new objects aren't constantly being created on every iteration
        self.substituted_query_params = None
        self.next_link = None
        self.next_link_with_pagination = None
        self.current_html_get_response = None 
        self.current_html = None
        self.current_ad_links = None 
        self.current_ad_data = {}
        self.current_links_crawled_length = 0
        self.is_ad_unique = None

        # Make sure the key value is also stored every time
        self.make_mispellings = {
            "honda": ["honda", "hoda", "hnda"],
            "subaru": ["subaru", "suburu", "soboru", "suboru"]
        }

    def is_valid_link(self, ad_link):
        print "[+] Validating Link: %s" % ad_link
        if ad_link.startswith("/"):
            print "[+] Link did not pass validation"
            return False

        print "[+] Link passed validation"
        return True

    def is_valid_odometer(self, odometer):
        if odometer >= 103 and odometer <= 350:
            return False
        return True

    def validate_odometer(self, ad_data):
        if ad_data["odometer"] != None and ad_data["odometer"].isdigit() and len(ad_data["odometer"]) <= 3:
            ad_data["odometer"] += "000"

    def extract_ad_data(self, ad_link):
        if not self.is_valid_link(ad_link):
            return None
        else:
            try:
                resp = requests.get(ad_link)
                html = resp.content
                ad_data = self.html_parser.get_ad_data(html, ad_link)
                return ad_data
            except Exception as e:
                print "[+] crawler.py line 53. Skipping because crawler threw an exception while requesting data from link"
                print str(e)
                return None


    def make_is_match(self, key, possible_match):
        return possible_match in self.make_mispellings[key]

    def handle_make(self, ad_data):
        try:

            if not self.is_valid_odometer(int(ad_data["odometer"])):
                return

            self.validate_odometer(ad_data)

            make_found = ad_data["make"]
            if make_found != None:
                make_found = make_found.strip()

            if self.make_is_match("honda", make_found):
                honda = HondaHandler(car_data=ad_data)
                honda.verify()
                self.handler = honda

            elif self.make_is_match("subaru", make_found):
                subaru = SubaruHandler(car_data=ad_data)
                subaru.verify()
                self.handler = subaru

            elif make_found == "chevrolet":
                chevy = ChevroletHandler(ad_data)
                chevy.verify()
                self.handler = chevy

            elif make_found == "ford":
                ford = FordHandler(ad_data)
                ford.verify()
                self.handler = ford

            elif make_found == "dodge":
                dodge = DodgeHandler(ad_data)
                dodge.verify()
                self.handler = dodge

            elif make_found == "gmc":
                gmc = GMCHandler(ad_data)
                gmc.verify()
                self.handler = gmc

        except Exception as e:
            print str(e)

    def filter_duplicates(self, links_found):
        links_filtered = []
        for link_data in links_found:
            if self.vehicle_dao.is_unique(link_data["link"]):
                links_filtered.append(link_data)

            elif self.vehicle_dao.price_lowered(link_data["link"], int(link_data["price"])):
                links_filtered.append(link_data)

        return links_filtered

    def crawlCraigslistUrl(self, search_url):

        # This method will get all the links and set the maximum pagination value
        self.all_ad_links_found = self.collect_all_ad_links(search_url)
        self.all_ad_links_found = self.filter_duplicates(self.all_ad_links_found)

        print "[+] Found %s links after filtering" % len(self.all_ad_links_found)
        for link_data in self.all_ad_links_found:
            print "##############################################\n\nNew Link Logging ->\n"
            print "[+] Starting Flip: %s" % link_data["link"]
            ad_data = self.extract_ad_data(link_data["link"])
            if ad_data != None:
                self.handle_make(ad_data)

            time.sleep(2)

        print "[+] Program is done Opening ads and inputting data. "
        if self.handler != None and self.handler.vauto.current_driver != None:
            self.handler.vauto.current_driver.execute_script("""
                alert('FlipperCars is Done!!! #Winning')
            """)

    def collect_all_ad_links(self, search_url):
        html = requests.get(search_url).content
        try:
            self.pagination_counter = int(regexp_handler.get_pagination_totalcount(html))
        except Exception as e:
            print "[+] Problem finding pagination counter. Defaulting to 2000"
            self.pagination_counter = 2000

        pagination_start = 0
        all_ads_found = []
        while pagination_start < self.pagination_counter:
            if pagination_start == 0:
                all_ads_found += self.html_parser.get_ad_links(html)

            else:
                search_url = search_url.replace("?", '?s=%s&' % pagination_start)
                all_ads_found += self.html_parser.get_ad_links(html)

            pagination_start += 120
            time.sleep(2)

        return all_ads_found

    def start_crawl_v1(self, search_url):
        print "crawling v1 baby"
        self.crawlCraigslistUrl(search_url)



