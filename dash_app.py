# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 12:43:22 2019

@author: paula.romero.lopes
"""
import dash_table
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import itertools
from six.moves.urllib.parse import quote

mapbox_access_token = 'pk.eyJ1IjoicHJvbWVybzA5MDkiLCJhIjoiY2pwZnlnOTlqMGQwNjNrcDg4aml2aGxvYyJ9.DBnp1meLcFgRwoDkJ-LsCg'

app = dash.Dash(name=__name__)
#app.config['suppress_callback_exceptions']=True
df = pd.read_csv('dentistas_2019_bairros.csv', sep=';', encoding='latin-1', names=['NAME','ESPECIALIDADE','ENDERECO','TIPO_CONSULTA','CONVENIOS','LAT','LONG','LINK'])
df['ESPECIALIDADE'] = df['ESPECIALIDADE'].fillna('Sem epecialidade')
specialities = []
for s in df['ESPECIALIDADE'].tolist():
    specialities.append(s.split(','))
flattened_list  = list(itertools.chain(*specialities))
list_temp = [x.strip() for x in flattened_list]
specialities = set(list_temp)
specialities.add('All')

df_s = pd.DataFrame()
for s in specialities:
    df_s1 = df[df['ESPECIALIDADE'].str.contains(s)]
    df_s1['spec'] = s
    df_s = df_s.append(df_s1)

def filter_data(value):
    selected_rows=[rows[i] for i in selected_row_indices]
    #or
    selected_rows=pd.DataFrame(rows).iloc[i] 


app.layout = html.Div([ 
                    html.H1('Dentistas no Rio de Janeiro cadastrados no site doctoalia.com',
                            style=	{'border':'1px solid',
                                    'border-color':'rgba(0,0,0,0.1)',
                                    'border-bottom-color':'rgba(0,0,0,0.2)',
                                    'border-top':'none',
                                    'background':'#f7f7f7',
                                    'background':'-webkit-linear-gradient(top, #f7f7f7, #f4f4f4)',
                                    'background':'-moz-linear-gradient(top, #f7f7f7, #f4f4f4)',
                                    'background':'-o-linear-gradient(top, #f7f7f7, #f4f4f4)',
                                    'background':'linear-gradient(to bottom, #f7f7f7, #f4f4f4)',
                                    'background':'-clip:padding-box',
                                    'border-radius':'0 0 5px 5px',
                                    'margin': 'auto',
                                    'position': 'relative',
                                    'width': '1000px'}),
                    html.Div([

                            html.Div(
                                        dcc.Graph(
                                            id='map-graph',
                                            animate=True),
                                            style={
                                                    'width': '49%',
                                                    'height': '45%',
                                                    'display':'inline-block'},
                                            className='map'),
                            html.Div(
                                    dcc.Graph(
                                            id='espec_graph'),
                                            style={
                                                    'width':'49%',
                                                    'height':'45%',
                                                    'display': 'inline-block'})])
                                    ,
                            html.Div([
                                     html.H3('Escolha uma especialidade para filtar a tabela e o mapa',
                                            style=	{'font-size': '24px',
                                    	             'line-height': '35px',
                                     	              'font-weight': 'normal',
                                    	              'font-family': 'sans-serif',
                                    	              'position': 'left',
                                    	              'color': '#0000ff',
                                                      'width':'40%',
                                                      "marginBottom": "2",
                                                      "marginTop": "4",                                                     
                                                      'display':'inline-block'}),
                                    html.Div(
                                            dcc.Dropdown(
                                            id="speciality_drop",
                                            options=[{'label':d,
                                                      'value':d} for d in specialities],
                                            multi=True,
                                            placeholder = 'Select Speciality...',
                                            value=''),
                                            
                                            style={    "width": "40%",
                                                        "textAlign": "center",
                                                        "marginBottom": "2",
                                                        "marginTop": "1",
                                                        'display':'inline-block'
                                                    },
                                    className='Drop'),
                                        html.A(
                                                'Download Data',
                                                id='download-link',
                                                download="rawdata.csv",
                                                href="",
                                                target="_blank",
                                                style = {'width':'15%',
                                                     'display':'inline-block',
                                                     'background-color': '#4CAF50', 
                                                      'border': 'none',
                                                      'color': 'white',
                                                      'padding': '5px',
                                                     ' text-align': 'center',
                                                     ' text-decoration': 'none',
                                                      'font-size': '20px',
                                                      'margin': '1px 1px',
                                                      'cursor': 'pointer',
                                                      'border-radius': '3%'})
                                                ]),
                    html.Div(id='none',children=[],style={'display': 'none'}),
                    html.Div([

                            html.Div(
                                    dash_table.DataTable(
                                            id='table',
                                            data=df.to_dict('rows'),
                                            columns=[{'id': c, 'name': c} for c in df.columns],
                                            filtering=True,
                                            sorting=True,
                                            sorting_type="multi",
                                            row_selectable="multi",
                                            row_deletable=False,
                                            selected_rows=[],
                                            style_as_list_view=True,
                                            style_table={'overflowX': 'scroll',
                                                         'maxHeight': '600px',
                                                         'overflowY': 'scroll',
                                                         'border': 'thin lightgrey solid'},
                                            style_header={
                                                'backgroundColor': 'white',
                                                'fontWeight': 'bold'
                                            },    
                                            style_cell={
                                                'minWidth': '0px', 'maxWidth': '180px',
                                                'whiteSpace': 'normal'
                                                },
                                            css=[{
                                                'selector': '.dash-cell div.dash-cell-value',
                                                'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                                            }],
                                                    
                                    ))
                                ])
                            ],
            style = {'background-color': 'white'})
                                            
@app.callback(
    Output('map-graph', 'figure'),
    [Input('speciality_drop', 'value')])
def update_map(selector):
    """
    Map graph callback
    """
    #room_selector.append(None)

    if isinstance(selector,list):
        pattern = '|'.join(selector)
        _df = df[df["ESPECIALIDADE"].str.contains(pattern)]
    else:
        _df = df[df["ESPECIALIDADE"].str.contains(selector)]

    # Paint mapbox into the data
    data = go.Data([
        go.Scattermapbox(
            lat=_df['LAT'],
            lon=_df['LONG'],
            mode='markers',
            hoverinfo= "text",
            text= [["Name: {} <br>Perfil: {}".format(i,j)]
                            for i,j in zip(df['NAME'], df['LINK'])],
            hoverlabel={
                'bordercolor': 'azure',
                'font': {
                    'color': '#FFF'
                }
               }
              )
             ]
            )

    # Layout and mapbox properties
    layout = go.Layout(
        autosize=True,
        hovermode='closest',
        hoverlabel=dict(bgcolor='rgba(188, 20, 26, 0.5)'),
        clickmode= 'event+select',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            pitch=0,
            zoom=12,

          #  style='mapbox://styles/promero0909/cjponsk183w7d2sry4cjlxqmj',
            center=dict(lat= -22.970722,
                        lon=-43.182365)
        ),
        margin = dict(l = 0, r = 0, t = 0, b = 0),
        paper_bgcolor='#191a1a',
        plot_bgcolor='#191a1a',
    )

    return go.Figure(
        data=data,
        layout=layout
    )
# @app.callback(Output('table', 'data'),
#               [Input('map-graph', 'clickData')])
# def highlight_rows(map_selector):
#     if map_selector is None:
#         s = 'nao e posi'
#         _df = df
#     else:
#         s = map_selector['points'][0]['text'].split('Perfil: ')[-1].split("'")[0]
#         _df = df[df['LINK']==s]    
    
#     # style_data_conditional=[{
#     #     "if": 'LINK eq %s' %s,
#     #     "backgroundColor": "#3D9970",
#     #     'color': 'white'
#     # }]
#     return _df.to_dict('records')
@app.callback(Output('table', 'data'), [Input('speciality_drop', 'value'),
              Input('map-graph', 'clickData')])
def update_rows(selector, map_selector):
    print(map_selector)
    old_ms = None
    
    if selector == 'All':
        _df=df
    if isinstance(selector,list):
        pattern = '|'.join(selector)
        _df = df[df["ESPECIALIDADE"].str.contains(pattern)]
    else:
        _df = df[df["ESPECIALIDADE"].str.contains(selector)]
    if map_selector is None or old_ms==map_selector:
        s = 'nao e posi'
        _dff = _df
    else:
        s = map_selector['points'][0]['text'].split('Perfil: ')[-1].split("'")[0]
        _dff = _df[_df['LINK']==s]    
        old_ms = map_selector
    return _df.to_dict('records')

@app.callback(Output('espec_graph','figure'),
              [Input('none', 'children')])
def spec_graph(sel):
    
    _df = df_s['spec'].value_counts()
    _df.drop('Sem epecialidade', inplace=True)
    data = [go.Bar(
            x=_df.index,
            y=_df
    )]    
    layout = go.Layout(
              title = '<b>Distriuição de Especialidades</b>',
              xaxis = dict(title = 'Especialidade'),
              yaxis = dict(title = 'Count'))
    
    return go.Figure(data=data,
                     layout=layout)

@app.callback(
    dash.dependencies.Output('download-link', 'href'),
   [ dash.dependencies.Input('table', 'data'),
      dash.dependencies.Input('table', 'selected_rows')])
def update_download_link(rows,selected_row_indices):

    selected_rows=[rows[i] for i in selected_row_indices]
    # selected_rows=pd.DataFrame(rows).iloc[i] 
    if selected_rows == []:
        csv_string = df.to_csv(index=False, encoding='utf-8')
    else:
        selected_rows = pd.DataFrame.from_dict(selected_rows)
        csv_string = selected_rows.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8,%EF%BB%BF" + quote(csv_string)
    return csv_string

if __name__ == '__main__':
    app.run_server(debug=True)