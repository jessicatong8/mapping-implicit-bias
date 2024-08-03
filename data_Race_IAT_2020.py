import pandas as pd

# count = 0
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
    # df_selected_range = chunk.iloc[:, 4:9]
    # print(df_selected_range.head(5))
    #filter for country of residence, state, and overall IAT D score
    filtered = chunk.loc[:,["countryres_num", "STATE","D_biep.White_Good_all"]]
    filtered.columns = ['Country', 'State', 'Score']
    # filter for people in the US, and nonempty state and scores
    filtered=filtered.loc[(filtered["Country"]=="1") & (filtered["State"] != " ") & (filtered["Score"] != " ")]
    filtered["Score"] = pd.to_numeric(filtered['Score'], errors='coerce')
    # print(filtered.head(10))
    numPeople = filtered.shape[0]
    # groupby states
    groupStates = filtered.groupby('State')['Score'].sum()
    
    return (groupStates, numPeople) 

oldChunk = None
oldPeople = 0
for chunk in pd.read_csv(file, chunksize=10000,dtype=dtype_dict):
    newChunk, newPeople = cleanChunk(chunk)
    oldPeople += newPeople
    # numPeople += cleanChunk(chunk)
    # concatenate old chunk and new chunk
    mergedChunk = pd.concat([oldChunk, newChunk], axis=1, ignore_index=True)
    # set old chunk for next iteration to the sum of old chunk and new chunk
    oldChunk = mergedChunk.sum(axis=1)
    


# print(oldChunk)
# print(oldPeople)   
averageScore = oldChunk / oldPeople
print(averageScore)


    

