import streamlit as st
import pandas as pd
import plotly.express as px

st.title("EEG Emotion Dashboard")
st.write("Ye dashboard EEG Brainwave data se Emotion ko samajhta hai. Isme 3 Emotions hain: POSITIVE, NEGATIVE aur NEUTRAL.")

data = pd.read_csv("emotions.csv")

# Pehla numeric column khud dhoondo
numeric_cols = data.select_dtypes(include='number').columns.tolist()
col_a = numeric_cols[0]
col_b = numeric_cols[1]
col_c = numeric_cols[2]
col_d = numeric_cols[3]
col_e = numeric_cols[4]

# Sidebar - 2 Filters
st.sidebar.header("Filters")
emotion_filter = st.sidebar.multiselect("Emotion Select Karo:", data['label'].unique(), default=data['label'].unique())
min_val, max_val = st.sidebar.slider(f"{col_a} ki Range:", float(data[col_a].min()), float(data[col_a].max()), (float(data[col_a].min()), float(data[col_a].max())))

# Filtered Data
filtered = data[(data['label'].isin(emotion_filter)) & (data[col_a] >= min_val) & (data[col_a] <= max_val)]

# 4 Key Numbers at Top
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Rows", len(filtered))
c2.metric("Total Columns", len(data.columns))
c3.metric("POSITIVE", len(filtered[filtered['label'] == 'POSITIVE']))
c4.metric("NEGATIVE", len(filtered[filtered['label'] == 'NEGATIVE']))

# Graph 1
st.subheader("1. Emotion Count (Bar Graph)")
st.bar_chart(filtered['label'].value_counts())

# Graph 2
st.subheader(f"2. {col_a} ka Distribution (Histogram)")
fig2 = px.histogram(filtered, x=col_a, color='label', title=f"{col_a} Distribution")
st.plotly_chart(fig2)

# Graph 3
st.subheader(f"3. {col_a} vs {col_b} (Scatter - Bivariate)")
fig3 = px.scatter(filtered, x=col_a, y=col_b, color='label', title="Brainwave Comparison")
st.plotly_chart(fig3)

# Graph 4
st.subheader(f"4. Har Emotion me {col_a} (Box Plot - Comparison)")
fig4 = px.box(filtered, x='label', y=col_a, color='label', title="Emotion Wise Comparison")
st.plotly_chart(fig4)

# Graph 5
st.subheader("5. Average Brainwave Comparison")
avg_data = filtered.groupby('label')[[col_a, col_b, col_c, col_d, col_e]].mean().T
st.line_chart(avg_data)

# Checkbox Raw Data
if st.checkbox("Raw Data Dikhao"):
    st.dataframe(filtered.head(20))

# Findings
st.subheader("Findings")
st.write("1. Data me 3 Emotions taqreeban barabar hain.")
st.write("2. POSITIVE aur NEUTRAL ka brainwave pattern milta julta hai.")
st.write("3. NEGATIVE Emotion me brainwave ki value thori alag hoti hai.")
st.write("4. Dashboard se hum Emotion ko filter karke aasani se dekh sakte hain.")