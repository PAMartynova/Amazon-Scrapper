import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import re
from collections import Counter


def mobiles():

    # get data from database
    conn = sqlite3.connect('amazon.db')
    conn.commit()

    data = pd.read_sql("SELECT * FROM mobiles", conn)
    conn.close()
     
    # change datatype for ratings
    data.rating = data.rating.astype("float32")

    # delete ',' from price
    data.price = data.price.map(lambda x: str(x).replace(',', ''))

    # change datatype for price
    data.price = data.price.map(lambda x: np.nan if x == 'Unknown' else x).astype('float32')

    # bring all 'IOS' rows to the same type
    data.OS = data.OS.map(lambda x: 'IOS' if 'IOS' in x else x)

    # bring all 'Anroid' rows to the same type
    def func(s):
        mat = re.search(r".*(Android\s\d*).*", s, re.I)
        return mat.groups()[0] if mat else s.strip()
    data.OS = data.OS.map(func)

    # create 'bar' chart for distribution by OS and save it
    OS_COUNTS = data.OS.value_counts()  # type - Series

    fig, ax = plt.subplots()
    bar = data.OS.map(lambda x: x if OS_COUNTS[x] > 5 else 'Other').value_counts().plot(kind='bar', title='Distribution by OS', ylabel='Amount', xlabel='OS', ax=ax, fontsize=15)
    fig.set_size_inches(25,15)
    fig.savefig('analitics/mobiles_distribution_bar.png')

    # create 'pie' chart for Distribution by OS and save it
    fig, ax = plt.subplots()
    pie = data.OS.map(lambda x: x if OS_COUNTS[x] > 10 else 'Other').value_counts().plot(kind='pie', title='Distribution by OS', ylabel='', ax=ax, fontsize=20)
    fig.set_size_inches(25, 20)
    fig.savefig('analitics/mobiles_distribution_pie.png')


    # create table for distribution by rating. Raiting: most common brand
    dic = {}
    for rait, brand in zip(data.rating, data.brand):
        dic[round(rait, 1)] = dic.get(round(rait, 1), [])
        dic[round(rait, 1)].append(brand)


    for k, v in dic.items():
        counts = Counter(v)
        dic[k] = max(v, key=lambda x: counts[x])

    rating_brand = pd.DataFrame({'Raiting': dic.keys(), 'Most Common Brand': dic.values()})
    rating_brand.to_csv('analitics/relation_rating_to_brand.csv', index=False)


    # create 'bar' chart for average price by brand
    brand_counts = data["brand"].value_counts()

    # Only keep brands that appear more than 5 times
    brands_to_keep = brand_counts[brand_counts > 5].index

    # Filter the DataFrame to only keep the brands we want to keep
    data_filtered = data[data["brand"].isin(brands_to_keep)]

    # Get the average price for each brand
    fig, ax = plt.subplots()
    data_avg_price = data_filtered.groupby("brand")["price"].mean()
    chart_price = data_avg_price.plot(kind='bar', ylabel='price', xlabel='Brand', title='Brand Average Price', ax=ax)
    
    fig.set_size_inches(17,12)
    fig.savefig('analitics/Brand_Average_Price.png')

def office():
    # get data from database
    conn = sqlite3.connect('amazon.db')
    conn.commit()
    office = pd.read_sql("SELECT * FROM new_office", conn)
    conn.close()

    # change type price to float
    office.price = office.price.map(lambda x: str(x).replace(',', ''))
    office.price = office.price.map(lambda x: np.nan if x == 'Unknown' else x).astype('float32')

    # create chart and save it
    gr = office.country.value_counts()
    fig, ax = plt.subplots()

    gr.plot(kind='bar', ylabel='Amount', xlabel='Country', title='Distribution by Country of Origin', ax=ax)

    fig.set_size_inches(15,15)
    fig.savefig('analitics/office.png')



if __name__ == "__main__":
    mobiles()
    office()