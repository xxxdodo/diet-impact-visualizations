import pandas as pd
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler

# 读取数据
df = pd.read_csv("Results_21Mar2022.csv")


env_columns = [
    'mean_ghgs', 'mean_land', 'mean_watscar',
    'mean_eut', 'mean_bio', 'mean_watuse', 'mean_acid'
]

label_map = {
    'mean_ghgs': 'GHG Emissions',
    'mean_land': 'Land Use',
    'mean_watscar': 'Water Scarcity',
    'mean_eut': 'Eutrophication',
    'mean_bio': 'Biodiversity Impact',
    'mean_watuse': 'Water Use',
    'mean_acid': 'Acidification'
}

df_grouped = df.groupby('diet_group')[env_columns].mean().reset_index()
scaler = MinMaxScaler()
df_scaled = df_grouped.copy()
df_scaled[env_columns] = scaler.fit_transform(df_grouped[env_columns])

diet_code_map = {name: i for i, name in enumerate(df_scaled['diet_group'])}
df_scaled['diet_code'] = df_scaled['diet_group'].map(diet_code_map)


dimensions = [
    dict(label=label_map[col], values=df_scaled[col])
    for col in env_columns
]


fig = go.Figure(data=go.Parcoords(
    line=dict(
        color=df_scaled['diet_code'],
        colorscale='Turbo',
        showscale=True,
        cmin=0,
        cmax=len(diet_code_map) - 1
    ),
    dimensions=dimensions
))

fig.update_layout(
    title="Environmental Impacts by Diet Group",
    height=600
)

fig.write_html("parallel_coordinates_correct_final.html")
