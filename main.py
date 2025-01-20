# main.py

# Install required libraries
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
import kagglehub

# Step 1: Download the Dataset
path = kagglehub.dataset_download("arpitsinghaiml/instagram-user-growth-by-country")
print("Path to dataset files:", path)

# Step 2: Load the Dataset
df_ig = pd.read_csv(path + "/instagram-users-by-country-2024.csv")

# Step 3: Data Preview
print(df_ig.head())

# Step 4: Calculate Growth Rate
df_ig['GrowthRate'] = (df_ig['InstagramUsers_2024'] - df_ig['InstagramUsers2023']) / df_ig['InstagramUsers2023']

# Step 5: Identify Top 10 Countries by Growth Rate
top_10 = df_ig.nlargest(10, 'GrowthRate')[['country', 'InstagramUsers_2024', 'GrowthRate']]
print(top_10)

# Step 6: Plot Top 10 Countries by Instagram Users (2024)
fig = px.bar(
    top_10,
    x='country',
    y='InstagramUsers_2024',
    text='InstagramUsers_2024',
    title='Top 10 Countries by Instagram User Growth (2024)',
    labels={'InstagramUsers_2024': 'Instagram Users (Millions)', 'country': 'Country'},
    color='InstagramUsers_2024',
    color_continuous_scale=px.colors.sequential.Blues
)

fig.update_layout(
    title_font_size=20,
    xaxis_title_font_size=16,
    yaxis_title_font_size=16,
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(255,255,255,1)'
)
fig.show()

# Step 7: Linear Regression for Prediction
# Prepare data
X = df_ig[['InstagramUsers_2024', 'InstagramUsers_PctFemale_2024', 'InstagramUsers_PctMale_2024', 'InstagramUsers2023']]
y = df_ig['InstagramUsers_2024']

# Handle missing values
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

# Create a Linear Regression model
model = LinearRegression()
model.fit(X_imputed, y)

# Predict for a new country
new_country = pd.DataFrame({
    'InstagramUsers_2024': [1000000],
    'InstagramUsers_PctFemale_2024': [30],
    'InstagramUsers_PctMale_2024': [70],
    'InstagramUsers2023': [800000]
})
prediction = model.predict(new_country)

print('Predicted number of Instagram users:', prediction)
