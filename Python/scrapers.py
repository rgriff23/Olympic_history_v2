from requests import get
from bs4 import BeautifulSoup
from time import (sleep, time)
from tqdm import tqdm
import warnings
import pandas as pd


class Scraper:
    """
    Parent class for scrapers.

    Gets data from an athlete page. Subclasses add functions for
    identifying which pages to visit. For example, NocScraper is
    a subclass of Scraper that adds functions for finding all
    athletes for a given NOC, subject to optional constraints such
    as gender, sport, or Olympic year.
    """

    def __init__(self):
        self.base_url = 'https://www.sports-reference.com/oFlympics/'
        self.athlete_links = []  # a list of athlete links
        self.results = []  # results lists-of-lists get stored here
        self.info = [] # info box dictionaries get stored here
        self.events = [] # events history dicts of lists
        self.results_df = [] # infobox + results dataframe
        self.events_dfs = [] # events history dict of dataframes
 
    def parse_infobox(self, html_soup, p):
        """
        Used internally by self.get_athlete_data

        :param html_soup:
        :return: Results are stored as a list of dictionaries in self.info
        """

        # Get the infobox
        ptext = html_soup.find("div", {"id": "info_box"}).find('p').getText().split('\n')

        # Parse name
        name = html_soup.find('h1')
        if name:
            name = name.text
        else:
            name = None

        # Parse gender
        gender = list(filter(lambda x: 'Gender: ' in x, ptext))
        if gender:
            gender = gender[0][8:]
        else:
            gender = None

        # Parse height
        height = list(filter(lambda x: 'Height: ' in x, ptext))
        if height:
            height = height[0]
            height = int(height[height.find('(') + 1:height.find(' cm)')])
        else:
            height = None

        # Parse weight
        weight = list(filter(lambda x: 'Weight: ' in x, ptext))
        if weight:
            weight = weight[0]
            weight = weight[8:]
        else:
            weight = None

        # Parse date and place of birth
        birth = list(filter(lambda x: 'Born: ' in x, ptext))
        if birth:
            birth = birth[0].split('Born: ')[1]
        else:
            birth = None

        # Parse date and place of death
        death = list(filter(lambda x: 'Died: ' in x, ptext))
        if death:
            death = death[0].split('Died: ')[1]
        else:
            death = None

        # Parse affiliations
        affiliations = list(filter(lambda x: 'Affiliations: ' in x, ptext))
        if affiliations:
            affiliations = affiliations[0].split('Affiliations: ')[1]
        else:
            affiliations = None

        # Parse related Olympians
        relatives = list(filter(lambda x: 'Related Olympians: ' in x, ptext))
        if relatives:
            relatives = relatives[0].split('Related Olympians: ')[1]
        else:
            relatives = None

        # Append infobox as dictionary to self.info
        self.info.append({'name': name,
                          'gender': gender,
                          'height': height,
                          'weight': weight,
                          'birth': birth,
                          'death': death,
                          'affiliations': affiliations,
                          'relatives': relatives,
                          'link': self.athlete_links[p]})

    def get_athlete_data(self):
        """
        Fetch and parse Results table and Infobox from each athlete page.

        :return: Results tables are stored in self.results and Infoboxes in self.info
        """

        # Checks
        if len(self.athlete_links) == 0:
            warnings.warn('Athlete links are missing! Run get_athlete_links.')

        print('Getting data for each athlete...')
        start = time()

        # Loop over each page in athlete_links
        for p, page in enumerate(tqdm(self.athlete_links)):

            # Get and parse html text using Python's built-in HTML parser
            try:
                text = get(page).text
            # Pause for a minute if there was a problem and try again
            except Exception as e:
                print(e)
                print('Sleeping for 60 seconds before trying again.')
                sleep(60)
                print('Trying again...')
                try:
                    text = get(page).text
                except Exception as e:
                    self.results.append(None)
                    self.info.append(None)
                    print('Failed to get page: ' + page)
                    print(e)
                    continue

            # Parse HTML
            html_soup = BeautifulSoup(text, 'html.parser')

            # Parse info box and store in self.info
            try:
                self.parse_infobox(html_soup, p)
            except Exception as e:
                print('Exception parsing infobox: ' + page)
                print(e)
                continue

            # Parse results table and store in self.results
            table = html_soup.find("div", {"id": "div_results"})
            try:
                table_body = [tr.text for tr in table.find('tbody').find_all('tr')]
                table_body = [row.split('\n')[1:10] for row in table_body]
                self.results.append(table_body)
            except Exception as e:
                print('Exception parsing results table: ' + page)
                print(e)
                continue

        # Checks
        assert len(self.athlete_links) == len(self.results)
        assert len(self.athlete_links) == len(self.info)

        print(f'Collected data for {len(self.athlete_links)} athletes.')
        print('Time elapsed:', round((time() - start)/60, 2), 'minutes.')

    def join_data(self):
        """
        Merge results tables and infoboxes for each athlete. Run get_athlete_data first.

        :return: Dataframe with results and infobox data combined. Each row is an athlete-result.
        """

        # Checks
        assert (len(self.athlete_links) == len(self.results)) & (len(self.athlete_links) == len(self.info))
        if len(self.results) == 0 or len(self.info) == 0:
            warnings.warn('Info and/or results are missing! Run get_athlete_data.')
            return

        # Reset results_df if it is not empty
        if len(self.results_df) != 0:
            warnings.warn('results_df was not empty... resetting.')
            self.results_df = []

        # Unpack individual results sets into dataframes (one per athlete)
        results_dfs = [pd.DataFrame.from_records(table) for table in self.results]

        # Unpack individual info boxes into a dataframe (one row per athlete)
        info_df = pd.DataFrame.from_records(self.info)

        # Check
        if info_df.shape[0] != len(results_dfs):
            warnings.warn('Join failed: number of info_df rows differs from length of results_dfs.')
            return

        print('Joining data from results tables and infoboxes...')
        start = time()

        # Merge results and infoboxes
        final_dfs = []
        for i, results_df in enumerate(results_dfs):

            # Rename results columns
            results_names = ['Games', 'Age', 'City', 'Sport', 'Event', 'Team', 'NOC', 'Rank', 'Medal']
            results_df.columns = results_names

            # Set primary keys
            results_df['primary_key'] = 1
            info_df['primary_key'] = pd.Series([1 if j == i else 0 for j in range(info_df.shape[0])])

            # Join results/info and add to final_dfs list
            joined = results_df.join(info_df.set_index('primary_key'), on='primary_key').drop('primary_key', axis=1)
            final_dfs.append(joined)

        self.results_df = pd.concat(final_dfs)
        if not self.results_df.empty:
            print('Join successful!')
            print('Time elapsed:', round((time() - start)/60, 2), 'minutes.')


