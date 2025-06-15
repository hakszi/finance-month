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

    y = year_df(monthly_categories, 2025)
    print(y)

    fig, axes = plt.subplots(nrows=4,
                             ncols=3,
                             figsize=(10, 10),
                             dpi=100)

    visualize(y, fig, axes)


def year_df(df, year):
    return df[pd.to_datetime(df['Date']).dt.year == year]


def month_df(df, year, month):
    return df[(pd.to_datetime(df['Date']).dt.year == year)
              & (pd.to_datetime(df['Date']).dt.month == month)]


def split_year(y):
    min_y = min(sorted(set(y['Date'].dt.month)))  # first day of the given month
    max_y = max(sorted(set(y['Date'].dt.month)))  # last day of the given month
    m = []
    for i in range(min_y, max_y + 1):  # put each month into a list, later to iterate through and plot one-by-one
        m_tmp = month_df(y, y['Date'].dt.year, i)
        m.append(m_tmp)
    return m


def visualize(df, fig, axes):
    y_split = split_year(df)

    year = sorted(set(y_split[0]['Date'].dt.year))

    fig.subplots_adjust(top=0.95)
    # fig.suptitle(f'TITLEEEEEEEEEEE ({year[0]})', fontsize=35, y=.99)

    plt.rcParams.update({  # set font that scale better to high DPI (500)
        'font.family': 'DejaVu Sans',
        'text.antialiased': True,
        'font.weight': 'normal'
    })

    i = 0
    for ax in axes.flat:
        if i < len(y_split):
            sns.set_style(style="whitegrid")
            sizes = y_split[i]["Value"].values
            label = y_split[i]["Category"]
            squarify.plot(sizes=sizes, label=label, alpha=0.6, ax=ax)
            ax.axis('off')

            i += 1
            # ax.set_title(f"{m['Date'].iloc[0].year} - {m['Date'].iloc[0].month}")

    plt.savefig('output.pdf', dpi=100)  # save the heatmap as pdf for best quality
    # plt.show()


main()
