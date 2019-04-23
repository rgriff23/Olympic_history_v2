import pandas as pd

pd.set_option('display.max_columns', 50)
pd.set_option('display.max_rows', 500)


def validate_year(df):
    df.Year.isin(pd.read_csv('../Data/d_games.csv', usecols=['Year']))
        
test_dict = {
        'Year': validate_year,
        }


def Validate(df):
    
    # List of fields with validation functions
    valid_fields = test_dict.keys
    
    # Subset of fields without valid functions
    print('The following fields lack corresponding tests: \r', 
          df.columns[df.columns not in valid_fields])
    
    # Subset of fields without valid functions
    print('The following tests will NOT be performed (missing fields): \r', 
          valid_fields[valid_fields not in df.columns])
    
    # Subset of fields with valid functions
    print('The following validation tests will be performed: \r', 
          df.columns[df.columns in valid_fields])
    
    print('Performing tests...')
    
    for test in valid_fields:
        try:
            df = test_dict[test](df)
        except Exception as e:
            print(e)
            print('Test failed for field:', test)


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
