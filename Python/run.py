from scrapers import NocScraper
from parsers import Parser
import pandas as pd

pd.set_option('display.max_columns', 50)
pd.set_option('display.max_rows', 500)

##########
# SCRAPE #
##########

# Create instance of NocScraper
scraper = NocScraper('KOR')

# Get list of Games that NOC participated in
scraper.get_games_links(min_year=1970, max_year=1972)

# Get list of athletes in those Games 
# set male=False or female=False to turn off either sex
# set one_sport='Valid Sport' to collect data from a specific sport
# A valid list of sports can be found at Data/d_sport
scraper.get_athlete_links(male=False)

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
results_parsed = parser.parsed_results
results_parsed.columns
results_parsed.head(5)

# Event history parsing
parser.parse_events_dfs()
events_parsed = parser.parsed_events
events_parsed.columns
events_parsed.head(5)

############
# VALIDATE #
############

df = results_parsed

print(df.shape)
print(df.isna().sum())

# name 
print(df.Name.unique())

# Age 
print(df.Age.astype(int).hist(bins=20))

# City 
print(df.City.value_counts(ascending=True).plot.barh())

# Sport 
print(df.Sport.value_counts(ascending=True).plot.barh())

# Event 
print(df.Event.value_counts())

# NOC 
print(df.NOC.value_counts(ascending=True).plot.barh())

# Medal 
print(df.Medal.value_counts(ascending=True).plot.barh())

# gender 
print(df.Sex.value_counts(ascending=True).plot.barh())

# height 
print(df.Height.hist())

# weight 
print(df.Weight.hist())

# birthdate 
print(pd.to_datetime(df.BirthDate).dt.to_period('Y').astype(str).astype(int).hist())
print(df.BirthCity.plot.barh())
print(df.BirthCountry.plot.barh())

# death 
print(pd.to_datetime(df.DeathDate).dt.to_period('Y').astype(str).astype(int).hist())
print(df.DeathCity.plot.barh())
print(df.DeathCountry.plot.barh())

# link 
print(df.link[:5])

# affiliations 
print(df.affiliations.value_counts())

# relatives 
print(df.relatives.unique())

#######
# END #
#######

