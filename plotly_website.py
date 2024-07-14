import pandas as pd
import matplotlib.pyplot as plt
from google.oauth2 import service_account
from googleapiclient.discovery import build
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd

spreadsheet_id = "1fMlqflPJTg9oTuKthrAtgJdKLM124wMcgStw9fwLJ9Q"
# For example:
# spreadsheet_id = "8VaaiCuZ2q09IVndzU54s1RtxQreAxgFNaUPf9su5hK0"

credentials = service_account.Credentials.from_service_account_file(
    "/Users/Shared/cronscripts/musliwebsite/key_private.json",
    scopes=["https://www.googleapis.com/auth/spreadsheets"],
)
service = build("sheets", "v4", credentials=credentials)


request = service.spreadsheets().get(
    spreadsheetId=spreadsheet_id, ranges=[], includeGridData=True
)

# Assuming you want data from the first sheet and the entire range of data present
sheet_props = request.execute()
sheet = sheet_props.get("sheets", [])[0]  # Get the first sheet in the spreadsheet
title = sheet.get("properties", {}).get("title")  # Get the title of the sheet
range_name = f"{title}"  # Assuming you want the whole sheet

# Modify this line if you know the specific range you're interested in, e.g., 'Sheet1!A1:D5'
result = (
    service.spreadsheets()
    .values()
    .get(spreadsheetId=spreadsheet_id, range=range_name)
    .execute()
)

# Get values and convert to DataFrame
values = result.get("values", [])
if not values:
    print("No data found.")
else:
    # Assuming the first row of your data contains the column headers
    df = pd.DataFrame(values[1:], columns=values[0])

df["Gewicht"] = df["Gewicht"].apply(lambda x: float(x.replace("g", "")))
# Ensure the 'Datum' column is in datetime format
df["Datum"] = pd.to_datetime(df["Datum"], format="%d.%m.%Y")

# Calculate total weight
total_weight = df["Gewicht"].sum()


# get current day of the year
import datetime

today = datetime.datetime.now()
day_of_year = today.timetuple().tm_yday
day_of_year


# Assuming 'df' is your DataFrame after processing

# Calculate total weight
total_weight = df["Gewicht"].sum()

# get current day of the year


# Sum the weight for each Müsli type
weights = df.groupby("Müsli")["Gewicht"].sum().reset_index()

# Create a pie chart with Plotly
fig_pie = px.pie(
    weights,
    names="Müsli",
    values="Gewicht",
    title="",
    color_discrete_sequence=px.colors.sequential.RdBu,
)
fig_pie.update_traces(textinfo="percent+label")
fig_pie.update_layout(legend_title_text="Müsli Type")


# Create a cumulative weight column
df_sorted = df.sort_values("Datum")
df_sorted["Cumulative Weight"] = df_sorted["Gewicht"].cumsum()

# Plot cumulative weight over time with Plotly
fig_line = px.line(df_sorted, x="Datum", y="Cumulative Weight", title="", markers=True)
fig_line.update_traces(line_color="RoyalBlue")
fig_line.update_layout(
    xaxis_title="Date", yaxis_title="Gesamtgewicht (g)", xaxis=dict(tickangle=45)
)


# Sample data and Plotly figures setup (Replace with your actual data and figures)
# Assuming 'df' is your DataFrame after processing
# Example: df = pd.DataFrame({'Müsli': ['Type A', 'Type B'], 'Gewicht': [100, 200], 'Datum': ['2021-01-01', '2021-01-02']})

# Calculate total weight
total_weight = df["Gewicht"].sum()

total_weight_kg = np.round(total_weight / 1000, 2)

import datetime

today = datetime.datetime.now()
day_of_year = today.timetuple().tm_yday
total_prognose = total_weight / day_of_year * 366
total_prognose_kg = np.round(total_prognose / 1000, 2)

# Generate Plotly charts (fig_pie and fig_line) here, as previously described

# Convert Plotly figures to HTML strings without full HTML document structure
pie_chart_html = fig_pie.to_html(
    full_html=False,
    include_plotlyjs="cdn",
    # config={"responsive": True},  # Make the chart responsive
)

line_chart_html = fig_line.to_html(
    full_html=False,
    include_plotlyjs="cdn",
    # config={"responsive": True},  # Make the chart responsive
)

# Adjusted HTML template with double braces for CSS and JavaScript sections
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Müsli Analysis</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .info-container {{
            display: flex;
            flex-wrap: wrap; /* Allow items to wrap on small screens */
            justify-content: center; /* Center items on small screens */
            align-items: center;
            width: 100%;
            margin: 20px 0;
        }}
        .total-weight {{
            margin: 10px; /* Adjust for spacing on all sides */
            padding: 10px 20px;
            border: 2px solid #007BFF;
            border-radius: 8px;
            font-size: 24px;
            color: #007BFF;
            background-color: #f0f0f0;
            flex: 1; /* Allow flex items to grow to fill available space */
            max-width: 300px; /* Max width to prevent overly large blocks on wide screens */
        }}
        .chart-container {{
            width: 100%;
            display: flex;
            flex-direction: column; /* Stack charts vertically */
            align-items: center;
            margin-top: 20px;
        }}
        .chart {{
            width: 90%; /* Use a percentage of the viewport width */
            max-width: 600px; /* Max width to prevent overly wide charts */
            margin: 10px 0; /* Add vertical margin */
            padding: 10px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
    </style>
</head>
<body>
    <div class="info-container">
        <div class="total-weight">Bisher verspeistes Müsli: <strong>{total_weight} kg</strong></div>
        <div class="total-weight">Aktuelle Jahresprognose: <strong>{total_prognose} kg</strong></div>
    </div>
    
    <div class="chart-container">
        <div class="chart" id="pie-chart">{pie_chart_html}</div>
        <div class="chart" id="line-chart">{line_chart_html}</div>
    </div>

    <script>
        // Insert JavaScript here if needed
    </script>
</body>
</html>


"""

# Insert the Plotly charts HTML and total weight into the template
final_html = html_template.format(
    pie_chart_html=pie_chart_html,
    line_chart_html=line_chart_html,
    total_weight=total_weight_kg,
    total_prognose=total_prognose_kg,
)

# Write the combined HTML to a file
with open(
    "/Users/Shared/cronscripts/musliwebsite/index.html", "w"
) as f:
    f.write(final_html)
