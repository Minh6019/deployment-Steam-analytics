import streamlit as st
import pandas as pd
import json
import sqlite3
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns

#import plotly.express as px
# import shap


@st.cache
def get_data(sql,cnx):
    df= df=pd.read_sql(sql, cnx)
    return df


# Création d'une base de données Sqlite3 en mémoire
# cnx = sqlite3.connect(':memory:')
# Création d'une base de données Sqlite3:
cnx = sqlite3.connect('steam_games.db')
curs = cnx.cursor()

# Ask table df a query SQL
sql = "select * from steam_games"
curs.execute(sql)
#print(curs.fetchone())
df=pd.read_sql(sql, cnx)

header = st.container()
dataset = st.container()
features = st.container()
model_training = st.container()

st.markdown(
    '''
    <style>
    .main { 
    background-color: #F5F5F5; 
    }
    </style>
    ''',
    unsafe_allow_html=True
    )

with header:
    st.title("Welcome to my Deployment **Steam-Analytics**!")
    image = Image.open('steam.jpg')
    st.image(image, width=200)
    st.write('---')

with dataset:
    st.header('Steam dataset')
    st.text('This is our Database:')
    n_row=st.selectbox('Number of rows ?', options=[5, 10, 20, 50], index=0)
    st.write(df.head(n_row))

    # Select some rows using st.multiselect.
    st.write('### Full Dataset', df)
    selected_indices_1 = st.multiselect('Select rows:', df.index, 1)
    selected_rows = df.loc[selected_indices_1]
    st.write('### Rows Selected', selected_rows)

with features:
    st.header('Games features')
    #st.text('This is description....')
    n_age = st.selectbox('Age limit ?', options=[0, 15, 16, 17, 18], index=2)
    # Ask table df a query SQL
    if n_age==0:
        sql = "select * from steam_games where required_age >= 0"
    elif n_age==15:
        sql = "select * from steam_games where required_age >= 15"
    elif n_age==16:
        sql = "select * from steam_games where required_age >= 16"
    elif n_age==17:
        sql = "select * from steam_games where required_age >= 17"
    elif n_age==18:
        sql = "select * from steam_games where required_age >= 18"

    df_age = pd.read_sql(sql, cnx)
    st.write(df_age)
    # st.markdown('* **first feature:** I create this feature because...')

    # Select columns
    columns=df.columns.to_list()
    container = st.container()
    all = st.checkbox("Select all")
    #['A', 'B', 'C'], ['A', 'B', 'C']

    if all:
        selected_options = container.multiselect("Select one or more options:",
                                                 columns, columns)
    else:
        selected_options = container.multiselect("Select one or more options:",
                                                 columns,default='name')

    string_selected =""

    for i in range(len(selected_options)):
        if i==0:
            string_selected=string_selected + selected_options[i]
        else:
            string_selected = string_selected + ", " + selected_options[i]

    sql = "SELECT "+ string_selected + " FROM steam_games"
    st.text(sql)
    if string_selected != "":
        df_select = pd.read_sql(sql, cnx)
        st.write(df_select)

with model_training:
    st.header('Plotting')
    #st.text('This is description....')
    sel_col, disp_col = st.columns(2)

    #first column:
    sel_col.subheader('Review_score count')
    rev_score= pd.DataFrame(df['review_score'].value_counts()).head(50)
    sel_col.bar_chart(rev_score, width=80)

    # 2nd column:

    disp_col.subheader('Price / total_positive:')
    x_max = disp_col.slider('X scale_max: ', 200, 1500, 1000)
    y_max = disp_col.slider('Y scale_max: ', 10, 200, 100)
    fig, ax = plt.subplots()
    #sns.lmplot(x='total_positive', y='final', data=df)
    #sns.distplot(df['final'])
    #sns.lmplot(x='num_reviews', y='final', data=df,
    #           fit_reg=False,  # No regression line
    #           hue='review_score')  # Color by evolution stage
    #plt.bar(df['total_positive'],df['final'])
    #ax.hist(df['total_positive'], rwidth=0.8)
    ax.scatter(x=df['total_positive'], y=df['final'], c='blue', alpha=0.3, edgecolors='red')
    #sns.distplot(df['total_positive'])
    plt.xlabel("total_positive")
    plt.ylabel("final (price)")
    plt.xlim(0,x_max)
    plt.ylim(0,y_max)
    disp_col.write(fig)

