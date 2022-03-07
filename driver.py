from imdb import TopShows

shows = TopShows("https://www.imdb.com/", "show_details.csv", "show_details.xlsx")
shows.open_page()
shows.set_to_release_date()
shows.create_csv()
shows.convert_to_excel()