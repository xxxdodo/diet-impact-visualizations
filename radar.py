import pandas as pd
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler

# 加载数据（请确保路径正确）
df = pd.read_csv("Results_21Mar2022.csv")

# 环境维度变量
env_columns = [
    'mean_ghgs', 'mean_land', 'mean_watscar',
    'mean_eut', 'mean_bio', 'mean_watuse', 'mean_acid'
]

# 环境变量的可读名称（用于图中显示）
label_map = {
    'mean_ghgs': 'GHG Emissions',
    'mean_land': 'Land Use',
    'mean_watscar': 'Water Scarcity',
    'mean_eut': 'Eutrophication',
    'mean_bio': 'Biodiversity Impact',
    'mean_watuse': 'Water Use',
    'mean_acid': 'Acidification'
}

# 按饮食组分组，取每组平均
df_grouped = df.groupby('diet_group')[env_columns].mean().reset_index()

# 对每个指标进行标准化（0~1），便于在雷达图中比较
scaler = MinMaxScaler()
df_scaled = df_grouped.copy()
df_scaled[env_columns] = scaler.fit_transform(df_grouped[env_columns])

# 提取变量标签
categories = [label_map[col] for col in env_columns]
categories += [categories[0]]  # 闭合多边形

# 创建雷达图对象
fig = go.Figure()

for _, row in df_scaled.iterrows():
    r_values = row[env_columns].tolist()
    r_values += [r_values[0]]  # 闭合多边形图形

    fig.add_trace(go.Scatterpolar(
        r=r_values,
        theta=categories,
        fill='toself',
        name=row['diet_group']
    ))

# 布局设置
fig.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 1])
    ),
    title="Radar Chart: Environmental Impact of All Diet Groups",
    showlegend=True,
    height=700,
    width=800
)

# 导出为 HTML 文件（可选）
fig.write_html("radar_chart_all_dietgroups.html")
