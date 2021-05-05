import time
import traceback
from selenium.webdriver.common.keys import Keys
from selenium                       import webdriver
from config                         import VautoConfig
from dd_file_reader import DDFileReader
from dd_website_automater           import WebsiteAutomater

class VautoHandler(WebsiteAutomater):

    def __init__(self):
        self.data_not_correct   = False
        self.logged_in          = False
        self.vauto_login_url    = "https://www2.vauto.com/Va/Share/Login.aspx?redirect=636390026881069419&ReturnUrl=%2fVa%2fAppraisal%2fDefault.aspx%3fnew%3dtrue&new=true"
        self.vauto_loggedin_url = "https://www2.vauto.com/Va/Appraisal/Default.aspx?new=true"
        self.input_timer        = 2
        self.firefox_drivers    = []
        self.current_driver     = None
        self.vauto_tab_counter  = 0
        self.loading_wait_time  = 2

    # Only instantiate firefox webdriver if we haven't already
    def connect_firefox(self):
        if self.current_driver == None:
            self.firefox_profile = webdriver.FirefoxProfile("C:\Users\dylan\AppData\Roaming\Mozilla\Firefox\Profiles\joxqxckv.default")
            self.firefox_profile.profile_dir = "C:\Users\dylan\AppData\Roaming\Mozilla\Firefox\Profiles\joxqxckv.default"
            self.current_driver = webdriver.Firefox(self.firefox_profile)
            self.set_browser_size(727, 0, 804, 1038)
            self.firefox_drivers.append(self.current_driver)

    def set_browser_size(self, x, y, width, height):
        self.current_driver.set_window_position(x, y)
        self.current_driver.set_window_size(width, height)

    # In test case that we want to iterate through an array of input elements and clear the value
    def clear_inputs(self, input_elements):

        for key, input_element in input_elements.iteritems():
            try:
                input_element.clear()
            except Exception as e:
                print str(e)
                continue

    def click_go(self):

        # Click the go btn by executing javascript. Problem is that the javascript will run asynchronous to my program
        # self.current_driverexecute_script("document.getElementById('ext-gen153').click()")
        # Click the go button without javascript
        go_btn = self.current_driver.find_element_by_id("VehicleApplyButton")
        go_btn.click()

    def validate_inputs(self, car_data, with_vin=False):
        pass
        # model = self.current_driver.find_element_by_id("Model")
        # model_text = model.get_attribute("value")
        #
        # if model_text == '' and car_data["model"] != None:
        #     model.send_keys(car_data["model"])
        #     model.send_keys(Keys.ENTER)
        #
        # series = self.current_driver.find_element_by_id("series")
        # series_text = series.get_attribute("value")
        # if series_text == '' and car_data["series"] != None:
        #     series.send_keys(car_data["series"])
        #     series.send_keys(Keys.ENTER)


    def wait_for_elements_loading(self):
        self.wait_for_bodytype_loading()
        self.wait_for_model_loading()
        self.wait_for_series_loading()

    # If the car data contains a value for odometer
    # We add 2k miles to the original value and send that value into the input field in vauto
    def handle_odometer(self, data, input_elements):
        if data["odometer"] != None and data["odometer"].isdigit():
            odometer = str(int(data["odometer"]) + 2000)
            input_elements["odometer"].send_keys(odometer)
        else:
            print "[+] Odometer was not found on ad. We should probably skip"

    # Input the year into vauto
    def handle_year(self, data, input_elements):
        input_elements["year"].send_keys(data["year"])

    # Input the make into vauto
    def handle_make(self, data, input_elements):
        if data["make"] != None:
            input_elements["make"].send_keys(data["make"].capitalize())
            time.sleep(0.2)
            input_elements["make"].send_keys(Keys.ENTER)
            self.wait_for_elements_loading()

    # Input the model
    def handle_model(self, data, input_elements):
        if data["model"] != None:
            input_elements["model"].send_keys(data["model"])
            time.sleep(self.loading_wait_time)
            input_elements["model"].send_keys(Keys.ENTER)
            self.wait_for_elements_loading()

    # Input the series
    def handle_series(self, data, input_elements):
        if data["series"] != None:
            input_elements["series"].send_keys(data["series"])
            time.sleep(self.loading_wait_time)
            input_elements["series"].send_keys(Keys.ENTER)
            self.wait_for_elements_loading()

    # The body type is usually autofilled by vauto based on entering the previous data.
    # Therefore in order to take advantage of vauto we check to see if vauto has already 
    # Inputted data and if so we leave it
    def handle_type(self, data, input_elements):
        if data["type"] != None:
            current_value = input_elements["type"].get_attribute("value")
            if current_value == '':
                input_elements["type"].send_keys(data["type"])
                time.sleep(self.loading_wait_time)
                input_elements["type"].send_keys(Keys.ENTER)

    # If the cylinders were found then check the current value to see if vauto autofilled it.
    # Then remove the whitespace and input the digit into vauto if its a digit
    # If the value for cylinders is not a digit. Then print out a message that the cylinders was not parsed correctly
    def handle_cylinders(self, data, input_elements):
        current_value = input_elements["cylinders"].get_attribute("value")
        if current_value == '' and data["cylinders"] != None:
            cylinders = data["cylinders"].strip()
            if cylinders.isdigit():
                input_elements["cylinders"].send_keys(cylinders)
                time.sleep(self.loading_wait_time)
                input_elements["cylinders"].send_keys(Keys.ENTER)
            else:
                print "[+] Number of cylinders was not parsed from html correctly"

    # The transmission input field in vauto is usually autofilled by vauto.
    # Therefore we must check its value and if no value then send the transmission value
    # If the transmission was not received from parsing the html, or searching, then
    # Default to automatic
    def handle_transmsission(self, data, input_elements):
        current_value = input_elements["transmission"].get_attribute("value")
        if current_value == '':
            if data["transmission"] == None:
                input_elements["transmission"].send_keys("automatic")
            else:
                input_elements["transmission"].send_keys(data["transmission"])

            time.sleep(0.2)
            input_elements["transmission"].send_keys(Keys.ENTER)

    def set_distance(self, distance):
        self.wait_for_rbook_loading()
        distance_element = self.current_driver.find_element_by_name("distanceCombo")
        distance_element.clear()
        distance_element.send_keys(distance) 
        if distance_element.get_attribute("value") == distance:
            print "[+] Distance Element successfully set to %s" % distance

    def handle_body_type_checklist(self, data, rbook_data):
        pass

    def extract_checkbox_label(self, checkbox_dom_element):
        text_and_count = checkbox_dom_element.find_element_by_css_selector(".label.optionLabel").text
        if text_and_count == None:
            return

        index_of_digit = 0
        for i in range(len(text_and_count)):
            if text_and_count[i].isdigit():
                index_of_digit = i 
        text, count = text_and_count[:index_of_digit], text_and_count[index_of_digit:]
        return text, count

    def uncheck_rbook_elements(self, rbook_data):
        for k, v in rbook_data.iteritems():
            if k != "Series:":
                checkboxes = v["dom_elements"]
                for checkbox in checkboxes:
                    if "va-checkbox-checked" in checkbox.get_attribute("class"):
                        checkbox.click()

    def uncheck_all_checked_boxes_for_rbook(self, rbook_data):
        while self.rbook_has_checked_boxes(rbook_data):
            print "[+] Unchecking all rbook checklist"
            self.uncheck_rbook_elements(rbook_data)
            self.wait_for_rbook_loading()

        print "[+] Rbook Should not have any checked boxes"

    def appraise_blackbook(self, car_data):
        print "[+] Appraising BlackBook"

    def negotiate_prices(self, car_data):
        print "[+] Negotiating Prices"

    # Collect all the vauto input boxes that we need for inputting data to vauto
    def gather_vauto_inputs(self):
        return WebsiteAutomater.get_vauto_inputs(self.current_driver)

    # Collect the appropriate form inputs and send the username and password from our config file and click login
    def enter_login_details_and_click_go(self):
        username_input_element = self.current_driver.find_element_by_id("X_PageBody_ctl00_ctl00_Login1_UserName")
        username_text = username_input_element.get_attribute("value")
        if username_text == '':
            username_input_element.send_keys(VautoConfig.username)
        password_input_element = self.current_driver.find_element_by_id("X_PageBody_ctl00_ctl00_Login1_Password")
        login_btn = self.current_driver.find_element_by_id("X_PageBody_ctl00_ctl00_Login1_LoginButton")
        password_input_element.send_keys(VautoConfig.password)
        login_btn.click()

    # Handle creating a new tab or initial login
    def login_vauto(self):
        self.connect_firefox()

        # The current url attribute of selenium webdriver object is equal to about:blank when empty.
        # In test case of a new tab. The current url will either be a url or about:newtab 
        if self.current_driver.current_url == "about:blank":
            self.handle_initial_page()

        else:
            self.load_new_vauto_tab()

    def wait_for_newtab_loading(self, num_old_window_handles):
        while not len(self.current_driver.window_handles) > num_old_window_handles:
            time.sleep(0.1)

    # Load a new tab
    def load_new_vauto_tab(self):
        num_old_window_handles = len(self.current_driver.window_handles)
        self.current_driver.execute_script("window.open()")
        self.wait_for_newtab_loading(num_old_window_handles)
        last_window_handler = self.current_driver.window_handles[-1]
        self.current_driver.switch_to_window(last_window_handler)
        self.current_driver.get(self.vauto_loggedin_url)
        self.vauto_tab_counter += 1
        self.current_driver.execute_script("document.title = '%s Vauto'" % self.vauto_tab_counter)

    # Handle the initial login to vauto.
    def handle_initial_page(self):
        self.current_driver.get(self.vauto_loggedin_url)
        if "/Va/Share/Login.aspx?" in self.current_driver.current_url:
            self.enter_login_details_and_click_go()
        else:
            self.load_new_vauto_tab()

    def handle_honda_bygui(self, honda_data, duplicate=False):
        self.login_vauto_bygui()

        # If the passed in honda car data has a vin then we handle the vin. Otherwise we forget about the vin
        if honda_data["vin"] != None:
            self.handle_honda_with_vin(honda_data)
        else:
            self.handle_honda_without_vin(honda_data)

    def handle_honda_without_vin(self, honda_data):
        print "[+] Handling honda without vin"
        try:
            # odometer = honda_data["odometer"]
            # if odometer != None and odometer.isdigit():
            #     odometer_input_field = self.current_driver.find_element_by_id("Odometer")
            #     odometer_input_field.send_keys(odometer)
            #
            # year = honda_data["year"]
            # if year != None and year.isdigit():
            #     year_input_field = self.current_driver.find_element_by_id("ModelYear")
            #     year_input_field.send_keys(year)

            input_elements = WebsiteAutomater.get_vauto_inputs(self.current_driver)
            self.handle_odometer(honda_data, input_elements)
            self.handle_year(honda_data, input_elements)
            self.handle_make(honda_data, input_elements)
            self.handle_model(honda_data, input_elements)
            self.handle_series(honda_data, input_elements)
            self.handle_type(honda_data, input_elements)
            self.handle_cylinders(honda_data, input_elements)
            self.handle_transmsission(honda_data, input_elements)

            self.validate_inputs(honda_data)
            self.click_go()
            self.appraise_blackbook(honda_data)
            self.negotiate_prices(honda_data)

        except Exception as e:
            tb = traceback.format_exc()
            print tb

    def handle_honda_with_vin(self, honda_data):
        print "[+] Handling honda with vin"
        try:
            vin_input_element = self.current_driver.find_element_by_id("Vin")
            vin_input_element.send_keys(honda_data["vin"])

            odometer = self.current_driver.find_element_by_id("Odometer")
            odometer.send_keys(str(int(honda_data["odometer"]) + 2000))

            counter = 0
            while True:
                try:
                    classes = vin_input_element.get_attribute("class")
                    if "x-form-invalid" in classes and vin_input_element.get_attribute("value") != '':
                        print "[+] Invalid Vin. "
                        vin_input_element.clear()
                        odometer.clear()
                        self.handle_honda_without_vin(honda_data)
                        break

                    else:
                        if counter == 10:
                            self.validate_inputs(WebsiteAutomater.get_vauto_inputs(self.current_driver), with_vin=True)
                            self.click_go()
                            self.appraise_blackbook(honda_data)
                            self.negotiate_prices(honda_data)
                            break

                        counter += 1

                    time.sleep(0.3)

                except Exception as e:
                    print str(e)
                    break


        except Exception as e:
            print "[+] Encountered Exception from handling honda with vin"
            print str(e)

    def login_vauto_bygui(self):
        try:
            self.connect_firefox()
            if self.current_driver.current_url == "about:blank":
                self.current_driver.get(self.vauto_loggedin_url)
                if "/Va/Share/Login.aspx?" in self.current_driver.current_url:
                    self.enter_login_details_and_click_go()
                    self.current_driver.execute_script("document.title = '%s vauto'" % self.vauto_tab_counter)
                else:
                    print "[+] Logged in to vauto. #winning"

            else:
                self.load_new_vauto_tab()

        except Exception as e:
            print str(e)
            print "[+] Exception encountered while loading firefox tab"

    # Vauto is weird and buggy. We need a way to check if vauto is still loading when inputting data into vehicle fields

    # That way we know when to make another interactable
    # Pass in a dom element and for that dom element, check the va-label-spinner that's loading on the next element
    # So we now know when to input the next set of car data
    def wait_for_model_loading(self):

        try:
            model_loading_circle = self.current_driver.find_element_by_css_selector("#ext-gen168 .va-label-spinner")
            while model_loading_circle.value_of_css_property("visibility").lowercase() == "visible":
                time.sleep(self.loading_wait_time)

        except Exception as e:
            pass

    def wait_for_series_loading(self):
        try:
            series_loading_circle = self.current_driver.find_element_by_css_selector(
                "#ext-gen597 .va-label-spinner")
            while series_loading_circle.value_of_css_property("visibility").lowercase() == "visible":
                time.sleep(self.loading_wait_time)

        except Exception as e:
            print str(e)

    def wait_for_bodytype_loading(self):
        try:
            body_type_loading_circle = self.current_driver.find_element_by_css_selector(
                "#ext-gen590 .va-label-spinner")
            while body_type_loading_circle.value_of_css_property("visibility").lowercase() == "visible":
                time.sleep(self.loading_wait_time)

        except Exception as e:
            print str(e)

    def wait_for_rbook_loading(self):
        try:
            rbook_panel = self.current_driver.find_element_by_id("Radar-view-23")
            loading_element = rbook_panel.find_element_by_css_selector(".x-tool.x-tool-loading")
            while loading_element.value_of_css_property("display") == "block":
                time.sleep(self.loading_wait_time)

        except Exception as e:
            pass

    # Checks to see if the rbook panel is open
    def is_rbook_open(self):
        rbook_panel_container = self.current_driver.find_element_by_id("ext-gen355")
        css_display_property = rbook_panel_container.value_of_css_property("display")
        if css_display_property == "none":
            return False
        elif css_display_property == "block":
            return True

            # Opens rbook panel

    def open_rbook(self):
        # The id of the html element for the rbook top level node that opens up rbook in vauto
        # #Radar-view-23
        rbook_panel = self.current_driver.find_element_by_id("Radar-view-23")
        rbook_panel.click()
        time.sleep(self.input_timer)

    def rbook_has_checked_boxes(self, rbook_data):
        for key, value in rbook_data.iteritems():
            if key != "Series:":
                for checkbox in value["dom_elements"]:
                    if "va-checkbox-checked" in checkbox.get_attribute("class"):
                        print "[+] checkbox is checked"
                        return True

        return False

    # Gets the rbook column titles as keys, and the value is a dict with one key "dom_elements" and the value of "dom_elements" is an array of the checkboxes for that title
    def get_rbook_checklist(self):
        current_rbook_option_fields = self.current_driver.find_elements_by_css_selector(".fields.standardFields .optionField")
        rbook_data = {}
        for dom_element in current_rbook_option_fields:
            title = dom_element.find_element_by_class_name("optionFieldLabel").text
            checklist_values = dom_element.find_elements_by_css_selector(".options .optionList li a")
            if checklist_values != None:
                print "[+] Found %s checklist values for %s" % (len(checklist_values), title)
                rbook_data[title] = {"dom_elements": checklist_values}
        return rbook_data

    def appraise_rbook(self, honda_data):
        pass


