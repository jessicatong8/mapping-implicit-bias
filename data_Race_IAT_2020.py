import pandas as pd

# count = 0
#D_biep.White_Good_all: Overall IAT D Score
# countryres_num	Country of Residence
    # 1: USA
# STATE	2-letter State name for US residents
# CountyNo	County No. for US residents
# MSANo	Metropolitan Statistical Area No. for US residents
# MSAName	Metropolitan Statistical Area Name for US residents


for chunk in pd.read_csv('Race.IAT.public.2020.csv', chunksize=1000):
    #filter for country of residence, state, and overall IAT D score
    df = chunk.loc[:,["countryres_num", "STATE","D_biep.White_Good_all"]]
    # filter for people in the US, and nonempty state and scores
    df=df.loc[(df["countryres_num"]=="1") & (df["STATE"] != " ") & (df["D_biep.White_Good_all"] != " ")]
    print(df.head(10)) 
    
    
    
    # Process each chunk
    # if count < 2:
    #     print(chunk.head()) 
    #     count += 1
    # else:
    #     break