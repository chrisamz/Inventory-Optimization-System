from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Initialize the Dash app
app = Dash(__name__)
app.title = "Inventory Optimization System"

# Load prepared data (replace with actual data source)
def load_data():
    data = pd.read_csv('data/processed/forecasted_inventory.csv')
    data['Date'] = pd.to_datetime(data['Date'])
    return data

data = load_data()
items = data['Item ID'].unique()

# App layout
app.layout = html.Div([
    html.H1("Inventory Optimization Dashboard", style={'textAlign': 'center'}),

    # Filters
    html.Div([
        html.Label("Select Item:"),
        dcc.Dropdown(
            id="item-dropdown",
            options=[{"label": item, "value": item} for item in items],
            value=items[0],
            multi=False
        ),

        html.Label("Date Range:"),
        dcc.DatePickerRange(
            id="date-picker",
            start_date=data['Date'].min(),
            end_date=data['Date'].max(),
            display_format="YYYY-MM-DD"
        )
    ], style={'width': '25%', 'display': 'inline-block', 'padding': '10px'}),

    # Key Metrics
    html.Div(id="key-metrics", style={'display': 'flex', 'justifyContent': 'space-around', 'padding': '20px'}),

    # Visualizations
    html.Div([
        dcc.Graph(id="demand-trend-chart"),
        dcc.Graph(id="inventory-level-chart")
    ]),

    # Data Table
    html.Div([
        html.H3("Detailed Forecast Data"),
        dcc.Graph(id="forecast-table")
    ])
])

# Callbacks
@app.callback(
    [Output("key-metrics", "children"),
     Output("demand-trend-chart", "figure"),
     Output("inventory-level-chart", "figure"),
     Output("forecast-table", "figure")],
    [Input("item-dropdown", "value"),
     Input("date-picker", "start_date"),
     Input("date-picker", "end_date")]
)
def update_dashboard(selected_item, start_date, end_date):
    filtered_data = data[
        (data['Item ID'] == selected_item) &
        (data['Date'] >= start_date) &
        (data['Date'] <= end_date)
    ]

    # Key Metrics
    total_demand = filtered_data['Demand'].sum()
    avg_demand = filtered_data['Demand'].mean()
    reorder_point = filtered_data['Reorder Point'].iloc[-1]

    key_metrics = [
        html.Div([
            html.H4("Total Demand"),
            html.P(f"{total_demand:,.0f} units")
        ], style={"border": "1px solid #ccc", "padding": "10px", "width": "30%"}),
        html.Div([
            html.H4("Average Daily Demand"),
            html.P(f"{avg_demand:,.2f} units/day")
        ], style={"border": "1px solid #ccc", "padding": "10px", "width": "30%"}),
        html.Div([
            html.H4("Reorder Point"),
            html.P(f"{reorder_point:,.0f} units")
        ], style={"border": "1px solid #ccc", "padding": "10px", "width": "30%"})
    ]

    # Demand Trend Chart
    demand_trend_fig = px.line(
        filtered_data, x="Date", y="Demand", title="Demand Trends"
    )

    # Inventory Level Chart
    inventory_level_fig = px.line(
        filtered_data, x="Date", y="Inventory Level",
        title="Inventory Levels Over Time"
    )

    # Forecast Table
    forecast_table_fig = px.bar(
        filtered_data, x="Date", y="Forecast",
        hover_data={"Forecast": ":.2f"},
        title="Forecasted Demand"
    )

    return key_metrics, demand_trend_fig, inventory_level_fig, forecast_table_fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
