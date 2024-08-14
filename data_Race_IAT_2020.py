import pandas as pd

import time
start_time = time.time()


#D_biep.White_Good_all: Overall IAT D Score
# countryres_num	Country of Residence
    # 1: USA
# STATE	2-letter State name for US residents
# CountyNo	County No. for US residents
# MSANo	Metropolitan Statistical Area No. for US residents
# MSAName	Metropolitan Statistical Area Name for US residents

file = 'Race.IAT.public.2020.csv'

# Read CSV file with specified dtypes
# Columns (4,5,6,7,8) have mixed types. Specify dtype option on import or set low_memory=False.

dtype_dict = {
    'month': 'str',
    'day': 'str',
    'year': 'str',
    'hour': 'str',
    'weekday': 'str'
}

def cleanChunk(chunk):
    #filter for country of residence, state, and overall IAT D score
    filtered = chunk.loc[:,["countryres_num", "STATE","D_biep.White_Good_all"]]
    filtered.columns = ['Country', 'State', 'Score']
    # filter for people in the US, and nonempty state and scores
    filtered=filtered.loc[(filtered["Country"]=="1") & (filtered["State"] != " ") & (filtered["Score"] != " ")]
    filtered["Score"] = pd.to_numeric(filtered['Score'], errors='coerce')
    return filtered
   
def groupBy(df):
    countStates = df.groupby('State').size()
    sumStates = df.groupby('State')['Score'].sum()
    groupedStates = pd.concat([sumStates, countStates], axis=1, ignore_index=True)
    groupedStates.columns = ['Sum', 'Count']
    return groupedStates

def sumChunks(file):
    first = True
    for chunk in pd.read_csv(file, chunksize=10000,dtype=dtype_dict):
        if first:
            oldChunk = groupBy(cleanChunk(chunk))
            first = False
        else:
            newChunk = groupBy(cleanChunk(chunk))
            oldChunk = oldChunk.add(newChunk, fill_value=0)
    return oldChunk

def main():
    df = sumChunks(file)
    df['Average'] = df['Sum'] / df['Count']
    print(df.to_string())
    print("Process finished --- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()


