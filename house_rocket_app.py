import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly as plt
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster, marker_cluster

st.set_page_config(layout='wide')

@st.cache(allow_output_mutation=True)
def get_data(path):
    data = pd.read_csv(path)
    return data

def date_format (df):
    df['date'] = pd.to_datetime(df['date'])
    return df


def drop_features (df):
    df = df.drop(['sqft_living15', 'sqft_lot15'], axis=1)
    return df


def delete_duplicates(df):
    df = df.drop_duplicates(subset = ['id'], keep = 'last')
    return df

def transform_feature(df):
    for i in range (len(df)):
        if (df.loc[i, 'waterfront']  == 0): 
            df.loc[i, 'waterfront']  = 'no'
        elif (df.loc[i, 'waterfront']  == 1):
            df.loc[i, 'waterfront']  = 'yes'
    return df


def new_features(df):
    df['age_build'] = df['yr_built'].apply(lambda x: 'build <1955' if x < 1955 else 'build > 1955')

    df['basement'] = df['sqft_basement'].apply(lambda x: 'basement' if x > 0 else 'no_basement')

    df['renovation'] = df['yr_renovated'].apply(lambda x: 'renovation' if x > 0 else 'no_renovation')

    df['condition_type'] = df['condition'].apply(lambda x: 'bad' if x <=2 else
                                                           'regular' if x == 3 or x == 4 else
                                                           'good') 

    df['year']= df['date'].dt.year

    df['month'] = df['date'].dt.month

    df['season'] = df['month'].apply(lambda x: 'summer' if (x > 6) & (x <= 9) else
                                               'spring' if (x > 3) & (x <= 6) else
                                               'fall' if (x > 9) & (x <= 12) else
                                               'winter')

    return df

def data_overview(df):
    st.title('House Rocket Project')
    st.sidebar.title('House Rocket Project')
    st.sidebar.write('''House Rocket is a platform for buying and selling properties. Its business model is buying properties 
                        and then selling them at a higher price.
                        The goal is to maximize the profit of the company, finding good deals.''')
    st.sidebar.write("Here you can find more information on this project: "
                         "[GitHub](https://github.com/cmfonseca/project-house-rocket)")
    if st.checkbox('Show raw dataset'):
        st.header('Data Overview')
        f_attributes = st.sidebar.multiselect('Enter columns', df.columns)
        f_zipcode = st.sidebar.multiselect('Enter zipcode', df['zipcode'].unique())
        if f_zipcode != [] and f_attributes != []:
            df = df.loc[df['zipcode'].isin(f_zipcode), f_attributes]
        elif f_zipcode != [] and f_attributes == []:
            df = df.loc[df['zipcode'].isin(f_zipcode), :]
        elif f_zipcode == [] and f_attributes != []:
            df = df.loc[:, f_attributes]
        else:
            df = df.copy()

        st.dataframe(df)

    
    return None


def descript_stat (df):
    st.header('Descriptive Statistics')
    num_attributes = df.select_dtypes(include=['int64', 'float64'])
    num_attributes = num_attributes.iloc[:, 1:]
    #Estimates of location
    avg = pd.DataFrame(num_attributes.apply(np.mean))
    median = pd.DataFrame(num_attributes.apply(np.median))

    #Estimates of variability
    std = pd.DataFrame(num_attributes.apply(np.std))
    max_ = pd.DataFrame(num_attributes.apply(np.max))
    min_ = pd.DataFrame(num_attributes.apply(np.min))

    #Concat
    d_st = pd.concat([avg, median, std, min_, max_], axis=1).reset_index()

    #Changing column names
    d_st.columns = ['features', 'average', 'median', 'std', 'min', 'max']

    st.dataframe(d_st, width = 900)
    return df

