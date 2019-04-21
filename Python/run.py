from scrapers import NocScraper
from parsers import Parser
from validation import Validate
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 50)
pd.set_option('display.max_rows', 500)

##########
# SCRAPE #
##########

# Create instance of NocScraper
scraper = NocScraper('KOR')

# Get list of Games that NOC participated in
scraper.get_games_links(min_year=1986, max_year=1988)

# Get list of athletes in those Games
scraper.get_athlete_links(male=False)

# Get data from results and infoboxes
scraper.get_athlete_data()

# Combine data from results and infoboxes into dataframe
scraper.join_data()

###########
# INSPECT #
###########

df = scraper.results_df

print(df.shape)
print(df.isna().sum())

# Games (add Year and Season, drop Games)
print(len(df.Games.unique()))
print(df.Games.unique())
print(df.Games.value_counts(ascending=True).plot.barh())

# Age (convert to integer)
print(df.Age.astype(int).hist(bins=20))

# City (weird characters)
print(df.City.value_counts(ascending=True).plot.barh())

# Sport (ok)
print(df.Sport.value_counts(ascending=True).plot.barh())

# Event (many)
print(df.Event.value_counts())

# Team (drop)
print(df.Team.value_counts(ascending=True).plot.barh())

# NOC (some athletes have competed for multiple countries)
print(df.NOC.value_counts(ascending=True).plot.barh())

# Rank (drop)
print(df.Rank.value_counts())

# Medal (replace empty cells with None)
print(df.Medal.value_counts(ascending=True).plot.barh())

# affiliations (many)
print(df.affiliations.value_counts())

# birth (add month, day, year, cities, countries)
print(df.birth.value_counts())

# death (add month, day, year, cities, countries)
print(df.death.value_counts())

# gender (rename Sex)
print(df.gender.value_counts(ascending=True).plot.barh())

# height (convert to cm, rename Height_cm)
print(df.height.value_counts(ascending=True).plot.barh())

# link (ok)
print(df.link.value_counts(ascending=True).plot.barh())

# name (weird characters)
print(df.name.unique())

# relatives (few)
print(df.relatives.unique())

# weight (convert to kg, rename Weight_kg)
print(df.weight.value_counts(ascending=True).plot.barh())

#########
# PARSE #
#########

parser = Parser(scraper)
parser.parse_results_df()
parser.parsed_results.columns
parser.parsed_results.head(5)

#########
# CHECK #
#########



#######
# END #
#######

