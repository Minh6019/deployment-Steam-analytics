
import json
import sqlite3

import pandas as pd
from collections import OrderedDict
from sqlalchemy import create_engine

# read file

with open ("steam scrape/database.json") as f:
    data=json.load(f)

df_1=pd.DataFrame(data)
pd.set_option('display.max_columns',111)
df_2=df_1.T




df_2_sub = df_2.filter(['name', 'steam_appid', 'required_age', 'is_free','short_description','website',
             'num_reviews','review_score', 'total_positive', 'total_negative','total_reviews'])



df_3=df_2['price_overview']

df_3= pd.json_normalize(df_2['price_overview'])

df_3=df_3.drop(['initial_formatted', 'recurring_sub', 'recurring_sub_desc'], axis=1)

df_4=pd.concat([df_2_sub,df_3], axis=1)

df_4['final_formatted'] = df_4['final_formatted'].map(lambda x: str(x)[:-1])





def original_db(df):
    conn = sqlite3.connect("steam_games.db")
    c = conn.cursor()
    df.to_sql("steam_games",conn,if_exists='replace', index=False)





def flatten_json(nested_json, exclude=['']):
    "flatten nested dictionaries in json"
    out = {}

    def flatten(x, name='', exclude=exclude):
        if type(x) is dict:
            for a in x:
                if a not in exclude: flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nested_json)
    return out

# df_genres = pd.DataFrame([flatten_json(x) for x in df['genres']])

# df_2 = df_genres.filter(["0_id","0_description","1_id", "1_description"])




df_3 = df_2['price_overview'].apply(pd.Series)


df_3['final_formatted'] = df_3['final_formatted'].replace(",", ".", regex=True)
df_3['final_formatted'] = df_3['final_formatted'].replace(" ", "", regex=True)
df_price = pd.DataFrame(df_3['final'])


df_4=pd.concat([df_2_sub,df_price],axis=1)
df_4=df_4.dropna(axis=0)

print(df_4.head())
print(df_4.info())

#convert object to int and float
df_4["required_age"]=df_4["required_age"].astype(int, errors = 'raise')
df_4["num_reviews"]=df_4["num_reviews"].astype(int, errors = 'raise')
df_4["review_score"]=df_4["review_score"].astype(int, errors = 'raise')
df_4["total_positive"]=df_4["total_positive"].astype(int, errors = 'raise')
df_4["total_negative"]=df_4["total_negative"].astype(int, errors = 'raise')
df_4["total_reviews"]=df_4["total_reviews"].astype(int, errors = 'raise')
df_4['final'] = df_4['final']/100
"""df_4['final_formatted'] = df_4['final_formatted'].replace("€", "", regex=True)
#df_4['final_formatted'] = df_4['final_formatted'].replace(regex=[0-9,\.], value='')
df_4['final_formatted'] = df_4['final_formatted'].replace("[^[0-9]]|[^\.]", "", regex=True)
df_4["final_formatted"]=df_4["final_formatted"].astype(str, errors = 'raise')
df_4["final_formatted"]=df_4["final_formatted"].astype(float, errors = 'raise')
"""


conn = sqlite3.connect("steam_games.db")
c = conn.cursor()
df_2.to_sql("genres", conn, if_exists='replace', index=False)

