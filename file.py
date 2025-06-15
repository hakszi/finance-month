import pandas as pd
import numpy as np
import squarify
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('data.csv', sep=',', header='infer')
df['Date'] = pd.to_datetime(df['Date'])
df.sort_values('Date', inplace=True)
print(df['Date'].dt.day)


# byDays = df.groupby(['Date', 'Category'], as_index=False)['Value'].sum()
df['Month'] = df['Date'].dt.to_period('M')
monthly = df.groupby('Month', as_index=False)['Value'].sum()
monthly_categories = df.groupby(['Month', 'Category'], as_index=False)['Value'].sum()

m = sorted(set(monthly_categories['Month']))[-1]

filtered = monthly_categories[monthly_categories['Month'] == '2025-05']

colors=['#fae588','#f79d65','#f9dc5c','#e8ac65','#e76f51','#ef233c','#b7094c'] #color palette

sns.set_style(style="whitegrid") # set seaborn plot style
sizes= filtered["Value"].values# proportions of the categories
label=filtered["Category"]
squarify.plot(sizes=sizes, label=label, alpha=0.6,color=colors).set(title=f'{m}')
plt.axis('off')
plt.show()

