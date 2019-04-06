from scrapers import NocScraper

# Create instance of NocScraper for a given NOC
test = NocScraper('AFG')

# Get list of Games that NOC participated in
test.get_games_links(min_year=2010)
print(test.games_links)

# Get list of athletes in those Games
test.get_athlete_links(female=True)
print(test.athlete_links)

# Get data from results and infoboxes
test.get_athlete_data()
print(test.results)
print(test.info)

# Combine data from results and infoboxes into dataframe
test.join_data()
print(test.dataframe)

# Clean up columns



