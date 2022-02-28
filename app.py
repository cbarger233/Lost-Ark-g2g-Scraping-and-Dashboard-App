from cProfile import label
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

#read in the gold information
df = pd.read_csv('global_info.csv')
df1 = pd.read_csv('region_info.csv')
#df1.date = pd.to_datetime(df1.date)
df2 = pd.read_csv('server_info.csv')
df3 = pd.read_csv('current_names.csv')
df4 = pd.read_csv('names_historical.csv')
df5 = pd.read_csv('gold_info.csv')
df6 = df5.groupby(['name', 'date'])['price'].mean().reset_index()



app = Dash(__name__)
server = app.server


#figure for the global gold prices
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.date, y=df['min'], fill='tozeroy', name='Min Price', legendrank=1, marker_color='rgba(152, 0, 0, .8)'))
fig.add_trace(go.Scatter(x=df.date, y=df['mean'], fill='tonexty', name='Average Price', legendrank=2, marker_color='rgba(212, 90, 93, .9)'))
fig.update_layout(
    title = 'Global Mean and Minimum Prices Per Gold',
    title_font = {"size": 25}
)
fig.update_xaxes(
    tickangle = 30,
    title_text = "Date",
    title_font = {"size": 20},
)
fig.update_yaxes(
    title_text = "Price (USD)",
    title_standoff = 25,
    title_font = {"size": 20}
)

#figure for the daily gold sellers with most listings
fig2 = px.bar(
    data_frame = df3.head(40),
    x='Seller',
    y='Listings',
    template='presentation',
    color='Listings',
    text_auto=True,
    title='Top Daily Listings by Seller',
    color_continuous_scale='tealgrn'
)
fig2.update_layout(
    xaxis=dict(tickfont=dict(size=10))
)


#--------------------------------------------------------------------------
#the app layout
#this is essentially the html code for the web application
#except a lot easier than html lol
app.layout = html.Div([
    html.H1('Lost Ark Gold Prices on g2g', style={'text-align': 'center'}),


    #global average and minimum gold prices graph
    html.Div([
        dcc.Graph(id='global_gold_prices',
        figure=fig)
    ]),


    #server gold prices mean and min
    html.Div([
        dcc.Graph(id='server_and_region_prices'),
        'Select a server to view gold prices: ',
        dcc.Dropdown(
            id='select_server',
            options=[
                {'label':'Adrinne', 'value':'Adrinne'},
                {'label':'Agaton', 'value':'Agaton'},
                {'label':'Akkan', 'value':'Akkan'},
                {'label':'Aldebaran', 'value':'Aldebaran'},
                {'label':'Antares', 'value':'Antares'},
                {'label':'Arcturus', 'value':'Arcturus'},
                {'label':'Asta', 'value':'Asta'},
                {'label':'Avesta', 'value':'Avesta'},
                {'label':'Azena', 'value':'Azena'},
                {'label':'Beatrice', 'value':'Beatrice'},
                {'label':'Bergstrom', 'value':'Bergstrom'},
                {'label':'Brelshaza', 'value':'Brelshaza'},
                {'label':'Calvasus', 'value':'Calvasus'},
                {'label':'Danube', 'value':'Danube'},
                {'label':'Elzowin', 'value':'Elzowin'},
                {'label':'Enviska', 'value':'Enviska'},
                {'label':'Feiton', 'value':'Feiton'},
                {'label':'Galatur', 'value':'Galatur'},
                {'label':'Gienah', 'value':'Gienah'},
                {'label':'Inanna', 'value':'Inanna'},
                {'label':'Kadan', 'value':'Kadan'},
                {'label':'Karta', 'value':'Karta'},
                {'label':'Kazeros', 'value':'Kazeros'},
                {'label':'Kharmine', 'value':'Kharmine'},
                {'label':'Kurzan', 'value':'Kurzan'},
                {'label':'Ladon', 'value':'Ladon'},
                {'label':'Mari', 'value':'Mari'},
                {'label':'Mokoko', 'value':'Mokoko'},
                {'label':'Moonkeep', 'value':'Moonkeep'},
                {'label':'Neria', 'value':'Neria'},
                {'label':'Nineveh', 'value':'Ninevah'},
                {'label':'Petrania', 'value':'Petrania'},
                {'label':'Prideholme', 'value':'Prideholme'},
                {'label':'Procyon', 'value':'Procyon'},
                {'label':'Punika', 'value':'Punika'},
                {'label':'Regulus', 'value':'Regulus'},
                {'label':'Rethramis', 'value':'Rethramis'},
                {'label':'Rohendel', 'value':'Rohendel'},
                {'label':'Sasha', 'value':'Sasha'},
                {'label':'Sceptrum', 'value':'Sceptrum'},
                {'label':'Shadespire', 'value':'Shadespire'},
                {'label':'Shandi', 'value':'Shandi'},
                {'label':'Sirius', 'value':'Sirius'},
                {'label':'Slen', 'value':'Slen'},
                {'label':'Stonehearth', 'value':'Stonehearth'},
                {'label':'Thaemine', 'value':'Thaemine'},
                {'label':'Thirain', 'value':'Thirain'},
                {'label':'Tortoyk', 'value':'Tortoyk'},
                {'label':'Tragon', 'value':'Tragon'},
                {'label':'Trixion', 'value':'Trixion'},
                {'label':'Una', 'value':'Una'},
                {'label':'Valtan', 'value':'Valtan'},
                {'label':'Vern', 'value':'Vern'},
                {'label':'Vykas', 'value':'Vykas'},
                {'label':'Wei', 'value':'Wei'},
                {'label':'Yorn', 'value':'Yorn'},
                {'label':'Zinnervale', 'value':'Zinnervale'},
                {'label':'Zosma', 'value':'Zosma'},
                {'label':'Альдеран', 'value':'Альдеран'},
                {'label':'Кратос', 'value':'Кратос'}
            ],
            multi=False,
            value = 'Agaton',
            style={'width':'40%'}
        ),
        
        
        'Select a region to view gold prices:',
        dcc.Dropdown(
            id='select_region',
            options=[
                {'label':'EU Central', 'value':'EU Central'},
                {'label':'EU West', 'value':'EU West'},
                {'label':'US East', 'value':'US East'},
                {'label':'US West', 'value':'US West'},
                {'label':'Korea', 'value':'KR'},
                {'label':'Russia', 'value':'RU'},
                {'label':'Japan', 'value':'JP'},
                {'label':'South America', 'value':'SA'}
            ],
            multi=False,
            value = 'EU Central',
            style={'width':'40%'}
        )

    ]),

    #daily gold seller listings
    html.H2('Gold Sellers with the Most Listings'),
    html.Div([
        dcc.Graph(id='gold_sellers',
        figure=fig2)
    ]),


    #Graph for individual seller information
    html.Div(
        html.Div([
            dcc.Graph(id='individual_seller_info'),
            'Input Seller Name (case-sensitive): ',
            dcc.Input(id='user_input', value='lucky', type='text')
        ])
    ),



    html.Br(),
    html.H6('Made in 2022 by Colton Barger')

])


