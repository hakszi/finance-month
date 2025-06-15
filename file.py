import pandas as pd
import numpy as np
import squarify
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    df = pd.read_csv('data.csv', sep=',', header='infer')
    df['Date'] = pd.to_datetime(df['Date'])

    df['Month'] = df['Date'].dt.to_period('M')
    monthly_categories = df.groupby(['Month', 'Category'], as_index=False)['Value'].sum()
    monthly_categories = monthly_categories.rename(columns={'Month': 'Date'})
    monthly_categories['Date'] = monthly_categories['Date'].dt.to_timestamp(how='start')

    y = year_df(monthly_categories, 2024)

    fig, axes = plt.subplots(nrows=4,
                             ncols=3,
                             figsize=(15, 15),
                             dpi=100)

    visualize(y, fig, axes)


def year_df(df, year):
    return df[pd.to_datetime(df['Date']).dt.year == year]


def month_df(df, year, month):
    return df[(pd.to_datetime(df['Date']).dt.year == year)
              & (pd.to_datetime(df['Date']).dt.month == month)]


def split_year(y):
    all_months = range(1, 13)  # All months from January to December
    m = []
    years = sorted(set(y['Date'].dt.year))  # Get all unique years in the data

    for year in years:
        for month in all_months:
            m_tmp = month_df(y, year, month)
            if m_tmp.empty:
                # Create a DataFrame with "N/A" for months with no data
                month_year = pd.to_datetime(f'{year}-{month:02d}-01')  # Create a date for the first of the month
                m_tmp = pd.DataFrame({'Category': ['N/A'], 'Value': [0], 'Date': [month_year]})
            m.append(m_tmp)
    return m




def visualize(df, fig, axes):
    y_split = split_year(df)

    fig.subplots_adjust(top=0.95)

    plt.rcParams.update({
        'font.family': 'DejaVu Sans',
        'text.antialiased': True,
        'font.weight': 'normal'
    })

    i = 0
    for ax in axes.flat:
        if i < len(y_split):
            sizes = y_split[i]["Value"].values
            label = y_split[i]["Category"]
            month_year = y_split[i]["Date"].dt.strftime('%B %Y').iloc[0]  # Get month and year

            if label.iloc[0] == 'N/A':  # Check if the month has no data
                ax.text(0.5, 0.5, f'N/A\n{month_year}', fontsize=20, ha='center', va='center')
            else:
                sns.set_style(style="whitegrid")
                squarify.plot(sizes=sizes, label=label, alpha=0.6, ax=ax,edgecolor='white', linewidth=1)
                ax.set_title(f"{y_split[i]['Date'].dt.month_name().iloc[0]} {y_split[i]['Date'].dt.year.iloc[0]}", fontsize=12,
                             fontweight='bold')


            ax.axis('off')
            i += 1

    plt.savefig('output.pdf', dpi=100)



main()
