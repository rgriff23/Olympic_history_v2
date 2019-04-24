from scrapers import NocScraper
from parsers import Parser

# NOCs Lars asked for
nocs = ['GER','GDR','FRG','SAA','AUT','DEN','NOR','ISL','IRL','SWE','SUI']

for noc in nocs:

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
    
    # Write to csv
    results_parsed.to_csv(f"H:/Olympic history data/NOC/{noc}.csv", 
                          columns=['Year', 'Season', 'City', 'Sport', 'Event', 
                                  'NOC', 'Name', 'Sex', 'Age',  
                                  'Height', 'Weight', 'Medal', 
                                  'BirthDate', 'BirthCity', 'BirthCountry',
                                  'DeathDate', 'DeathCity', 'DeathCountry',
                                  'affiliations','relatives','link'],
                          index=False)


