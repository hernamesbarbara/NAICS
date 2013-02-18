import numpy as np
import pandas as pd
import string
import pprint as pp

pd.set_printoptions(max_columns=10, max_rows=50)
dirname = './data/cleaned/'
n_to_s_02_87 = pd.read_csv(dirname + '2002_NAICS_to_1987_SIC.xls.txt', sep="|")
# n_to_n_97_02 = pd.read_csv(dirname + '2002_NAICS_to_1997_NAICS.xls.txt', sep="|")
# n_to_n_02_07 = pd.read_csv(dirname + '2007_to_2002_NAICS.xls.txt', sep="|")
# n_to_n_07_12 = pd.read_csv(dirname + '2012_to_2007_NAICS.xls.txt', sep="|")

n_to_s_02_87 = n_to_s_02_87.drop("Unnamed: 0", axis=1)
# n_to_n_97_02 = n_to_n_97_02.drop("Unnamed: 0", axis=1)
# n_to_n_02_07 = n_to_n_02_07.drop("Unnamed: 0", axis=1)
# n_to_n_07_12 = n_to_n_07_12.drop("Unnamed: 0", axis=1)

n_to_s_02_87.columns = ['end_naics', 'end_naics_title', 'start_sic', 'start_sic_title', 'filename', 'start', 'end']
n_to_s_02_87.start_sic[n_to_s_02_87.start_sic.isnull()] = ""

def toFloat(x):
    try:
        return int(float(x))
    except:
        return np.nan

n_to_s_02_87.start_sic = n_to_s_02_87.start_sic.apply(toFloat)
n_to_s_02_87.end_naics = n_to_s_02_87.end_naics.apply(toFloat)

naics = n_to_s_02_87.end_naics
years = n_to_s_02_87.end

y2k2 = pd.DataFrame(zip(naics,['naics'] * len(naics), years), columns=['code', 'standard', 'year'])


sics = n_to_s_02_87.start_sic
y2k2 = y2k2.append(pd.DataFrame(zip(sics,['sic'] * len(sics), years), columns=['code', 'standard', 'year']))



from pandas.core.reshape import melt

melted = melt(n_to_s_02_87, id_vars=['end'], value_vars=['end_naics'])