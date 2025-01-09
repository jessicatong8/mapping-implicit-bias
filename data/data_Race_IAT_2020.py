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

file = '/Users/jessicatong/Documents/IAT/Race.IAT.public.2020.csv'

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

state_fips = pd.read_csv('mapping-implicit-bias/data/us-state-fips.csv',dtype=state_fips_dtype)
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

def jsonify(in_file, out_file):
    """
    param: in_file (str) file path to csv
    param: out_file (str) file path to output json
    return: json representation in the format  {'id': 'US.WA', 'value': 0.1234}
    """

    df = pd.read_csv(in_file)
    # Drop columns
    df.drop(['Sum', 'Count'], axis=1, inplace=True)
    # Rename columns
    df.columns = ['id', 'value']
    # Add prefix 'US.' to stateAbb
    df['id'] = 'US.' + df['id']
    # Round value to 4 decimal places
    df['value'] = df['value'].round(4)
    print(df)
    # Write to json file, one record per line for lines=True option in to_json() function.
    df.to_json(out_file, orient='records', lines=True)


def main():
    # df = processChunks(file,'stateAbb')
    # df.to_csv('test.csv', index=False)
    # print(df.to_string())
    # print("Process finished --- %s seconds ---" % (time.time() - start_time))

    jsonify("mapping-implicit-bias/data/2020_RaceAverageScore_States.csv", "mapping-implicit-bias/data/states_2020.json")

if __name__ == "__main__":
    main()


