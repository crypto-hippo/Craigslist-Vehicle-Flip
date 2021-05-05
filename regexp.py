import re

class RegexpHandler(object):

    def __init__(self):
        self.pagination_total_count_regexp = re.compile('<span class="totalcount">(.*?)</span>')

    def get_pagination_totalcount(self, html):
        match = self.pagination_total_count_regexp.search(html)
        if match: 
            return match.groups(0)[0]
        else:
            print "--------pagination not found----------"
            return 2000
