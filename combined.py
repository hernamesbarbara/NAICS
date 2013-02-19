import numpy as np
import pandas as pd
import string
import pprint as pp

pd.set_printoptions(max_columns=10, max_rows=50)

f = './data/cleaned/industry_codes_1987_to_2012.csv'

df = pd.read_csv(f, sep='|')