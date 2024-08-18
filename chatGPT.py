import pandas as pd
import time

start_time = time.time()

file = 'Race.IAT.public.2020.csv'

dtype_dict = {
    'month': 'str',
    'day': 'str',
    'year': 'str',
    'hour': 'str',
    'weekday': 'str'
}

def clean_chunk(chunk):
    filtered = chunk.loc[:, ["countryres_num", "STATE", "D_biep.White_Good_all"]]
    filtered.columns = ['Country', 'State', 'Score']
    filtered = filtered[(filtered["Country"] == "1") & 
                        (filtered["State"].notna()) & 
                        (filtered["Score"].notna())]
    filtered["Score"] = pd.to_numeric(filtered['Score'], errors='coerce')
    return filtered

def process_chunks(file):
    result = []
    for chunk in pd.read_csv(file, chunksize=10000, dtype=dtype_dict):
        cleaned_chunk = clean_chunk(chunk)
        result.append(cleaned_chunk)
    
    combined_df = pd.concat(result)
    grouped_states = combined_df.groupby('State')['Score'].agg(['sum', 'count']).reset_index()
    return grouped_states

def main():
    df = process_chunks(file)
    df['Average'] = df['sum'] / df['count']
    df.to_csv('2020_RaceAverageScore.csv', index=False)
    print(df.to_string())
    print("Process finished --- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()
