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

state_fips_dtype = {
    'stateName': 'str',
    'stateNo': 'str',
    'stateAbb': 'str',
}

state_fips = pd.read_csv('us-state-fips.csv',dtype=state_fips_dtype)
#print(state_fips.columns)
#print(state_fips.head(5))  # print first 5 rows for testing

def cleanChunk(chunk):
    #filter for country of residence, state, and overall IAT D score
    df = chunk.loc[:,["countryres_num", "STATE", "CountyNo", "MSANo", "MSAName", "D_biep.White_Good_all"]]
    df.columns = ['country', 'stateAbb', 'countyNo', 'metroNo', 'metroName', 'score']
    # filter for people in the US, and nonempty state and scores
    df = df[(df["country"] == "1") &
            (df["stateAbb"] != " ") &
            (df["countyNo"] != " ") &
            (df["metroNo"] != " ") & 
            (df["metroName"] != " ") & 
            (df["score"] != " ")]
    df["score"] = pd.to_numeric(df['score'], errors='coerce')
    # add column with state number
    df['stateNo'] = df['stateAbb'].map(state_fips.set_index('stateAbb')['stateNo'])
    # add column with fips (stateNo + countyNo)
    df['fips'] = df['stateNo'] + df['countyNo']
    return df

def processChunks(file,group):
    result = []
    for chunk in pd.read_csv(file, chunksize=100000, dtype=dtype_dict):
        cleaned_chunk = cleanChunk(chunk)
        #print(cleaned_chunk.head(5))  # print first 5 rows for testing)
        result.append(cleaned_chunk)
    combined_df = pd.concat(result)
    # group by state, select score column, sums scores and counts number of people
    grouped = combined_df.groupby(group)['score'].agg(['sum', 'count']).reset_index()
    # calculate new column with  average score
    grouped['avgScore'] = (grouped['sum'] / grouped['count'])
    return grouped

def main():
    df = processChunks(file,'metroNo')
    df.to_csv('2020_RaceAverageScore_metro.csv', index=False)
    print(df.to_string())
    print("Process finished --- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()


