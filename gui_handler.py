import Tkinter as tk 
from crawler import Crawler
from tkFileDialog import askopenfilename
from multiprocessing import Process
from dd_file_reader import DDFileReader


class GuiHandler(object):
    """ Gui Handler Documentation """
    
    def __init__(self):
        self.craigslist_placeholder = "Enter Ad Link"
        self.crawler = Crawler()
        self.root = tk.Tk()
        self.row, self.column = 0, 0
        self.widgets = self.create_widgets()
        self.pack_widgets()
        self.grid_widgets()
        self.root.mainloop()
        self.gui_processes = []
        self.current_process = None

    def reset_row_column(self):
        self.row, self.column = 0, 0

    def openfile(self):

        filename = askopenfilename(parent=self.root)
        return DDFileReader.read_file_lines_stripped(str(filename))

    # Every time a key is pressed into the url entry, do nothing
    def url_entry_keypress(self, event):
        print event.keycode

    def url_entry_onclick(self, event):
        print "Showing ad link entry input"
        input_text = self.url_entry.get().strip()
        print input_text
        if input_text == self.craigslist_placeholder:
            self.delete_input(self.url_entry, input_text)

    def delete_input(self, tk_entry_element, text):
        while text != None and len(text) > 0:
            for i in range(len(text)):
                tk_entry_element.delete(i)
            text = tk_entry_element.get()

    def create_widgets(self):
        self.url_entry = tk.Entry()
        self.insert_placeholder(self.url_entry, self.craigslist_placeholder)
        self.url_entry.bind("<Key>", self.url_entry_keypress)
        self.url_entry.bind("<Button-1>", self.url_entry_onclick)
        self.go_button = tk.Button(text="Open Ads", command=self.handle_crawl, bg="black", fg="green")
        self.get_nasty_btn = tk.Button(text="Open Ads From File", command=self.handle_crawl_from_file, bg="black", fg="blue")
        return [self.url_entry, self.go_button, self.get_nasty_btn]

    def insert_placeholder(self, entry_element, placeholder_value):
        entry_element.insert(0, placeholder_value)

    def handle_crawl(self):
        current_ad_link = self.url_entry.get()
        if self.valid_ad_link(current_ad_link):
            try:
                self.crawler.start_crawl_v1(current_ad_link)
            except Exception as e:
                print str(e)

    def handle_crawl_from_file(self):
        links = self.openfile()
        for link in links:
            print link
            print "\n"
            print "\n"
            self.crawler.start_crawl_v1(link)

    def valid_ad_link(self, current_ad_link):
        print "[+] Checking link %s" % current_ad_link

        if current_ad_link == '' or current_ad_link == self.craigslist_placeholder:
            for i in range(3): print "[+] You must enter a url "
            return False
        return True

    def pack_widgets(self):
        for widget in self.widgets:
            widget.pack()

    def grid_widgets(self):
        for widget in self.widgets:
            widget.grid(row=self.row, column=self.column)
            self.column += 1

if __name__ == "__main__":
    gui = GuiHandler()



