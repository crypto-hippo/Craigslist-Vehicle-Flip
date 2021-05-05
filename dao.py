import pymysql
import threading
from config import DBConfig

class VehicleDAO(object):

    vehicles_columns = ["subtitle","series_type", "vauto_link", "series", "html", "drive", "size", "type", "title_status", "transmission", "cylinders", "vin", "time_added", "last_modified", "odometer"]
    duplicate_odometer_range = 700
    price_lowered_range = 1000

    def __init__(self):
        pass

    def connect(self):
        self.connection = pymysql.connect(DBConfig.servername, DBConfig.username, DBConfig.password, DBConfig.db)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.connection.close()
        self.cursor.close()

    # Escape the data being inserted into mysql db by pymysql
    def pymysql_escape_dict(self, ad_data):
        for key in ad_data:
            ad_data[key] = self.connection.escape(ad_data[key])
        return ad_data

    def is_unique(self, link):
        self.connect()
        query = "select id from all_vehicles where link = %s"
        self.cursor.execute(query, link)
        result_set = self.cursor.fetchone()
        self.disconnect()
        return result_set == None

    # Delete all rows from db
    def truncate_table(self, table_name):
        self.connect()
        query = "truncate table %s" % table_name
        self.cursor.execute()
        self.disconnect()

    def duplicate_by_year_price_make_model_odometer(self, data):
        self.connect()
        query = "select id from all_vehicles where year = %s and price = %s and make = %s and model = %s and odometer = %s"
        self.cursor.execute(query, (data["year"], data["price"], data["make"], data["model"], data["odometer"]))
        row = self.cursor.fetchone()
        self.disconnect()
        return row != None

    # Return True if year, price, make, model, and odometer is within a valid duplicate odometer range
    def duplicate_by_year_price_make_model_odometer_inrange(self, ad_data):
        try:
            self.connect()
            query = "select odometer, link, price from all_vehicles where year = '%s' and price = '%s' and make = '%s' and model = '%s'" % (ad_data["year"], ad_data["price"], ad_data["make"], ad_data["model"])
            self.cursor.execute(query)
            row = self.cursor.fetchone()
            if row != None:
                old_odometer = int(row[0])
                if ad_data["odometer"] != None:
                    new_odometer = int(ad_data["odometer"])
                    if abs(new_odometer - old_odometer) <= self.duplicate_odometer_range:
                        self.disconnect()
                        return True

            self.disconnect()
            return False
        except Exception as e:
            print str(e), "Line 64 dao"

    def duplicate_by_year_make_model_odometer_inrange_price_inrange(self, ad_data):
        self.connect()
        query = "select link, price, odometer from all_vehicles where year = '%s' and make = '%s' and model = '%s'" % (ad_data["year"], ad_data["make"], ad_data["model"])
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        if row == None:
            return False, None

        else:
            old_odometer = int(row[2])
            if ad_data["odometer"] != None:
                new_odometer = int(ad_data["odometer"])
                if abs(new_odometer - old_odometer) <= self.duplicate_odometer_range:
                    duplicate_price = int(row[1])
                    if ad_data["price"] != None:
                        new_price = int(ad_data["price"])
                        if new_price < duplicate_price:
                            if duplicate_price - new_price <= self.price_lowered_range:
                                self.disconnect()
                                return True, row[0]

            self.disconnect()
            return False, None

    def store_duplicate_for_human_assistance(self, ad_data, original_link):
        try:
            self.connect()
            ad_data = self.pymysql_escape_dict(ad_data)
            ad_data["original_link"] = self.connection.escape(original_link)
            query = "insert into human_assistance (%s) values(%s)" % (",".join(ad_data.keys()), ",".join(ad_data.values()))
            self.cursor.execute(query)
            self.connection.commit()
            print "[+] Stored %s in human_assistance" % ad_data["link"]
        except Exception as e:
            print "[+] Duplicate blacklist link %s" % ad_data["link"]
        finally:
            self.disconnect()

    def store_in_blacklist(self, ad_data):
        try:
            self.connect()
            ad_data = self.pymysql_escape_dict(ad_data)
            query = "insert into vehicles_blacklisted (%s) values(%s)" % (",".join(ad_data.keys()), ",".join(ad_data.values()))
            try:
                self.cursor.execute(query)
                self.connection.commit()
                print "[+] Stored %s into vehicles_blacklisted" % ad_data["link"]

            except Exception as e:
                print "[+] Duplicate blacklist link %s" % ad_data["link"]

            finally:
                self.disconnect()

        except Exception as e:
            print str(e), "Line 106 dao"

    def store_in_all_vehicles(self, ad_data):
        try:
            self.connect()
            ad_data = self.pymysql_escape_dict(ad_data)
            query = "insert into all_vehicles (%s) values(%s)" % (",".join(ad_data.keys()), ",".join(ad_data.values()))
            self.cursor.execute(query)
            self.connection.commit()
            self.disconnect()
            print "[+] Stored %s into all_vehicles" % ad_data["link"]

        except Exception as e:
            print str(e), "Line 114 dao"

    # This method takes in 2 dictionaries of data and checks to see what has changed
    def compare_ads(self, dict_1, dict_2):
        changes = []
        for key in dict_1:
            if dict_2[key] != dict_1[key]:
                changes.append(key)
        return changes

    def get_duplicate_link(self, link):
        query = "select * from all_vehicles where link = %s"
        self.connect()
        self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        self.cursor.execute(query, link)
        duplicate_row = self.cursor.fetchone()
        self.disconnect()
        return duplicate_row

    def update_price(self, link, new_price, old_price):
        query = "update all_vehicles set price = %s where link = %s"
        self.connect()
        self.cursor.execute(query, (new_price, link))
        self.disconnect()

    def price_lowered(self, link, new_price):
        query = "select price from all_vehicles where link = %s"
        self.connect()
        self.cursor.execute(query, link)
        old_price = self.cursor.fetchone()[0]
        self.disconnect()
        print "[+] Comparing prices: new: %s, old: %s" % (new_price, old_price)
        if new_price < int(old_price) and (int(old_price) - new_price) > 200:
            print "[+] Price has lowered from %s to %s. Updating link in the db: %s" % (old_price, new_price, link)
            self.update_price(link, new_price, old_price)
            return True
        return False









