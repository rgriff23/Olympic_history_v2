from requests import get
from bs4 import BeautifulSoup
from time import sleep
import warnings
import pandas as pd


class Scraper:
    """
    Parent class for scrapers.

    Gets data from an athlete page. Subclasses add functions for
    identifying which pages to visit. For example, NocScraper is
    a subclass of Scraper that adds functions for finding all
    athletes for a given NOC, subject to optional constraints such
    as gender, sport, or year of the Olympics.
    """

    def __init__(self):
        self.base_url = 'https://www.sports-reference.com/olympics/'
        self.athlete_links = []  # a list of athlete links
        self.failed_links = []  # pages that fail get saved here
        self.results = []  # results lists-of-lists get stored here
        self.info = [] # info box dictionaries get stored here
        self.dataframe = [] # final processed data

    def parse_infobox(self, html_soup):
        """
        Used internally by self.get_athlete_data

        :param html_soup:
        :return: Results are not returned, they are stored as a list of dictionaries in self.info
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
        # TODO: add code to clean the variable
        weight = list(filter(lambda x: 'Weight: ' in x, ptext))
        if weight:
            weight = weight[0]
            weight = weight[8:]
        else:
            weight = None

        # Parse date and place of birth
        birth = list(filter(lambda x: 'Born: ' in x, ptext))
        if birth:
            mob = birth[0].split(' ')[1]
            yob = birth[0].split(' ')[3]
            if mob not in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                           'October', 'November', 'December']:
                mob = None
            if len(yob) == 4 and yob.isdigit():
                yob = int(yob)
            else:
                yob = None
            birthplace = birth[0].split(' in ')
            if len(birthplace) == 2:
                birthplace = birthplace[1]
            else:
                birthplace = None
        else:
            mob = None
            yob = None
            birthplace = None

        # Parse date of death
        death = list(filter(lambda x: 'Died: ' in x, ptext))
        if death:
            mod = death[0].split(' ')[1]
            yod = death[0].split(' ')[3]
            if mod not in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                           'October', 'November', 'December']:
                mod = None
            if len(yod) == 4 and yod.isdigit():
                yod = int(yod)
            else:
                yod = None
        else:
            mod = None
            yod = None

        # Append infobox as dictionary to self.info
        self.info.append({'name': name,
                          'gender': gender,
                          'height': height,
                          'weight': weight,
                          'mob': mob,
                          'yob': yob,
                          'birthplace': birthplace,
                          'mod': mod,
                          'yod': yod})

    def join_data(self):
        """
        Merge results tables and infoboxes for each athlete. Run get_athlete_data first.

        :return: List of dataframes (one per athlete) with results and infobox data combined.
        """

        # Check that there are info and results to unpack
        if len(self.results) == 0 or len(self.info) == 0:
            warnings.warn('Info and/or results are missing! Run get_athlete_data.')
            return

        # Check that info and results are the same length
        if len(self.results) != len(self.info):
            warnings.warn('Oops... info and results are not the same length!')
            return

        # Reset dataframe if it is not empty
        if len(self.dataframe) != 0:
            warnings.warn('combined_data was not empty... resetting.')
            self.dataframe = []

        # Unpack individual results sets into dataframes (one per athlete)
        results_dfs = [pd.DataFrame.from_records(table) for table in self.results]

        # Unpack individual info boxes into a dataframe (one row per athlete)
        info_df = pd.DataFrame.from_records(self.info)

        # Check
        if info_df.shape[0] != len(results_dfs):
            warnings.warn('Join failed: number of info_df rows differs from length of results_dfs.')
            return

        print('Joining data from results tables and infoboxes...')

        # Merge results and infoboxes
        final_dfs = []
        for i in range(len(results_dfs)):

            # Rename results columns
            results_names = ['Games', 'Age', 'City', 'Sport', 'Event', 'Team', 'NOC', 'Rank', 'Medal']
            results_df = results_dfs[i]
            results_df.columns = results_names

            # Set primary keys
            results_df['primary_key'] = 1
            info_df['primary_key'] = pd.Series([1 if j == i else 0 for j in range(info_df.shape[0])])

            # Join results/info and add to final_dfs list
            joined = results_df.join(info_df.set_index('primary_key'), on='primary_key').drop('primary_key', axis=1)
            final_dfs.append(joined)

        self.dataframe = pd.concat(final_dfs)
        if not self.dataframe.empty:
            print('Join successful!')

    def get_athlete_data(self):
        """
        Fetch and parse Results table from each athlete page.
        The Results tables are stored in self.results

        Two issues will have to solved to combine results across many athletes:

        1. The length of the header may differ from the length of the rows containing data.
        2. The lengths of tables may vary across athletes depending on data availability.

        :return: List of lists, where each list is the Results table for an athlete.
        """

        # Checks
        if len(self.athlete_links) == 0:
            warnings.warn('Athlete links are missing! Run get_athlete_links.')

        print('Getting data from results tables and info boxes for each athlete...')

        # Look over each page in athlete_links
        for page in self.athlete_links:

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
                    self.failed_links.append(page)
                    self.results.append(None)
                    print(e)
                    print('Failed to get page: ' + page)
                    continue

            # Parse HTML
            html_soup = BeautifulSoup(text, 'html.parser')

            # Parse info box and store in self.info
            try:
                self.parse_infobox(html_soup)
            except Exception as e:
                self.failed_links.append(page)
                self.info.append(None)
                print(e)
                print('Failed to parse infobox: ' + page)
                continue

            # Parse table body and store in self.results
            table = html_soup.find("div", {"id": "div_results"})
            try:
                table_body = [tr.text for tr in table.find('tbody').find_all('tr')]
                table_body = [row.split('\n')[1:10] for row in table_body]
                self.results.append(table_body)
            except Exception as e:
                print(e)
                print('Failed to parse results table: ' + page)
                self.results.append(None)
                continue

        # Check for problems
        if len(self.athlete_links) != len(self.results):
            warnings.warn('Number of athlete links and number of results tables differ.')
        if len(self.athlete_links) != len(self.info):
            warnings.warn('Number of athlete links and number of info boxes differ.')

        print(f'Collected data for {len(self.athlete_links)} athletes.')

    # TODO: Function to combine results and info box into final data
    # TODO: Function to write final data


class NocScraper(Scraper):
    """
    Scrape athlete data for a given NOC.

    :param geo: 3 letter NOC
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
        :return: List of links to athletes in the NOC/Games
        """

        print('Getting individual athlete urls...')

        # Reset athlete_links if it is not empty
        if len(self.athlete_links) == 0:
            print('athlete_links was not empty... resetting.')
            self.athlete_links = []

        # Loop through games_pages and extract athlete_links
        for page in self.games_links:

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
