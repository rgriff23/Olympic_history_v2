import pandas as pd

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

