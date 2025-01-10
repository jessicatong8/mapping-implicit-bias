import pandas as pd
import pyreadstat
import time
start_time = time.time()

file = "/Users/jessicatong/Documents/IAT/Race_IAT.public.2020.sav"

state_fips_dtype = {
    'stateName': 'str',
    'stateNo': 'str',
    'stateAbb': 'str',
}

state_fips = pd.read_csv('mapping-implicit-bias/data/us-state-fips.csv', dtype=state_fips_dtype)


def cleanChunk(chunk):
    # filter for country of residence, state, and overall IAT D score
    # PCT_error_3467 = % of error in combined-task blocks
    # pct_300 = % of latencies below 300 ms
    df = chunk.loc[:,["year","countryres_num", "STATE", "CountyNo", "D_biep.White_Good_all", "PCT_error_3467", "pct_300"]]
    # rename columns
    df.columns = ['year','country', 'stateAbb', 'countyNo','score','percentError','percentRT<300']
    # print(df.head(10))
    
    # filter for inclusion/exclusion critera
    # exclude missing data
    df = df.dropna()
    # include people in the US with state and county info
    df = df[(df["country"] == 1.0) &
            (df["stateAbb"] != "") &
            (df["countyNo"] != "") &
            # exclude errors on > 30% of trials
            (df["percentError"] <= 30) &
            # exclude reaction times <300 ms on >10% of trials
            (df["percentRT<300"] <= 10)].copy()

    # cast to correct data types
    df['year'] = df['year'].astype(int)
    df['countyNo'] = df['countyNo'].astype(str)
    df['countyNo'] = df['countyNo'].str.zfill(3)

    # add column with state name and number
    df['stateName'] = df['stateAbb'].map(state_fips.set_index('stateAbb')['stateName'])
    df['stateNo'] = df['stateAbb'].map(state_fips.set_index('stateAbb')['stateNo'])
    # add column with fips (stateNo + countyNo)
    df['fips'] = df['stateNo'] + df['countyNo']

    # drop uneccessary columns from dataframe
    df.drop(['country', 'countyNo', 'stateNo', 'percentError', 'percentRT<300'], axis=1, inplace=True)
    return df


def processChunks(file,group):
    result = [] 
    # Read spss .sav file in chunks
    reader = pyreadstat.read_file_in_chunks(pyreadstat.read_sav, file, chunksize= 10000)
    for df, meta in reader:
        cleaned_chunk = cleanChunk(df)
        # print(cleaned_chunk.head(10))  # print first 10 rows for testing)
        result.append(cleaned_chunk)
    combined_df = pd.concat(result)
    # group by given group, select score column, sums scores and counts number of people
    grouped = combined_df.groupby(group)['score'].agg(['sum', 'count']).reset_index()
    # calculate new column with  average score
    grouped['avgScore'] = (grouped['sum'] / grouped['count'])
    return grouped

def main():
    df = processChunks(file,'stateAbb')
    df.to_csv('2020_state_sav.csv', index=False)
    print(df.to_string())
    print("Process finished --- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    main()