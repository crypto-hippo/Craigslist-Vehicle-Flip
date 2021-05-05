from craigslist_handler import CraigslistHandler
from dd_file_reader import DDFileReader
import sys

from vauto_handler import VautoHandler

reload(sys)
sys.setdefaultencoding("utf8")

class Car(object):
    global_blacklist_values             = DDFileReader.read_global_blacklist_values()
    global_blacklist_values_to_nullify  = DDFileReader.read_global_blacklist_values_to_nullify()
    is_awd_terms                        = DDFileReader.read_is_awd_terms()
    awd_terms_to_nullify                = DDFileReader.read_awd_terms_to_nullify()
    words_notto_hyphenize              = ["fit"]
    vauto = VautoHandler()
    craigslist_handler = CraigslistHandler()

    def nullify_for_blacklist(self, t, s, d):
        tc, sc, dc = t, s, d  
        blacklist_terms_to_nullify = Car.global_blacklist_values_to_nullify

        for term in blacklist_terms_to_nullify:
            if term in tc:
                tc = tc.replace(term, '')
            if term in sc:
                sc = sc.replace(term, '')
            if term in dc:
                dc = dc.replace(term, '')

        return tc, sc, dc 

    def nullify_for_drive(self, t, s, d):
        tc, sc, dc = t, s, d 
        for term in Car.awd_terms_to_nullify:
            if term in tc:
                tc = tc.replace(term, '')
            if term in sc:
                sc = sc.replace(term, '')
            if term in dc:
                dc = dc.replace(term, '')
        return tc, sc, dc

    def search_for_drive(self, t, s, d):
        tc, sc, dc, = self.nullify_for_drive(t, s, d)
        for term in Car.is_awd_terms:
            if term in tc or term in sc or term in dc:
                return "awd"
        return None

    def check_void(self, title, subtitle, description):
        blacklist_values = Car.global_blacklist_values
        
        # Nullify the blacklist before we search for blacklist values
        null_title, null_subtitle, null_description = self.nullify_for_blacklist(title, subtitle, description)

        for value in blacklist_values:
            if value in null_title:
                print "[+] Found blacklist value %s in %s" % (value, null_title)
                return True

            elif value in null_subtitle:
                print "[+] Found blacklist value %s in %s" % (value, null_subtitle)
                return True 

            elif value in null_description:
                print "[+] Found blacklist value %s in %s" % (value, null_description)
                return True

        return False

    def check_missing_hyphen(self, text):
        if len(text) == 3 and "-" not in text:
            text = text[:2] + "-" + text[2:3]
        return text



