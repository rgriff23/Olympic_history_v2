# Olympic history (version 2)

This code scrapes and parses data on Olympic athletes from www.sports-reference.com/olympics. 

The scraper requires a 3-letter NOC (National Olympic Committee) code as a parameter. 
A list of valid NOCs and their corresponding country/region can be found in `Data/d_noc.csv`.

The scraper takes a number of other parameters to narrow the scope of the scrape: 
minimum or maximum Olympic year, season, sex, and sport. Valid sports can be found 
in `Data/d_sports.csv` and valid Games can be found in `Data/d_games.csv`.

The geographic coordinates of host cities can be found in `Data/d_hostcity.csv`, and is useful
for plotting the locations of Games.