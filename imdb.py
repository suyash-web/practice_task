from RPA.Browser.Selenium import Selenium
import csv
import pandas as pd

browser = Selenium()

class TopShows:

    def __init__(self, website: str, csv_file_name: str, excel_file_name: str) -> None:
        """Acceps three arguments as string,
           website, csv file name and excel file name."""

        self.website = website
        self.csv_file_name = csv_file_name
        self.excel_file_name = excel_file_name
    
    def open_page(self) -> None:
        """Accepts no arguments
           selects the top 250 tv shows from the menu"""

        browser.open_available_browser(self.website)
        browser.set_browser_implicit_wait(10)
        browser.wait_until_element_is_visible("xpath://div[text()='Menu']", 10)
        browser.get_selenium_implicit_wait()
        browser.click_element("xpath://div[text()='Menu']")
        browser.get_selenium_implicit_wait()
        browser.click_element("xpath://span[text()='Top 250 TV Shows']")
        browser.wait_until_element_is_visible("xpath://label[text()='Sort by: ']", 10)

    def set_to_release_date(self) -> None:
        """Accepts no arguments
           selects the value release date from the drop down"""

        browser.select_from_list_by_value("xpath://select[@id='lister-sort-by-options']", "us:descending")
    
    def get_show_details(self) -> list:
        """Accepts no arguments
           returns show rank and show title as list of strings"""

        title_elements = browser.get_webelements("xpath://td[@class='titleColumn']")
        titles = list()
        for title in title_elements:
            titles.append(browser.get_text(title))
        return titles
    
    def get_show_ratings(self) -> list:
        """Accepts no arguments
           returns show IMDB ratings as list of strings"""

        rate_elements = browser.get_webelements("xpath://td[@class='ratingColumn imdbRating']")
        ratings = list()
        for rate in rate_elements:
            ratings.append(browser.get_text(rate))
        return ratings
    
    def create_csv(self) -> None:
        """Accepts no arguments
           creates a csv file for show details like rank, title and IMDB rating"""

        rows = []
        fields = ['Rank', 'Title', 'IMDB Rating']
        titles = self.get_show_details()
        ratings = self.get_show_ratings()
        for i in range(len(titles)):
            rows.append(titles[i].split("."))
        for i in range(len(ratings)):
            rows[i].append(ratings[i])
        with open(self.csv_file_name, 'w') as csvfile: 
            csvwriter = csv.writer(csvfile)  
            csvwriter.writerow(fields)
            csvwriter.writerows(rows)
    
    def convert_to_excel(self) -> None:
        """Accepts no arguments
           converts the csv file into an excel file"""

        df = pd.read_csv(self.csv_file_name, encoding = "iso-8859-1", on_bad_lines = "warn")
        excel_file = pd.ExcelWriter(self.excel_file_name)
        df.to_excel(excel_file, index=False)
        excel_file.save()