def data_analysis(df):
    st.header('Data Insights')
    #######
    #H01
    #######
    c1, c2 = st.beta_columns(2)
    c1.subheader('H01: Properties that are waterfront are, in average, 30% more expensive.')

    water_price = df[['price', 'waterfront']].groupby('waterfront').mean().reset_index()
    fig = px.bar(water_price, x="waterfront", y="price", color = 'waterfront', template= 'seaborn',
                labels={'waterfront':'Waterfront', 'price': 'Property Price'})
    fig.update_layout(showlegend=False)
    c1.plotly_chart(fig, use_container_width=True)


    #######
    #H02
    #######
    c2.subheader('H02: Properties built before 1955 are, in average, 50% less expensive.')
    build_price = df[['price', 'age_build']].groupby('age_build').mean().reset_index()
    fig = px.bar(build_price, x="age_build", y="price", color='age_build', template= 'seaborn',
                labels={'age_build':'Age of the Building', 'price': 'Property Price'})
    fig.update_layout(showlegend=False)
    c2.plotly_chart(fig, use_container_width=True)

    #######
    #H03
    #######
    c1, c2 = st.beta_columns(2)
    c1.subheader('H03: Properties without basement have a sqrt_lot 50% bigger than the ones with basement.')
    basement_lot = df[['sqft_lot', 'basement']].groupby('basement').sum().reset_index()
    fig = px.bar(basement_lot, x="basement", y="sqft_lot", color='basement', template = 'seaborn',
                labels={'basement':'Basement', 'sqft_lot': 'Property Lot Size'})
    fig.update_layout(showlegend=False)
    c1.plotly_chart(fig, use_container_width=True)

    #######
    #H04
    #######
    c2.subheader('H04: Properties with higher number of bedrooms are, in average, 10% more expensive.')
    bedrooms_price = df[['price', 'bedrooms']].groupby('bedrooms').mean().reset_index()
    bedrooms_price['bedrooms']= bedrooms_price['bedrooms'].astype(str)
    fig = px.bar(bedrooms_price, x="bedrooms", y="price", color='bedrooms', template='seaborn',
                labels={'bedrooms':'Number of Bedrooms', 'price': 'Property Price'})
    fig.update_layout(showlegend=False)
    c2.plotly_chart(fig, use_container_width=True)

    #######
    #H05
    #######
    c1, c2 = st.beta_columns(2)
    c1.subheader('H05: Properties that were never renovated are, in average, 20% less expensive.')
    renovation_price = df[['price', 'renovation']].groupby('renovation').mean().reset_index()
    fig = px.bar(renovation_price, x="renovation", y="price", color='renovation', template='seaborn', 
                labels={'renovation':'Renovation', 'price': 'Property Price'})
    fig.update_layout(showlegend=False)
    c1.plotly_chart(fig, use_container_width=True)


    #######
    #H06
    #######
    c2.subheader('H06: Older properties that were never renovated are 40% less expensive.')
    data = df[df['age_build'] == 'build <1955']
    renovation_price = data[['price', 'renovation']].groupby('renovation').mean().reset_index()
    fig = px.bar(renovation_price, x="renovation", y="price", color='renovation', template='seaborn', 
                labels={'renovation':'Renovation', 'price': 'Property Price'})
    fig.update_layout(showlegend=False)
    c2.plotly_chart(fig, use_container_width=True)

    #######
    #H07
    #######
    c1, c2 = st.beta_columns(2)
    c1.subheader('H07: Properties that were renovated recently are, in average, 10% more expensive.')
    data = df[df['renovation'] == 'renovation']
    data = data.copy()
    data['age_renovation'] = data['yr_renovated'].apply(lambda x: 'new_renovation' if x >= 2000 else 'old_renovation')
    new_renovation_price = data[['price', 'age_renovation']].groupby('age_renovation').mean().reset_index()
    fig = px.bar(new_renovation_price, x="age_renovation", y="price", color='age_renovation', 
                template = 'seaborn', labels={'age_renovation':'Age of Renovation', 'price': 'Property Price'})
    fig.update_layout(showlegend=False)
    c1.plotly_chart(fig, use_container_width=True)

    #######
    #H08
    #######
    c2.subheader('H08: Older properties that were never renovated are 40% less expensive.')
    data = df[df['condition_type'] == 'bad']
    bad_water_price = data[['price', 'waterfront']].groupby('waterfront').mean().reset_index()
    fig= px.bar(bad_water_price, x="waterfront", y="price", color='waterfront', template='seaborn', 
                labels={'waterfront':'Waterfront', 'price': 'Property Price'})
    fig.update_layout(showlegend=False)
    c2.plotly_chart(fig, use_container_width=True)

    #######
    #H09
    #######
    c1, c2 = st.beta_columns(2)
    c1.subheader('H09: The YoY (Year over Year) growth of the price of the properties is of 10%.')
    YoY = df[['year', 'price']].groupby('year').median().reset_index()
    YoY['year']= YoY['year'].astype(str)
    fig = px.bar(YoY, x="year", y="price", color='year', template='seaborn', labels={'year':'Year', 'price': 'Property Price'})
    fig.update_layout(showlegend=False)
    c1.plotly_chart(fig, use_container_width=True)

    #######
    #H10
    #######
    c2.subheader('H10: The MoM (Month over Month) growth of the price of the properties is 15%.')
    MoM = df[['price', 'year', 'month']].groupby('month').mean().reset_index()
    MoM['month']=MoM['month'].apply(lambda x: 'Jan' if x == 1 else
                                            'Feb' if x == 2 else
                                            'Mar' if x == 3 else
                                            'Apr' if x == 4 else
                                            'May' if x == 5 else
                                            'Jun' if x == 6 else
                                            'Jul' if x == 7 else
                                            'Aug' if x == 8 else
                                            'Sep' if x == 9 else
                                            'Oct' if x == 10 else
                                            'Nov' if x == 11 else 'Dec')
    fig= px.line(MoM, x='month', y='price', template='seaborn', labels={'month':'Month', 'price': 'Property Price'})
    fig.update_traces(mode='markers+lines')
    c2.plotly_chart(fig, use_container_width=True)


