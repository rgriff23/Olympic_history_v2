from scrapers import NocScraper

# test
test = NocScraper('AFG')
test.get_games_links(min_year=2010)
test.get_athlete_links()
test.get_athlete_data()

print(test.games_links)
print(test.athlete_links)
print(test.results)

# Tests
print(test.info)



