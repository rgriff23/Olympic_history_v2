import pandas as pd
import numpy as np
import re
import dateparser as dp
from geotext import GeoText as gp

# Helper functions
def parse_games(df):
    temp = df.Games.str.split(' ', n = 1, expand = True)
    df['Year'] = temp[0]
    df['Season'] = temp[1]
    # The 'Equestrian' value corresponds to the 1956 Stockholm Games, which 
    # occurred separately from the rest of the Summer Games in Melbourne
    df['Season'] = df.Season.replace('Equestrian',  'Summer')
    df.drop('Games', axis=1, inplace=True)
    return df

def parse_age(df):
    df['Age'] = [None if i == '' else int(i) for i in df['Age']]
    return df

def parse_city(df):
    df.City.replace('MÃ¼nchen', 'Munich', inplace=True)
    df.City.replace('MontrÃ©al', 'Montreal', inplace=True)
    df.City.replace('Ciudad de MÃ©xico', 'Mexico City', inplace=True)
    return df

def parse_sport(df):
    return df

def parse_event(df):
    df['Event'] = df.Event.str.replace('Ã', 'x')
    df['Event'] = df.Event.str.replace('Ã\x97', 'x')
    df['Event'] = df.Event.str.replace('Ã\x89pÃ©e', 'epee') 
    return df

def parse_team(df):
    return df.drop(['Team'], axis=1)

def parse_noc(df):
    return df

def parse_rank(df):
    return df.drop(['Rank'], axis=1)

def parse_medal(df):
    df['Medal'].replace('', np.nan, inplace=True)
    return df

def parse_affiliations(df):
    return df

def parse_link(df):
    return df

def parse_relatives(df):
    return df

def parse_name(df):
    df.rename(columns={'name':'Name'}, inplace=True)
    return df

def parse_gender(df):
    df['Sex'] = df.gender
    df.drop(['gender'], axis=1, inplace=True)
    return df

def parse_birth(df):
    
    split = [s.split(' in ') if s else None for s in df.birth]
    # If no month / day is given, then April 21
    df['BirthDate'] = [dp.parse(s[0]) if s else None for s in split]
    df['BirthDate'] = [s.date() if s else None for s in df['BirthDate']]
    df['BirthCity'] = [None if s is None else gp(s[1]).cities if len(s) == 2 else None for s in split]
    df['BirthCity'] = [c[0] if c else None for c in df.BirthCity]
    df['BirthCountry'] = [None if s is None else gp(s[1]).countries if len(s) == 2 else None for s in split]
    df['BirthCountry'] = [c[0] if c else None for c in df.BirthCountry]
    df.drop(['birth'], axis=1, inplace=True)
    return df

def parse_death(df):
    split = [s.split(' in ') if s else None for s in df.death]
    # If no month / day is given, then April 21
    df['DeathDate'] = [dp.parse(s[0]) if s else None for s in split]
    df['DeathDate'] = [s.date() if s else None for s in df['DeathDate']]
    df['DeathCity'] = [None if s is None else gp(s[1]).cities if len(s) == 2 else None for s in split]
    df['DeathCity'] = [c[0] if c else None for c in df.DeathCity]
    df['DeathCountry'] = [None if s is None else gp(s[1]).countries if len(s) == 2 else None for s in split]
    df['DeathCountry'] = [c[0] if c else None for c in df.DeathCountry]
    df.drop(['death'], axis=1, inplace=True)
    return df

def parse_height(df):
    df['Height'] = df.height
    df.drop(['height'], axis=1, inplace=True)
    return df

def parse_weight(df): 
    weights = []
    for w, text in enumerate(df.weight):
        if text:
            if 'lbs' in text:
                weights.append(float(text.split(' lbs (')[1].split(' ')[0]))
            else:
                weights.append(pd.Series(re.findall('\d+', text)).astype(int).mean())
        else:
            weights.append(np.nan)
    df['Weight'] = weights
    df.drop(['weight'], axis=1, inplace=True)
    return df

parse_results_dict = {
        'name': parse_name,
        'gender': parse_gender,
        'Games': parse_games,
        'Age': parse_age,
        'City': parse_city,
        'Sport': parse_sport,
        'Event': parse_event,
        'Team': parse_team,
        'NOC': parse_noc,
        'Rank': parse_rank,
        'Medal': parse_medal,
        'height': parse_height,
        'weight': parse_weight,
        'birth': parse_birth,
        'death': parse_death,
        'affiliations': parse_affiliations,
        'relatives': parse_relatives,
        'link': parse_link
        }

    
class Parser:
    """
    Parent class for parsers. 
    
    Parses results_df and events_dfs. Subclasses can add parsing steps.
    
    :param scraper: Scraper with results_df populated. 
    """
    
    def __init__(self, scraper):
        self.scraper = scraper
        self.results_df = scraper.results_df
        assert (len(self.scraper.results_df) + len(self.scraper.events_dfs)) > 0
        self.parsed_results = []
        self.parse_results_dict = parse_results_dict
    
    def parse_results_df(self):
        
        df = self.results_df
        parse_dict = self.parse_results_dict
        
        # List of fields with validation functions
        valid_fields = list(parse_dict.keys())

        # Subset of fields without valid functions
        print('The following fields lack a parser: ')
        for i in df.columns[~df.columns.isin(valid_fields)].values:
            print(' - ', i)
        
        # Subset of fields without valid functions
        print('The following parsers will NOT be used (missing fields): ') 
        for i in [i for (i, v) in zip(valid_fields, [f in df.columns.values for f in valid_fields]) if not v]:
            print(' - ', i)
        
        # Subset of fields with valid functions
        valid_fields = [i for (i, v) in zip(valid_fields, [f in df.columns.values for f in valid_fields]) if v]
    
        # Run fields through the parsing functions
        print(f'Parsing {len(valid_fields)} fields...')
        for field in valid_fields:
            try:
                df = parse_dict[field](df)
                print(' - Parsed field:', field)
            except Exception as e:
                print('Parsing failed for field:', field)
                print(e)
        
        df.reset_index(drop=True, inplace=True)
        self.parsed_results = df
        
        print('Parsed', self.results_df.shape[1], 'fields.')

    