from scrapers import NocScraper
from parsers import Parser

noc = 'GER'

##########
# SCRAPE #
##########

# Create instance of NocScraper
scraper = NocScraper(noc)

# Get list of Games that NOC participated in
scraper.get_games_links()

# Get list of athletes in those Games 
# set male=False or female=False to turn off either sex
# set one_sport='Valid Sport' to collect data from a specific sport
# A valid list of sports can be found at Data/d_sport
scraper.get_athlete_links()

# Get data
scraper.get_athlete_data()

# Combine data
scraper.join_data()

#########
# PARSE #
#########

parser = Parser(scraper)

# Results parsing
parser.parse_results_df()

# Check results
results_parsed = parser.parsed_results
results_parsed.columns
results_parsed.head(5)

#########
# WRITE #
#########

# Write to csv
results_parsed.to_csv(f"H:/Olympic history data/NOC/{noc}.csv")

#######
# END #
#######

