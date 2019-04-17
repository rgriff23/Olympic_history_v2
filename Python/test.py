from scrapers import NocScraper
import pandas as pd
pd.set_option('display.max_columns', 50)
pd.set_option('display.max_rows', 500)

# Create instance of NocScraper for a given NOC
test = NocScraper('GDR')

# Get list of Games that NOC participated in
test.get_games_links(min_year=1980, max_year=1988)
print(test.games_links)

# Get list of athletes in those Games
test.get_athlete_links(male=False)
print(test.athlete_links)

# Get data from results and infoboxes
test.get_athlete_data()

# Combine data from results and infoboxes into dataframe
test.join_data()
print(test.dataframe.head(n=500))

# Clean up columns