#-------------------------------------------------------------------------------------------------------------
#Update the gold prices for the selected region and selected server from the dropdown
#user chooses a region and a server to view on the dashboard
@app.callback(
    Output(component_id='server_and_region_prices', component_property='figure'),
    Input(component_id='select_server', component_property='value'),
    Input(component_id='select_region', component_property='value')
)
def update_server_region_graph(selected_server, selected_region):
    server_df = df2.copy()
    server_df = server_df[server_df['server'] == selected_server]

    region_df = df1.copy()
    region_df = region_df[region_df['region'] == selected_region]

    fig1 = make_subplots(rows=1, cols=2, subplot_titles=[f'Prices in {selected_server}', f'Prices in {selected_region}'])
    fig1.add_trace(
        go.Scatter(x=server_df['date'], y=server_df['min'], fill='tozeroy', name='Server Min Price', legendrank=4),
        row=1, col=1
    )
    fig1.add_trace(
        go.Scatter(x=server_df['date'], y=server_df['mean'], fill='tonexty', name='Server Average Price', legendrank=3),
        row=1, col=1
    )

    fig1.add_trace(
        go.Scatter(x=region_df['date'], y=region_df['min'], fill='tozeroy', name='Region Min Price', legendrank=2),
        row=1, col=2
    )
    fig1.add_trace(
        go.Scatter(x=region_df['date'], y=region_df['mean'], fill='tonexty', name='Region Average Price', legendrank=1),
        row=1, col=2
    )

    fig1.update_xaxes(title_text='Date')
    #fig1.update_xaxes(title_text='Date', row=1, col=2)
    fig1.update_yaxes(title_text='Price')
    
    return fig1

#---------------------------------------------------------------------------------
#updating the graph for information on individual sellers. The dashboard
#user inputs the name of a seller they want to lok at and they can view
#the number of listings for that seller over time and their average prices
@app.callback(
    Output(component_id='individual_seller_info', component_property='figure'),
    Input(component_id='user_input', component_property='value')
)
def update_seller_info(seller_name):
    temp=df4.copy()

    filtered_df6 = df6[df6['name'] == seller_name]
    filtered_df = temp[temp['name'] == seller_name]
    fig1 = make_subplots(rows=1, cols=2,
    subplot_titles=('Number of Listings', 'Average Price'))
    fig1.add_trace(
        go.Scatter(x=filtered_df['date'], y=filtered_df['price'], name='Number of Listings'),
        row=1, col=1)
    fig1.add_trace(
        go.Scatter(x=filtered_df6['date'], y=filtered_df6['price'], name='Average Price'),
        row=1, col=2)
    
    #updating x-axis labels
    fig1.update_xaxes(title_text='Date', row=1, col=1)
    fig1.update_xaxes(title_text='Date', row=1, col=2)
    
    #updating y-axis labels
    fig1.update_yaxes(title_text='Listings', row=1, col=1)
    fig1.update_yaxes(title_text='Average Price', row=1, col=2)
    return fig1


if __name__ == '__main__':
    app.run_server(debug=True)