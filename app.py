import numpy as np
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import webbrowser

# Plotly mapbox public token
mapbox_access_token = "pk.eyJ1IjoicjIwMTY3MjciLCJhIjoiY2s1Y2N4N2hoMDBrNzNtczBjN3M4d3N4diJ9.OrgK7MnbQyOJIu6d60j_iQ"

# ------------------------------------------------- IMPORTING DATA -----------------------------------------------------

df = pd.read_csv("./data/final_df.csv")


# ----------------------------------------------------- FIGURES --------------------------------------------------------
colors = {
    'background': '#34495E ',
    'text': 'white'
}

def plots_actualize(df2):
    fig_map = go.Figure(
        data=go.Scattermapbox(
            lat=df2["latitude"],
            lon=df2["longitude"],
            mode="markers",
            marker=dict(
                color="navy")),
        layout=go.Layout(
            autosize=True,
            margin=go.layout.Margin(l=0, r=0, t=0, b=0),
            showlegend=False,
            mapbox=dict(
                accesstoken=mapbox_access_token,
                style="light",
                center={'lat': 30.26, 'lon': -97.7},
                zoom=8.5,
            )
        )
    )

    pie_colors = ["#636EFA", "#4296f5", "#42ddf5"]
    unique_rooms = list(df2.room_type.unique())
    if len(unique_rooms) == 1:
        if unique_rooms[0] == 'Private room':
            pie_colors = ["#4296f5"]
        elif unique_rooms[0] == 'Shared room':
            pie_colors = ["#42ddf5"]

    fig_pie = go.Figure(
        data=go.Pie(
            labels=df2['room_type'].value_counts().index,
            values=df2['room_type'].value_counts().values,
            textinfo='text+value+percent',
            text=df2['room_type'].value_counts().index,
            hoverinfo='label',
            showlegend=False,
            textfont=dict(
                color="white"
            ),
            marker=(
                dict(
                    colors=pie_colors,
                    line=dict(
                        color="white",
                        width=0.5
                    )
                )
            )
        ),
        layout=go.Layout(
            paper_bgcolor='dimgray',
            plot_bgcolor='dimgray',
            margin=go.layout.Margin(l=0, r=0, t=0, b=0),
        )
    )

    fig_bar = go.Figure(
        data=go.Bar(
            x=df2['ordinal_rating'].value_counts().values,
            y=df2['ordinal_rating'].value_counts().index,
            orientation='h',
            marker=dict(
                line=dict(
                    color="white"
                )
            )
        ),
        layout=go.Layout(
            paper_bgcolor='dimgray',
            plot_bgcolor='dimgray',
            margin=go.layout.Margin(l=0, r=0, t=0, b=0),
            clickmode='event+select',
            font=dict(
                color="white"
            ),
            xaxis_title='Number of Listings',
        )
    )

    fig_hist = go.Figure(
        data=go.Histogram(
            x=df2['price'],
            histnorm="",
            xbins=dict(
                size=30,
                end=2000
            ),
            marker=dict(
                line=dict(
                    color="white",
                    width=0.25
                )
            )
        ),
        layout=go.Layout(
            margin=go.layout.Margin(l=0, r=0, t=0, b=0),
            clickmode='event+select',
            paper_bgcolor='dimgray',
            plot_bgcolor='dimgray',
            xaxis_title='Price ($)',
            yaxis_title='Absolute frequencies',
            showlegend=False,
            font=dict(
                color="white"
            )
        )
    )

    return (fig_map, fig_pie, fig_bar, fig_hist)


fig_map, fig_pie, fig_bar, fig_hist = plots_actualize(df)

# ------------------------------------------------------- APP ----------------------------------------------------------
app = dash.Dash(__name__)


# Deployment
server = app.server

