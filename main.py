import pandas as pd
import streamlit as st
import plotly.express as px
from numerize.numerize import numerize
import feedparser


st.set_page_config(page_title='NEO Close Approach Dashboard',
                   layout='wide',
                   initial_sidebar_state='expanded')


@st.cache_data
def get_data():
    try:
        df = pd.read_csv('NEO.csv')
        return df
    except FileNotFoundError:
        st.error('NEO.csv file not found. Please check the file path.')
        return pd.DataFrame()
    except Exception as e:
        st.error(f'Error occurred while loading the data: {e}')
        return pd.DataFrame()


df = get_data()

df = df.rename(columns={
    'Close-Approach (CA) Date': 'CA_Date',
    'CA DistanceNominal (au)': 'CA_DistanceNominal',
    'V relative(km/s)': 'V_relative',
    'V infinity(km/s)': 'V_infinity'
})

header_left, header_mid, header_right = st.columns([1, 6, 1], gap='large')

with header_mid:
    st.title('NEO Close Approach Dashboard')
with st.sidebar:
    add_all_neos = st.checkbox("Add All", value=False)
    if add_all_neos:
        object_filter = st.multiselect(label='Select NEO',
                                       options=df['Object'].unique(),
                                       default=df['Object'].unique())
    else:
        object_filter = st.multiselect(label='Select NEO',
                                       options=df['Object'].unique(),
                                       default=df['Object'].unique()[0:10])

    rarity_filter = st.multiselect(label='Select Rarity',
                                   options=df['Rarity'].unique(),
                                   default=df['Rarity'].unique()[0:3])


    distance_nominal_filter = st.slider(label='Select Nominal Distance (au)',
                                        min_value=float(df['CA_DistanceNominal'].min()),
                                        max_value=float(df['CA_DistanceNominal'].max()),
                                        value=(float(df['CA_DistanceNominal'].min()), float(df['CA_DistanceNominal'].max())))

df1 = df.query('Object == @object_filter & Rarity == @rarity_filter & @distance_nominal_filter[0] <= CA_DistanceNominal <= @distance_nominal_filter[1]')
# df1 = df.query('Object == @object_filter & CA_Date == @date_filter & CA_DistanceNominal == @distance_nominal_filter')

if not df1.empty:
    total_neo = len(df1) + 1
    mean_diameter = float(df1["Diameter"].mean())
    mean_velocity_relative = float(df1["V_relative"].mean())
    mean_velocity_infinity = float(df1["V_infinity"].mean())
else:
    # If df1 is empty, provide default values or show a message
    total_neo = 0.0
    mean_diameter = 0.0
    mean_velocity_relative = 0.0
    mean_velocity_infinity = 0.0

total_1, mean_1, mean_2, mean_3 = st.columns(4, gap='large')

with total_1:
    st.image('images/asteroid.png', use_column_width='Auto')
    st.metric(label='Total NEOs', value=numerize(total_neo))

with mean_1:
    st.image('images/diameter.png', use_column_width='Auto')
    st.metric(label='Avg. Diameter', value=numerize(mean_diameter))

with mean_2:
    st.image('images/speedometer.png', use_column_width='Auto')
    st.metric(label='Avg. Relative Velocity', value=numerize(mean_velocity_relative))

with mean_3:
    st.image('images/infinity.png', use_column_width='Auto')
    st.metric(label='Avg. Infinity Velocity ', value=numerize(mean_velocity_infinity))

Q1, Q2 = st.columns(2)

with Q1:
    fig_scatter = px.scatter(df1, x='CA_DistanceNominal', y='V_relative',
                             color='Object',
                             title='<b>Close-Approach Distance vs. Relative Velocity</b>')
    fig_scatter.update_xaxes(rangeslider_visible=True)
    st.plotly_chart(fig_scatter, use_container_width=True)

with Q2:
    fig_pie = px.pie(df1, names='Rarity', title='<b>Rarity Distribution</b>', hole=.3,
                     color_discrete_sequence=px.colors.qualitative.Dark24)
    fig_pie.update_layout(showlegend=True)
    st.plotly_chart(fig_pie, use_container_width=True)


Q3, Q4 = st.columns(2)

with Q3:
    fig_box = px.box(df1, x='Rarity', y='V_relative',
                     hover_data=['Object'], title='<b>Relative Velocity vs. Rarity</b>')
    fig_box.update_xaxes(rangeslider_visible=True)
    st.plotly_chart(fig_box, use_container_width=True)
with Q4:
    fig_hist = px.histogram(df1, x='CA_DistanceNominal', nbins=20,
                            title='<b>Distribution of Close-Approach Distances (au)</b>')
    fig_hist.update_xaxes(rangeslider_visible=True)
    st.plotly_chart(fig_hist, use_container_width=True)

if not df1.empty:
    st.header('Detailed Info for Selected NEOs')
    st.table(df1[['Object', 'CA_Date', 'CA_DistanceNominal', 'V_relative', 'V_infinity', 'Rarity']])
else:
    st.warning('No NEOs found with the selected filters.')

def aggregate_neo_news_feeds(feed_urls, limit=10):
    aggregated_entries = []

    for url in feed_urls:
        feed = feedparser.parse(url)
        entries = feed.entries[:limit]
        aggregated_entries.extend(entries)

    # Sort the entries by date (most recent first)
    aggregated_entries.sort(key=lambda x: x.published_parsed, reverse=True)

    return aggregated_entries[:limit]

st.header('NEO News')
# List of RSS feed URLs related to NEOs and space exploration
neo_news_feeds = [
    "https://cneos.jpl.nasa.gov/feed/news.xml"
]

aggregated_neo_news = aggregate_neo_news_feeds(neo_news_feeds)

for entry in aggregated_neo_news:
    st.write(entry.title)
    st.write(entry.link)
    st.write(entry.published)
    st.write("=" * 30)
