import pandas as pd
import glob

# Paths
import_path = 'H:/Olympic history data/NOC/'
export_path = 'H:/Olympic history data/Athlete longevity study/'

# Import NOCs
df = pd.concat(map(pd.read_csv, glob.glob(import_path + '*.csv')))

# Dedupe
df = df.drop_duplicates()

# Export
df.to_csv(export_path + 'full_deduplicated_dataset.csv')