class WebsiteAutomater(object):
    """
        Parent class of Handler classes that use selenium, The handlers will be
        Classes that are specifically made for each website it automates. Common functionality
        Shared among all website handlers will be here
    """
    firefox_drivers = []

    @classmethod
    def get_current_window_handle_index(cls, firefox_driver):
        window_handle = firefox_driver.current_window_handle
        index = firefox_driver.window_handles.index(window_handle)
        return index

    @classmethod
    def add_firefox_driver(cls, firefox_driver):
        cls.firefox_drivers.append(firefox_driver)

    @classmethod
    def get_vauto_inputs(cls, firefox_driver):
        return {
            "odometer": firefox_driver.find_element_by_id("Odometer"),
            "year": firefox_driver.find_element_by_id("ModelYear"),
            "make": firefox_driver.find_element_by_id("Make"),
            "model": firefox_driver.find_element_by_id("Model"),
            "series": firefox_driver.find_element_by_id("Series"),
            "type": firefox_driver.find_element_by_id("BodyType"),
            "cylinders": firefox_driver.find_element_by_id("EngineCylinderCount"),
            "transmission": firefox_driver.find_element_by_id("TransmissionType"),
            "paint_color": firefox_driver.find_element_by_id("ExteriorColor"),
        }







