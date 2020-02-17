from scrapers import NocScraper
from parsers import Parser
import pandas as pd

"""
This script loops over a list of NOCs and writes parsed results to files
with the name of the noc in the specified directory
"""

nocs = pd.read_csv('H:/Olympic history data/Dimension tables/d_noc.csv')['NOC'].tolist()
write_path = 'H:/Olympic history data/final/'

for noc in nocs:
    
    try:

        ##########
        # SCRAPE #
        ##########
        
        # Create instance of NocScraper
        scraper = NocScraper(noc)
        
        # Get list of Games that NOC participated in
        scraper.get_games_links()
        
        # Get list of athletes in those Games 
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
        
        print('Writing results...')
        
        # Write parsed results to csv in NOC folder
        results_parsed.to_csv(f"{write_path}{noc}.csv", 
                              columns=['ID', 'Name', 'Sex', 'Age', 
                                       'Height', 'Weight', 'Team', 'NOC', 
                                       'Year', 'Season', 'City', 'Sport', 
                                       'Event', 'Medal', 'Rank',                                     
                                      'BirthDate', 'BirthCity', 'BirthCountry',
                                      'DeathDate', 'DeathCity', 'DeathCountry',
                                      'affiliations','relatives','link'],
                              index=False)
        
        # Write links_missing_data to a text file in Missing_data folder
        if len(scraper.links_missing_data) > 0:
            with open(f"H:/Olympic history data/Missing data/{noc}_missing.txt", 'w') as f:
                for link in scraper.links_missing_data:
                    f.write("%s\n" % link)
                    
        print('Finished!')
        
    except: 
        print(f'Failed on NOC {noc}')

