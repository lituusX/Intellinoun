import dash
from dash import dcc, html
import dash_table
import pandas as pd
import plotly.graph_objects as go
import dash_table.FormatTemplate as FormatTemplate
from dash_table.Format import Format, Scheme, Trim

df = pd.read_csv('./data/processed/datasets/votes_sentimentAVG.csv')

voter_ids = df['Voter ID'].unique()
proposal_ids = df['Proposal ID'].unique()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div('intellinoun', style={'textAlign': 'left', 'fontSize': 24, 'fontFamily': 'Arial', 'padding': '10px',
                                   'backgroundColor': '#f0f0f0'}),

    dcc.Tabs([
        dcc.Tab(label='Overview', children=[
            dash_table.DataTable(
                id='overview-table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                page_current=0,
                page_size=10,
                style_cell={'textAlign': 'left'}
            )
        ]),
        dcc.Tab(label='Voter Analysis', children=[
            dcc.Dropdown(
                id='voter-id-dropdown',
                options=[{'label': i, 'value': i} for i in voter_ids],
                value=voter_ids[0]
            ),
            html.Div(id='voter-output', style={'textAlign': 'left'}),
            dcc.Graph(id='voter-graph'),
            html.Button("Export data", id="export-button"),
            dcc.Download(id="download-data")
        ]),
        dcc.Tab(label='Proposal Analysis', children=[
            dcc.Dropdown(
                id='proposal-id-dropdown',
                options=[{'label': i, 'value': i} for i in proposal_ids],
                value=proposal_ids[0]
            ),
            dash_table.DataTable(
                id='proposal-table',
                columns=[{"name": i, "id": i} for i in df.columns],
                page_current=0,
                page_size=10,
                style_cell={'textAlign': 'left'}
            )
        ]),
    ])
])


@app.callback(
    [dash.dependencies.Output('voter-output', 'children'),
     dash.dependencies.Output('voter-graph', 'figure')],
    [dash.dependencies.Input('voter-id-dropdown', 'value')]
)
def update_voter_analysis(selected_voter_id):
    global voter_df
    voter_df = df[df['Voter ID'] == selected_voter_id]
    table = dash_table.DataTable(
        id='voter-table',
        columns=[{"name": i, "id": i} for i in voter_df.columns],
        data=voter_df.to_dict('records'),
        page_current=0,
        page_size=10,
        style_cell={'textAlign': 'left'}
    )

    fig = go.Figure()
    fig.add_trace(go.Histogram(x=voter_df['Score Avg'], nbinsx=20))

    return table, fig


@app.callback(
    dash.dependencies.Output("download-data", "data"),
    [dash.dependencies.Input("export-button", "n_clicks")],
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(voter_df.to_csv, "voter_data.csv")


@app.callback(
    dash.dependencies.Output('proposal-table', 'data'),
    [dash.dependencies.Input('proposal-id-dropdown', 'value')]
)
def update_proposal_table(selected_proposal_id):
    filtered_df = df[df['Proposal ID'] == selected_proposal_id]
    return filtered_df.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)