class NocScraper(Scraper):
    """
    Scrape athlete data for a given NOC.

    :param noc: 3 letter NOC
    """

    def __init__(self, noc):
        Scraper.__init__(self)
        self.noc = noc
        self.base_url = 'https://www.sports-reference.com/olympics/'
        self.athlete_url = self.base_url + 'athletes/'
        self.country_url = self.base_url + 'countries/'
        self.entry_url = self.country_url + noc + '/'
        self.games_links = []

    def get_games_links(self, min_year=1890, max_year=2050, summer=True, winter=True):
        """
        Get links to NOC/Games pages.

        This sets the attribute self.games_links.
        The attribute can also be set manually as a list of links.

        :param min_year: Minimum year to include (defaults to 1890)
        :param max_year: Maximum year to include (defaults to 2050)
        :param summer: Whether to include Summer Games (defaults to True)
        :param winter: Whether to include Winter Games (defaults to True)
        :return: List of links to Games the NOC has participated in
        """

        print('Getting Olympic Games urls for the NOC...')

        # Reset athlete_links if it is not empty
        if len(self.games_links) != 0:
            print('games_links was not empty... resetting.')
            self.games_links = []

        # Get and parse html text using Python's built-in HTML parser
        text = get(self.entry_url).text
        html_soup = BeautifulSoup(text, 'html.parser')

        # Extract the table body
        table_body = html_soup.find('table').find('tbody')

        # Extract NOC/Games links and store in self.games_links
        for row in table_body.find_all('tr'):
            html = str(row.find_all('td')[1]).split('/')

            # Filters for date and season
            if int(html[5]) < min_year or int(html[5]) > max_year:
                continue
            if summer == False and html[4] == 'summer':
                continue
            if winter == False and html[4] == 'winter':
                continue

            # If filters were passed, store Games page link in self.games_links
            link = self.entry_url + html[4] + '/' + html[5]
            self.games_links.append(link)

        # Print output when complete
        text = 'Collected urls for ' + \
               str(len(self.games_links)) + \
               ' Games for NOC = ' + \
               self.noc
        print(text)

    def get_athlete_links(self, male=True, female=True, one_sport=None):
        """
        Get links to individual athlete pages

        This sets the attribute self.athlete_links.
        The attribute can also be set manually as a list of links.

        :param male: Whether to include males (defaults to True)
        :param female: Whether to include females (defaults to True)
        :param one_sport: Include athletes from the specified sport only (defaults to None)
        :return: List of links to athletes in the NOC/Games
        """

        print('Getting individual athlete urls...')

        # Reset athlete_links if it is not empty
        if len(self.athlete_links) != 0:
            print('athlete_links was not empty... resetting.')
            self.athlete_links = []

        # Loop through games_pages and extract athlete_links
        for page in tqdm(self.games_links):

            # Get and parse html text using Python's built-in HTML parser
            text = get(page).text
            html_soup = BeautifulSoup(text, 'html.parser')

            # Extract the table body
            table_body = html_soup.find('table').find('tbody')

            # Extract athlete page links and store in self.athlete_links
            for row in table_body.find_all('tr'):
                cells = row.find_all('td')
                html = str(cells[1].find('a', href=True)['href']).split('/')
                sex = str(cells[2].contents[0])
                sport = cells[4].find('a', href=True).text

                # Filters for sex and sport
                if male == False and sex == 'Male':
                    continue
                if female == False and sex == 'Female':
                    continue
                if one_sport and sport != one_sport:
                    continue

                # If filters were passed, store athlete page links in self.athlete_links
                link = self.athlete_url + html[3] + '/' + html[4]
                self.athlete_links.append(link)

        # Remove duplicate pages
        self.athlete_links = list(set(self.athlete_links))

        # Print output when complete
        text = 'Collected urls for ' + \
               str(len(self.athlete_links)) + \
               ' athletes for NOC = ' + \
               self.noc
        print(text)