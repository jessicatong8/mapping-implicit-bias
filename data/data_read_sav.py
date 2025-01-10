import pandas as pd
import pyreadstat
import numpy as np
import time
start_time = time.time()

state_fips_dtype = {
    'stateName': 'str',
    'stateNo': 'str',
    'stateAbb': 'str',
}

state_fips = pd.read_csv('mapping-implicit-bias/data/us-state-fips.csv', dtype=state_fips_dtype)


def cleanChunk(chunk, group):
    # filter for country of residence, state, and overall IAT D score
    # PCT_error_3467 = % of error in combined-task blocks
    # pct_300 = % of latencies below 300 ms
    df = chunk[["year", "countryres_num", "STATE", "CountyNo", "D_biep.White_Good_all", "PCT_error_3467", "pct_300"]]
    # rename columns
    df.columns = ['year','country', 'stateAbb', 'countyNo','score','percentError','percentRT<300']
    # print(df.head(10))
    
    # filter for inclusion/exclusion critera
    #include people in the US with state and county info
    df = df[(df["country"] == 1.0) &
            (df["stateAbb"] != "") &
            (df["countyNo"] != "") &
            (df["score"].notna()) &
            # exclude errors on > 30% of trials
            (df["percentError"] <= 30) &
            # exclude reaction times <300 ms on >10% of trials
            (df["percentRT<300"] <= 10)]
    
    if group == 'county':
        # add column with state name and number
        df['stateNo'] = df['stateAbb'].map(state_fips.set_index('stateAbb')['stateNo'])
        # add column with fips (stateNo + countyNo)
        df['fips'] = df['stateNo'] + df['countyNo'].astype(str).str.zfill(3)
        df.drop(['stateNo'], axis=1, inplace=True)

    # round score to 2 decimal places
    df['score'] = df['score'].round(2)

    # drop uneccessary columns from dataframe
    df.drop(['country', 'countyNo', 'percentError', 'percentRT<300'], axis=1, inplace=True)
    
    # print(df.head(5))
    return df


def processChunks(file,group,year):
    # check if group is either state or county
    if group != "state" and group != "county":
        raise ValueError("Invalid group. Please choose either state or county.")
        
    result = [] 
    
    # Read spss .sav file in chunks
    reader = pyreadstat.read_file_in_chunks(pyreadstat.read_sav, file, chunksize= 10000)
    
    for df, meta in reader:
        cleaned_chunk = cleanChunk(df, group)
        # print(cleaned_chunk.head(10))  # print first 10 rows for testing)
        result.append(cleaned_chunk)  
    combined_df = pd.concat(result)

    # group by given group, select score column, sums scores and counts number of people
    if group == "state":
        key = "stateAbb"
    elif group == "county":
        key = "fips"
    
    grouped = combined_df.groupby(key)['score'].agg(['sum', 'count']).reset_index()
    # calculate new column with  average score
    grouped['avgScore'] = (grouped['sum'] / grouped['count']).round(2)
    grouped.drop(['sum'], axis=1, inplace=True)
    
    if group == "state":
        grouped['stateName'] = grouped['stateAbb'].map(state_fips.set_index('stateAbb')['stateName'])
    
    # add columns with year
    grouped['year'] = year

    return grouped

def main():
    file = "/Users/jessicatong/Documents/IAT/Race_IAT.public.2016.sav"
    year = 2016
    group = 'state'
    df = processChunks(file, group, year)
    df.to_csv('mapping-implicit-bias/data/' + str(year) + '_' + group + '.csv', index=False)
    print(df.to_string())
    print("Process finished --- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    main()