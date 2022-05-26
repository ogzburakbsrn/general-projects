from asammdf import MDF
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import sys
import os

try:
    if sys.frozen or sys.importers:
        script_directory = os.path.dirname(sys.executable)
except AttributeError:
    script_directory = os.path.dirname(os.path.realpath(__file__))

supported_file_types = "mf4, dat"
files_in_folder = []
signals_in_file = []

for file in os.listdir():
    if file.split(".")[1] in supported_file_types:
        files_in_folder.append(file)

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Concerto"),
    dcc.Graph(id='graph_1'),

    html.Div(
        [dcc.Dropdown(files_in_folder, id='file-names', style={'width': '50%'}),
         dcc.Dropdown(id='signal-names', style={'width': '50%'})
         ],
        style={'width': '50%', 'align-items': 'center', 'justify-content': 'center', 'padding': 10}),
])


@app.callback(
    Output('signal-names', 'options'),
    Output('graph_1', 'figure'),
    Input('file-names', 'value'),
    Input('signal-names', 'value'),
    prevent_initial_call=True)
def choose_file(selected_file, selected_signal):  # TODO: dcc.Store to store df to browser memory, button to clear.
    mdf_obj = MDF(selected_file)
    df = mdf_obj.to_dataframe(ignore_value2text_conversions=True, reduce_memory_usage=True, raster=0.1)
    df.rename(columns=(lambda x: x.split('\\', maxsplit=1)[0]), inplace=True)
    df = df.reindex(sorted(df.columns, key=lambda v: v.upper()), axis=1)
    if selected_signal:
        df['Time [s]'] = df.index
        fig = px.line(df, x='Time [s]', y=selected_signal, width=1000, height=600)
        fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
        fig.update_yaxes(title=selected_signal,
                         type='linear')
        fig.update_xaxes(title='Time [s]')
        fig.update_layout(hovermode='x unified')
        return df.columns.unique(), fig
    return df.columns.unique(), {}


if __name__ == '__main__':
    app.run_server(debug=True)