# ------------------------------------------------------- HTML
# Layout of Dash App
app.layout = html.Div(
    style={'backgroundColor': colors['background']},
    id="div-universe",
    children=[
        html.Div(
            id="div-header",
            className="row",
            children=[
                html.Div(
                    id="div-header-1",
                    className="two columns div-user-controls",
                    children=[
                        html.H2("AIRBNB REVENUE ESTIMATE APP", id="title"),
                    ]
                ),
                html.Div(
                    id="div-header-2",
                    className="four columns div-user-controls",
                    children=[
                        html.P("""The following application describes the Airbnb listings of Austin.
                        This dashboard is fully interactive and can be used to choose the ideal place to stay in Austin.
                         """, style={"padding": "30px 0"}),
                        html.P(
                            """""",
                            style={"padding": "0 0 0 0", 'color': 'tab20'}
                        )
                    ]
                ),
                html.Div(
                    id="div-header-3",
                    className="three columns div-user-controls",
                    style = {'color': 'tab20'},
                    children=[
                        "Interact with the dashboard: ",
                        html.Div(
                            id="div-dropdown-1",
                            className="div-for-dropdown",
                            style = {'color': 'tab20'},
                            children=[
                                dcc.Dropdown(
                                    id='dcc_neighbourhood_dropdown',
                                    options=[{'label': i, 'value': i} for i in
                                             ["All"] + df["neighbourhood_group"].unique().tolist()],
                                    placeholder="Select Municipality",
                                    style={'max-width': '250px', 'color': 'tab20'}
                                )
                            ]
                        ),
                        html.Div(
                            id="div-dropdown-2",
                            className="div-for-dropdown",
                            children=[
                                dcc.Dropdown(
                                    id='dcc_variable_dropdown',
                                    options=[{'label': i, 'value': j} for i, j in zip(
                                        ["Availability", "Superhost"],
                                        ["available", "host_is_superhost"])],
                                    placeholder="Select Variable",
                                    #value ="host_is_superhost",
                                    style={'max-width': '250px', 'color': 'tab20'}
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    id="div-header-4",
                    className="three columns div-user-controls",
                    children=[
                        "Percentage of listings: ",
                        html.P(id="percentage-listings", style={"height": "50px", "font-size": 40}),
                        "Rank of location: ",
                        html.P(id="rank-location", style={"height": "50px", "font-size": 40}),
                    ]
                )
            ]
        ),
        html.Div(
            id="div-data",
            children=[
                html.Div(
                    # MAP
                    id="div-map-graph",
                    className="eight columns pretty_container",
                    children=[
                        html.H3("Airbnb listings in Austin"),
                        dcc.Graph(figure=fig_map, id="dcc_map_graph", config={'displayModeBar': False})
                    ],
                    style = {'backgroundColor': 'tab20'}
                ),
                html.Div(
                    id="div-side",
                    className="four columns pretty_container",
                    style = {'color': 'tab20'},
                    children=[
                        html.H3("About Airbnb in Austin"),
                        html.Div(
                            # GRAPHS
                            id="div-other-graphs",
                            className="scrollcol",
                            children=[
                                html.Div(
                                    id="div-graph-1",
                                    className="pretty_container_sub",
                                    children=[
                                        html.Div(
                                            className="row",
                                            children=[
                                                html.P('Proportion of Room Type',
                                                       className="eight columns plot_title"),
                                                html.Button(
                                                    id='button_pie',
                                                    children=["Reset"],
                                                    className="four columns"
                                                ),
                                            ]
                                        ),
                                        dcc.Graph(figure=fig_pie, id="dcc_pie_graph", style={"max-height": "350px"},
                                                  config={'displayModeBar': False}),
                                    ]
                                ),
                                html.Div(
                                    id="div-graph-2",
                                    className="pretty_container_sub",
                                    children=[
                                        html.Div(
                                            className="row",
                                            children=[
                                                html.P("Listing Rating Frequency",
                                                       className="eight columns plot_title"),
                                                html.Button(
                                                    id="button_bar",
                                                    children="Reset",
                                                    className="four columns"),
                                            ]
                                        ),
                                        dcc.Graph(
                                            figure=fig_bar,
                                            id="dcc_bar_graph",
                                            style={"max-height": "350px", "max-width": "300px", "margin-top": "40px"},
                                            config={'displayModeBar': False}
                                        ),
                                    ]
                                ),
                                html.Div(
                                    id="div-graph-3",
                                    className="pretty_container_sub",
                                    children=[
                                        html.Div(
                                            className="row",
                                            children=[
                                                html.P("Price Distribution",
                                                       className="eight columns plot_title"),
                                            ]
                                        ),
                                        html.Div(
                                            className="row",
                                            style={"margin-top": "20px"},
                                            children=[
                                                dcc.Input(
                                                    id='input-min-price',
                                                    className="four columns",
                                                    placeholder='Min price',
                                                    type='text'
                                                ),
                                                dcc.Input(
                                                    id='input-max-price',
                                                    className="four columns",
                                                    placeholder='Max price',
                                                    type='text'
                                                ),
                                                html.Button('Filter', id='button_price', className="four columns")
                                            ]
                                        ),
                                        dcc.Graph(
                                            figure=fig_hist,
                                            id="dcc_hist_graph",
                                            style={"max-height": "300px", "margin-top": "40px"},
                                            config={'displayModeBar': False}
                                        ),
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

# --------------------------------------------------- DATA

nobs = df.shape[0]

location_ranking = df[["review_scores_location", "neighbourhood_group"]] \
    .groupby("neighbourhood_group").mean(). \
    sort_values(by="review_scores_location", ascending=False).index.tolist()

rates = list(df.ordinal_rating.unique())
neig = list(df.neighbourhood_group.unique())
price = [df.price.min(), df.price.max()]
room = list(df.room_type.unique())

aux_selected_bar = None
aux_selected_pie = None
aux_pie_unique = room
aux_bar_unique = rates
bar_click = 0
pie_click = 0

aux_selected_bar_map = None
aux_selected_pie_map = None
aux_pie_unique_map = room
aux_bar_unique_map = rates
bar_click_map = 0
pie_click_map = 0

link_aux = None


def slice_df(neig=neig, rates=rates, price=price, room=room):
    aux = df.copy()
    # slice neighbourhood
    aux = aux.loc[aux['neighbourhood_group'].isin(neig)]
    # slice rating
    aux = aux.loc[aux['ordinal_rating'].isin(rates)]
    # slice room type
    aux = aux.loc[aux['room_type'].isin(room)]
    # slice price
    aux = aux.loc[(aux['price'] >= min(price)) & (aux['price'] <= max(price))]
    return aux


def open_link(id):
    link = df['listing_url'].iloc[id]
    webbrowser.open_new_tab(link)

list_of_neighbourhoods = pd.read_csv("./data/location_zooming.csv")
list_of_neighbourhoods = list_of_neighbourhoods.set_index('neighbourhood_group')
list_of_neighbourhoods = list_of_neighbourhoods.to_dict('index')
list_of_neighbourhoods["All"] = {"latitude": 30.26, "longitude": -97.7}

# colors for variables' legend
legend_dict = {"host_is_superhost": [[0, 1], ["Not Superhost", "Superhost"], ["rgb(203,23,29)", "rgb(0,109,44)"]],
               # "cancellation_policy": [["strict", "moderate", "flexible"], ["Strict", "Moderate", "Flexible"],
               #                         ["rgb(203,23,29)", "#fdca26", "rgb(0,109,44)"]],
               "available": [["Low", "Medium", "High"], ["Low", "Medium", "High"],
                             ["rgb(203,23,29)", "#fdca26", "rgb(0,109,44)"]]}

def graph_params(df, latInitial, lonInitial, zoomInitial, variable = None):
    def traces_legend(df, name, color):
        return go.Scattermapbox(
            name=name,
            ids=df["id"],
            lat=df["latitude"],
            lon=df["longitude"],
            mode="markers",
            marker=dict(
                color=color
            ),
            customdata=np.array([df.price.values, df.years_host.values, df.pref_amenities, df.estimated_annual_revenue.values]).T,
            hovertemplate='Estimated_annual_revenue: %{customdata[3]:$.2f} <br> Price: %{customdata[0]:$.2f} <br>'
                          'Years as a host: %{customdata[1]} <br> Amenities: %{customdata[2]} <br> '
        )
    if variable:
        slices = [df.loc[df[variable] == value] for value in legend_dict.get(variable)[0]]
        data = [traces_legend(s, n, c) for s, n, c in zip(slices, legend_dict.get(variable)[1],
                                                          legend_dict.get(variable)[2])]
        layout = go.Layout(
            autosize=True,
            margin=go.layout.Margin(l=0, r=35, t=0, b=0),
            showlegend=True,
            mapbox=dict(
                accesstoken=mapbox_access_token,
                center={'lat': latInitial, 'lon': lonInitial},
                zoom=zoomInitial,
                style="dark",
            ),
            legend=dict(
                bgcolor='grey',
                #bgcolor='#262626',
                font=dict(
                    color="white"
                )
            )
        )
    else:
        data = go.Scattermapbox(
            ids=df["id"],
            lat=df["latitude"],
            lon=df["longitude"],
            mode="markers",
            customdata=np.array([df.price.values, df.years_host.values, df.pref_amenities, df.estimated_annual_revenue.values]).T,
            hovertemplate='Estimated_annual_revenue: %{customdata[3]:$.2f} <br> Price: %{customdata[0]:$.2f} <br>' 
                          'Years as a host: %{customdata[1]} <br> Amenities: %{customdata[2]} <br>',
        )
        layout = go.Layout(
            autosize=True,
            margin=go.layout.Margin(l=0, r=35, t=0, b=0),
            showlegend=False,
            mapbox=dict(
                accesstoken=mapbox_access_token,
                center={'lat': latInitial, 'lon': lonInitial},
                zoom=zoomInitial,
                style="dark",
            )
        )
    return go.Figure(data=data, layout=layout)


# --------------------------------------------------- CALLBACKS

@app.callback(
    Output("dcc_map_graph", "figure"),
    [Input("dcc_neighbourhood_dropdown", "value"),
     Input("dcc_variable_dropdown", "value"),
     Input("dcc_pie_graph", "clickData"),
     Input("dcc_bar_graph", "selectedData"),
     Input("button_price", "n_clicks"),
     Input("button_pie", "n_clicks"),
     Input("button_bar", "n_clicks"),
     Input("dcc_map_graph", "clickData"),
     ],
    [State('input-min-price', 'value'),
     State('input-max-price', 'value')
     ]
)
def update_map(selectedlocation, selectedvariable, selected_pie, selected_bar, button_price, button_pie, button_bar,
               list_sel, min_price, max_price):
    global aux_selected_bar_map, aux_selected_pie_map, pie_click_map, bar_click_map, aux_pie_unique_map, aux_bar_unique_map, link_aux

    if list_sel and list_sel != link_aux:
        print(list_sel)
        # lat = int(list_sel['points'][0]['lat'])
        # lon = int(list_sel['points'][0]['lon'])
        # i = df.loc[(df['latitude'] == lat) & (df['longitude'] == lon)].index
        i = list_sel['points'][0]['pointIndex']
        open_link(i)
    link_aux = list_sel

    latInitial = 30.26
    lonInitial = -97.7
    zoomInitial = 8.5

    if selectedlocation:
        latInitial = list_of_neighbourhoods[selectedlocation]["latitude"]
        lonInitial = list_of_neighbourhoods[selectedlocation]["longitude"]
        if selectedlocation == 'All':
            zoomInitial = 8.5
        else:
            zoomInitial = 12
    list_params = [latInitial, lonInitial, zoomInitial]

    if selected_pie:
        selected_pie_unique = []
        selected_pie_unique.append(selected_pie['points'][0]['label'])
    else:
        selected_pie_unique = room

    if selected_bar:
        selected_bar_unique = list(np.intersect1d(rates, [b['y'] for b in selected_bar['points']]))
    else:
        selected_bar_unique = rates

    if min_price and max_price:
        selected_hist_unique = [int(min_price), int(max_price)]
    elif min_price:
        selected_hist_unique = [int(min_price), price[-1]]
    elif max_price:
        selected_hist_unique = [price[0], int(max_price)]
    else:
        selected_hist_unique = price

    if button_pie != pie_click_map:
        selected_pie_unique = room
    elif button_pie is not None and selected_pie == aux_selected_pie_map:
        selected_pie_unique = aux_pie_unique_map

    pie_click_map = button_pie
    aux_selected_pie_map = selected_pie
    aux_pie_unique_map = selected_pie_unique

    if button_bar != bar_click_map:
        selected_bar_unique = rates
    elif button_bar is not None and selected_bar == aux_selected_bar_map:
        selected_bar_unique = aux_bar_unique_map

    bar_click_map = button_bar
    aux_selected_bar_map = selected_bar
    aux_bar_unique_map = selected_bar_unique

    df_sliced_map = slice_df(neig, selected_bar_unique, selected_hist_unique, selected_pie_unique)

    # Dropdown for the variables
    if selectedvariable:
        return graph_params(df_sliced_map, list_params[0], list_params[1], list_params[2], selectedvariable)
    else:
        return graph_params(df_sliced_map, list_params[0], list_params[1], list_params[2])


@app.callback([
    Output('dcc_pie_graph', "figure"),
    Output('dcc_bar_graph', "figure"),
    Output('dcc_hist_graph', "figure"),
    Output("percentage-listings", "children"),
]
    , [Input("dcc_neighbourhood_dropdown", "value"),
       Input("dcc_pie_graph", "clickData"),
       Input("dcc_bar_graph", "selectedData"),
       Input("button_price", "n_clicks"),
       Input("button_pie", "n_clicks"),
       Input("button_bar", "n_clicks")],
    [State('input-min-price', 'value'),
     State('input-max-price', 'value')])

def update_graph(sel_neig, selected_pie, selected_bar, button_price, button_pie, button_bar, min_price, max_price):
    global aux_selected_bar, aux_selected_pie, pie_click, bar_click, aux_pie_unique, aux_bar_unique

    selected_neig = []
    selected_neig.append(sel_neig)

    if not sel_neig:
        selected_neig = neig
        list_percent_update = ""
    elif sel_neig == "All":
        selected_neig = neig
        list_percent_update = "100%"

    if selected_pie:
        selected_pie_unique = []
        selected_pie_unique.append(selected_pie['points'][0]['label'])

    else:
        selected_pie_unique = room

    if selected_bar:
        selected_bar_unique = list(np.intersect1d(rates, [b['y'] for b in selected_bar['points']]))
    else:
        selected_bar_unique = rates

    if min_price and max_price:
        selected_hist_unique = [int(min_price), int(max_price)]
    elif min_price:
        selected_hist_unique = [int(min_price), price[-1]]
    elif max_price:
        selected_hist_unique = [price[0], int(max_price)]
    else:
        selected_hist_unique = price

    # check if reset_pie was clicked
    if button_pie != pie_click:
        selected_pie_unique = room
    elif button_pie is not None and selected_pie == aux_selected_pie:
        selected_pie_unique = aux_pie_unique

    pie_click = button_pie
    aux_selected_pie = selected_pie
    aux_pie_unique = selected_pie_unique

    # check if reset_bar was clicked
    if button_bar != bar_click:
        selected_bar_unique = rates
    elif button_bar is not None and selected_bar == aux_selected_bar:
        selected_bar_unique = aux_bar_unique

    bar_click = button_bar
    aux_selected_bar = selected_bar
    aux_bar_unique = selected_bar_unique

    df_sliced = slice_df(selected_neig, selected_bar_unique, selected_hist_unique, selected_pie_unique)

    if sel_neig and sel_neig != 'All':
        list_percent_update = "{0:.1f}%".format((df_sliced.shape[0] / nobs) * 100)

    fig_map_update, fig_pie_update, fig_bar_update, fig_hist_update = plots_actualize(df_sliced)

    return fig_pie_update, fig_bar_update, fig_hist_update, list_percent_update


@app.callback(
    Output("rank-location", "children"),
    [
        Input("dcc_neighbourhood_dropdown", "value")
    ]
)
def update_rank_municip(neighbpicked):
    if (neighbpicked is None) | (neighbpicked == "All"):
        return ""
    else:
        return "#{}".format(
            location_ranking.index(neighbpicked) + 1
        )


if __name__ == '__main__':
    app.run_server(host = '127.0.0.1', dev_tools_hot_reload=True)
