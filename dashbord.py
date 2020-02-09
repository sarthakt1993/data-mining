import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import dash_table
import pandas as pd

df = pd.read_pickle('data/dataframe_apriori.pickle')
df_main=df.astype(str)
df_main.antecedents=df_main.antecedents.apply(lambda x: x[11:-2])
df_main.consequents=df_main.consequents.apply(lambda y: y[11:-2])
df_main.support=df_main.support.apply(lambda a: round(float(a),5))
df_main.confidence=df_main.confidence.apply(lambda b: round(float(b),5))
df_main.lift=df_main.lift.apply(lambda c: round(float(c),5))
df_main.columns=['Antecedents','Consequents','Support','Confidence','Lift']

df=pd.read_pickle('data/dataframe.pickle')
df = pd.DataFrame({col:str(col)+'=' for col in df}, index=df.index)+df.astype(str)
melted_data = pd.melt(df)
frequency = melted_data.groupby(by=['value'])['value'].count().sort_values(ascending=False)
freq_itemset = pd.DataFrame({'Item':frequency.index, 'Frequency':frequency.values})

fig = px.scatter(df_main, x="Support", y="Confidence", color="Consequents",
                 size='Lift', hover_data=['Antecedents'])

fig2 = px.bar(freq_itemset.head(10), x='Item', y='Frequency',text='Frequency')

app = dash.Dash(__name__)

app.layout = html.Div([
             html.Header([
                 html.H2("Data Mining Dashboard"),
                 html.Img(src="/assets/syrlogo2.jpg")], className="banner"),
            html.Div([
                    html.H3("Attrition Tables"),
                    html.Div([
                            html.H6("Attrition=No"),
                            dash_table.DataTable(
                                    id='Attrition Table No',
                    columns=[{'name': i, 'id': i, 'deletable': False} for i in sorted(df_main.columns)],
                    data=df_main[df_main.Consequents=='\'Attrition=No\''].to_dict('records'),
                    page_current= 0,
                    page_size= 5,
                    page_action='native',
                    filter_action='native',
                    filter_query='',

                    sort_action='native',
                    sort_mode='multi',
                    sort_by=[],
                    style_data_conditional=[
                            {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': 'rgb(248, 248, 248)'
                                    }],
                    style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold',
                            'fontSize':'15px'
                            })],style={"width":"90%","margin-left":"auto","margin-right":"auto"}, className="attritiontablesno"),
        
        html.Div([
                html.H6("Attrition=Yes"),
                dash_table.DataTable(
                    id='Attrition Table Yes',
                    columns=[{'name': i, 'id': i, 'deletable': False} for i in sorted(df_main.columns)],
                    data=df_main[df_main.Consequents=='\'Attrition=Yes\''].to_dict('records'),
                    page_current= 0,
                    page_size= 5,
                    page_action='native',
                    filter_action='native',
                    filter_query='',
                    
                    sort_action='native',
                    sort_mode='multi',
                    sort_by=[],
                    style_data_conditional=[
                            {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': 'rgb(248, 248, 248)'
                                    }],
                    style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold',
                            'fontSize':'15px'
                            }
                    )],style={"width":"90%","margin-left":"auto","margin-right":"auto"}, className="attritiontablesyes")], className="attritiontables"),

        html.Div([
                html.H3("Visualizations")
                ]),
        html.Div([
                 html.Div([
                         html.H6("Support vs Confidence"),
                         dcc.Graph( id='scatter',figure=fig)],className="six columns"),
                
                html.Div([
                        html.H6("Most Frequent Items"),
                dcc.Graph( id='bar plot',figure=fig2)],className="six columns"),],className='rows'),
                
        html.Div([
        html.Footer(children=[
             html.P("© 2020 Sarthak Tandon")])],className='footr')

],className="body")

app.css.append_css({
    "external_url":"/assets/mycss2.css"
})
 

if __name__ == '__main__':
    app.run_server(debug=False)