def business_challenges(df):
    st.header('Data Insights')

    ###############
    #Q.01
    ###############
    st.subheader('1. Which properties should House Rocket buy, and at what price?')
    data = df[['id', 'zipcode', 'price', 'condition', 'lat', 'long', 'season']]
    data = data.copy()
    # Determine median price by zipcode
    zipcode_price = data[['zipcode', 'price']].groupby('zipcode').median().reset_index()

    # Defining buying strategy
    buy_strat = pd.merge(zipcode_price, data, on='zipcode', how='inner') # Join columns
    buy_strat = buy_strat.rename(columns={'price_x': 'zipcode_median', 'price_y': 'property_price'}) # Rename columns
    buy_strat = buy_strat.reindex(columns=['id', 'zipcode', 'lat', 'long', 'season', 
                                        'condition', 'zipcode_median', 'property_price']) # Order columns
    buy_strat['buy'] = 'NA' # Create empty column

    # Populate column buy
    # Buy only properties in regular/good condition and with prices below the median price by zipcode
    for i in range (len(buy_strat)):
        if (buy_strat.loc[i, 'zipcode_median']  >= buy_strat.loc[i, 'property_price']) & (buy_strat.loc[i, 'condition'] > 3): 
            buy_strat.loc[i, 'buy']  = 'yes'
        else:
            buy_strat.loc[i, 'buy']  = 'no'
    # Map
    data_map = buy_strat[['id', 'lat', 'long', 'property_price', 'condition', 'buy', 'zipcode_median']]

    buy_map = folium.Map(location=[df['lat'].mean(), df['long'].mean()],
                    width= 600,
                    height=300,
                    default_zoom_start=30)
    for i, row in data_map.iterrows():
        if row['buy'] == 'yes':
            folium.CircleMarker([row['lat'], row['long']], color="#2e8540", fill=True, fill_color="#3186cc", radius= 5,
                                                        popup=('''Price ${0}. 
                                                        Condition: {1}, 
                                                        Zipcode median ${2}
                                                        Buy: {3}''').format(row['property_price'], 
                                                        row['condition'],
                                                        row['zipcode_median'],                                                     
                                                        row['buy']),).add_to(buy_map)
        else:
            folium.CircleMarker([row['lat'], row['long']], color="#cd2026", fill=True, fill_color="#3186cc", radius= 5,
                                            popup=('''Price ${0}. 
                                            Condition: {1}, 
                                            Zipcode median ${2}
                                            Buy: {3}''').format(row['property_price'], 
                                            row['condition'],
                                            row['zipcode_median'],                                                     
                                            row['buy']),).add_to(buy_map)

    folium_static(buy_map)

    ###############
    #Q.02
    ###############
    st.subheader('2. Once the property is aquired, what is the best moment to sell, and by which price?')

    data = buy_strat[buy_strat['buy'] == 'yes']

    # Determine median price by zipcode, by season
    season_zip_price = data[['season', 'zipcode', 'property_price']].groupby(['zipcode', 'season']).median().reset_index()
    season_zip_price = season_zip_price.rename(columns={'season': 'season_median', 'property_price': 'season_prop_price'})

    # Defining selling strategy
    sell_strat = pd.merge(season_zip_price, data, on='zipcode', how='inner') # Join columns
    sell_strat = sell_strat.reindex(columns=['id', 'zipcode', 'lat', 'long', 'season', 
                                            'condition', 'zipcode_median', 'season_median', 'season_prop_price',
                                            'property_price']) # Order columns

    sell_strat['sell_price'] = 'NA' # Create empty column

    # Populate column buy
    for i in range (len(sell_strat)):
        if (sell_strat.loc[i, 'property_price'] >= sell_strat.loc[i, 'season_prop_price']): 
            sell_strat.loc[i, 'sell_price']  = sell_strat.loc[i, 'property_price'] * 1.1
        else:
            sell_strat.loc[i, 'sell_price']  = sell_strat.loc[i, 'property_price'] * 1.3
    st.subheader('Selling price of the properties')
    sell_strat['sell_price'] = sell_strat['sell_price'].astype(float)
    sell_strat['sell_price'] = sell_strat['sell_price'].round(decimals=2)
    st.dataframe(sell_strat[['id', 'season', 'property_price', 'sell_price']], width = 900)

    st.subheader('Best time to sell')
    fig = px.bar(sell_strat, x='season', y='sell_price', color ='season', 
                labels={'season':'Season', 'sale': 'Selling Price'})
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, x='season', y='sell_price', use_container_width=True)
    
    st.subheader('Total profit')
    sell_strat['profit'] = sell_strat['sell_price'] - sell_strat['property_price']
    total_profit = sell_strat['profit'].sum()
    st.write(f'The total profit (profit = buying price - selling price) of the properties in the portfolio is: ${total_profit:.2f}')

    st.subheader('Business Results')
    st.markdown('''| ID | Description | Conclusion |
                | --- | --- | --- |
                | H01 | Properties that are waterfront are, in average, 30% more expensive. | TRUE |
                | H02 | Properties built before 1955 are, in average, 50% less expensive. | FALSE |
                | H03 | Properties without basement have a sqrt_lot 50% bigger than the ones with basement. | TRUE |
                | H04 | Properties with higher number of bedrooms are, in average, 10% more expensive. | FALSE |
                | H05 | Properties that were never renovated are, in average, 20% less expensive. | TRUE |
                | H06 | Older properties that were never renovated are 40% less expensive. | FALSE |
                | H07 | Properties that were renovated recently are 10% more expensive. | TRUE |
                | H08 | Properties in bad condition but with that are waterfront, are 10% more expensive. | TRUE |
                | H09 | The YoY (Year over Year) growth of the price of the properties is of 10%. | FALSE |
                | H10 | The MoM (Month over Month) growth of the price of the properties is 15%. | FALSE |''', 
                unsafe_allow_html=False)
    
    return None
    

if __name__ == "__main__":
    path = 'kc_house_data.csv'
    df = get_data(path)
    drop_features(df)
    delete_duplicates(df)
    date_format(df)
    transform_feature(df)
    new_features(df)
    data_overview(df)
    descript_stat(df)
    data_analysis(df)
    business_challenges(df)