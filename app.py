# %%
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# %%
file_path = 'C:/Users/DELL/Desktop/Jijaji Work/New Dataset Analysis/thorogood shoes data/thorogood_reviews_cleansed.csv'
data = pd.read_csv(file_path, encoding='ISO-8859-1')

# %%
# Convert timestamp from milliseconds to datetime and keep only the date part
data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms').dt.date

# %%
# Create a 'period' column for 6-month periods
data['period'] = pd.to_datetime(data['timestamp']).dt.to_period('6M')
data['period'] = data['period'].astype(str)

# %%
attributes = ['Comfort','Durability','Weight','Fit','Style','Value-For-Money','Available','Features.1','Arch-Support','Break-In','Traction','Looks','Performance','Breathability',
              'Price','Breaking-In','Fits','Waterproof','Durablity','Waterproofing','Water-Proof','Availability','Support','durability.1','style.1','looks.1','value-for-money.1',
              'Sizing','Size','Material','Water-Resistance','Arch-support.1','Height-Increase','Warmth','Warm','Summer-Hiking','Weatherproofing','Weather-Resistance','Ease-of-Use',
              'Fit Recommendation','Available Sizes','Height','Fit Comments','Brand','Quality','Customer Service','Waterproofness','Toe-Protection','Slip-On','Made in USA']

# %%
for attribute in attributes:
    if attribute in data.columns:
        data[attribute] = data[attribute].fillna('Blank')

# %%
# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1('Product Ratings Over Time'),
    dcc.Dropdown(
        id='title-dropdown',
        options=[{'label': title, 'value': title} for title in data['title_meta'].unique()],
        value=data['title_meta'].unique()[0]  # Default to the first title
    ),
    dcc.Dropdown(
        id='attribute-dropdown',
        options=[{'label': attr, 'value': attr} for attr in attributes],
        value='Comfort'  # Default attribute
    ),
    dcc.Graph(id='line-chart'),
    dcc.Graph(id='stacked-bar-chart'),
    dcc.Graph(id='histogram')
])

# Callback to update charts based on selected title and attribute
@app.callback(
    [Output('line-chart', 'figure'),
     Output('stacked-bar-chart', 'figure'),
     Output('histogram', 'figure')],
    [Input('title-dropdown', 'value'),
     Input('attribute-dropdown', 'value')]
)
def update_charts(selected_title, selected_attribute):
    print(f"Selected Title: {selected_title}")
    print(f"Selected Attribute: {selected_attribute}")

    if selected_attribute in data.columns:
        # Filter data based on the selected title
        filtered_data = data[data['title_meta'] == selected_title]
        print(f"Filtered Data for {selected_title}:")
        print(filtered_data.head())

        # Aggregate data
        agg_data = filtered_data.groupby(['period', selected_attribute]).size().reset_index(name='count')
        print(f"Aggregated Data for {selected_title} and {selected_attribute}:")
        print(agg_data.head())

        if not agg_data.empty:
            # Line chart
            line_fig = go.Figure()
            for attr_value in agg_data[selected_attribute].unique():
                trend_data = agg_data[agg_data[selected_attribute] == attr_value]
                line_fig.add_trace(go.Scatter(x=trend_data['period'], y=trend_data['count'], mode='lines+markers', name=f"Trend - {attr_value}"))

            line_fig.update_layout(
                title=f"Trend of {selected_attribute} Ratings for Product '{selected_title}' Over Time",
                xaxis_title='6-Month Period',
                yaxis_title='Count',
                legend_title=selected_attribute,
                xaxis_tickangle=-45
            )

            # Stacked bar chart
            bar_fig = px.bar(agg_data, x='period', y='count', color=selected_attribute, barmode='stack',
                             title=f"Stacked Bar Chart of {selected_attribute} Ratings for Product '{selected_title}' Over Time")
            bar_fig.update_xaxes(tickangle=-45)

            # Histogram
            hist_fig = px.histogram(agg_data, x='period', y='count', color=selected_attribute, barmode='stack',
                                    title=f"Histogram of {selected_attribute} Ratings for Product '{selected_title}' Over Time", nbins=30)
            hist_fig.update_xaxes(tickangle=-45)

            return line_fig, bar_fig, hist_fig

    return go.Figure(), go.Figure(), go.Figure()

# %%
# Run the app on a different port (e.g., 8050)
if __name__ == '__main__':
    app.run_server(port=8050)

# %%



