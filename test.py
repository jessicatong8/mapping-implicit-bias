import pandas as pd
import data_Race_IAT_2020

file = 'Race.IAT.public.2020.csv'

for chunk in pd.read_csv(file, chunksize=10000):
    #filter for country of residence, state, and overall IAT D score
    filtered = chunk.loc[:,["countryres_num", "STATE","D_biep.White_Good_all"]]
    filtered.columns = ['Country', 'State', 'Score']
    # filter for people in the US, and nonempty state and scores
    filtered=filtered.loc[(filtered["Country"]=="1") & (filtered["State"] != " ") & (filtered["Score"] != " ")]
    filtered["Score"] = pd.to_numeric(filtered['Score'], errors='coerce')
    print(filtered.head(5))
    groupedStates = filtered.groupby('State').size()
    # print(groupedStates.first())
    # print(groupedStates.get_group('WA'))
    # print(groupedStates.get_group('WA').shape[0])
    # count = groupedStates.size()
    print(groupedStates)
    sumStates = filtered.groupby('State')['Score'].sum()
    print(sumStates)
    df = pd.concat([sumStates, groupedStates], axis=1, ignore_index=True)
    df.columns = ['Sum', 'Count']
    print(df)
    
    break
    
    # # count number of people
    # numPeople = filtered.shape[0]
    # # groupby states
    # groupStates = filtered.groupby('State')['Score'].sum()



# Sample DataFrames
df1 = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6]
})
df2 = pd.DataFrame({
    'A': [7, 8, 9],
    'B': [10, 11, 12]
})

# Concatenate horizontally
result = pd.concat([df1, df2], axis=1)
print(result)
addTest = df1.add(df2)
print(addTest)


# Exception has occurred: ValueError
# invalid literal for int() with base 10: ' '
# TypeError: Cannot cast array data from dtype('O') to dtype('int64') according to the rule 'safe'

# During handling of the above exception, another exception occurred:

#   File "/Users/jessicatong/CS/IAT Project/IAT.github.io/data_Race_IAT_2020.py", line 49, in <module>
#     for chunk in pd.read_csv(file, chunksize=10000,dtype=dtype_dict):
# ValueError: invalid literal for int() with base 10: ' '
