from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from dd_website_automater import WebsiteAutomater
import time

class CraigslistHandler(WebsiteAutomater):

    def __init__(self):
        self.current_driver_set = False
        self.tab_counter = 0
        self.firefox_drivers = []
        self.current_driver = None
        self.craigslist_tab_counter = 0

    def connect_firefox(self):
        if self.current_driver == None:
            self.firefox_profile = webdriver.FirefoxProfile("C:/Users/dylan/AppData/Roaming/Mozilla/Firefox/Profiles/joxqxckv.default")

            # This is a hack and is the coolest thing.
            self.firefox_profile.profile_dir = "C:/Users/dylan/AppData/Roaming/Mozilla/Firefox/Profiles/joxqxckv.default"

            self.current_driver = webdriver.Firefox(self.firefox_profile)

            # vauto: 1027, 0, 904, 1038, craigslist: -17, 0, 1061, 1038
            self.current_driver.set_window_position(-17, 0)
            self.current_driver.set_window_size(757, 1038)
            self.firefox_drivers.append(self.current_driver)

    def open_craigslist_url(self, url):
        self.connect_firefox()
        if self.is_initial_window():
            self.current_driver.get(url)
            self.current_driver.execute_script("document.title = '%s lead'" % self.craigslist_tab_counter)
        else:
            num_old_current_window_handles = len(self.current_driver.window_handles)
            # Since body.send_keys(Keys.CONTROL + 't') is not working anymore for creating new tabs.
            # We are executing javascript to open a new tab. This will ad a new window handle to driver.window_handles
            self.current_driver.execute_script("window.open()")

            # This code waits for the javascript to finish loading before it switches windows
            while not (len(self.current_driver.window_handles) > num_old_current_window_handles):
                time.sleep(0.1)

            self.craigslist_tab_counter += 1
            self.current_driver.switch_to_window(self.current_driver.window_handles[-1])
            self.current_driver.get(url)
            self.current_driver.execute_script("document.title = '%s lead'" % self.craigslist_tab_counter)
            print "[+] Current driver index: %s" % self.craigslist_tab_counter

    def load_new_tab(self, url):
        num_window_handles_before = len(self.current_driver.window_handles)
        self.current_driver.execute_script("window.open();")
        self.wait_for_newtab_loading(num_window_handles_before)
        self.current_driver.switch_to_window(self.current_driver.window_handles[-1])
        self.current_driver.get(url)
        self.craigslist_tab_counter += 1
        self.current_driver.execute_script("document.title = '%s lead'" % self.craigslist_tab_counter)

    def load_duplicate_tab(self, url):
        num_window_handles_before = len(self.current_driver.window_handles)
        self.current_driver.execute_script("window.open();")
        self.wait_for_newtab_loading(num_window_handles_before)
        self.current_driver.switch_to_window(self.current_driver.window_handles[-1])
        self.current_driver.get(url)

        js = "document.title = '(%s Duplicate) Comapre Ads'; document.body.style.background = '#ffff66'" % self.craigslist_tab_counter
        self.current_driver.execute_script(js)

    def open_craigslist_url_for_duplicate(self, url, original_link):
        self.connect_firefox()
        if self.is_initial_window():
            self.handle_initial_window(url, duplicate=True)
            self.load_duplicate_tab(original_link)

        else:
            self.load_new_tab(url)
            self.load_duplicate_tab(original_link)

        print "[+] Current driver index: %s" % self.craigslist_tab_counter

    def handle_initial_window(self, url, duplicate=False):
        self.current_driver.get(url)
        if duplicate:
            self.current_driver.execute_script("document.title = '(%s Duplicate) lead'" % self.craigslist_tab_counter)
        else:
            self.current_driver.execute_script("document.title = '%s lead'" % self.craigslist_tab_counter)

    def wait_for_newtab_loading(self, num_window_handles_before):

        # This code waits for the javascript to finish loading before it switches windows
        while not (len(self.current_driver.window_handles) > num_window_handles_before):
            time.sleep(0.1)

    def is_initial_window(self):
        return self.current_driver.current_url == "about:blank"

    def is_new_tab(self):
        return self.current_driver.current_url == "about:newtab"

    def open_original_link(self, original_link):
        pass