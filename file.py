import pandas as pd
import numpy as np
import squarify
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.cm as cm


def main():
    df = pd.read_csv('data.csv', sep=',', header='infer')
    df['Date'] = pd.to_datetime(df['Date'])

    df['Month'] = df['Date'].dt.to_period('M')
    monthly_categories = df.groupby(['Month', 'Category'], as_index=False)['Value'].sum()
    monthly_categories = monthly_categories.rename(columns={'Month': 'Date'})
    monthly_categories['Date'] = monthly_categories['Date'].dt.to_timestamp(how='start')

    y = year_df(monthly_categories, 2025)

    fig, axes = plt.subplots(nrows=4,
                             ncols=3,
                             figsize=(25, 25),
                             dpi=100)

    visualize(y, fig, axes)
    plt.close(fig)


def year_df(df, year):
    return df[df['Date'].dt.year == year]


def month_df(df, year, month):
    return df[(df['Date'].dt.year == year) & (df['Date'].dt.month == month)]


def split_year(y):
    all_months = range(1, 13)
    m = []
    year = y['Date'].dt.year.iloc[0]
    for month in all_months:
        m_tmp = month_df(y, year, month)
        m.append(m_tmp)
    return m


def visualize(df, fig, axes):
    sns.set_style(style="whitegrid")
    y_split = split_year(df)
    fig.subplots_adjust(top=0.95)
    year = y_split[0]['Date'].dt.year.iloc[0]
    fig.suptitle(f'Personal finance ({year})', fontsize=35, y=.99)
    plt.rcParams.update({
        'font.family': 'DejaVu Sans',
        'text.antialiased': True,
        'font.weight': 'normal'
    })
    i = 0
    for ax in axes.flat:
        if i < len(y_split):
            month = y_split[i]
            month = month.sort_values('Value', ascending=True)
            sizes = month["Value"].values
            label = month["Category"]
            month_num = i + 1
            month_name = pd.to_datetime(f'{year}-{month_num:02d}-01').strftime('%B')
            ax.set_title(
                month_name,
                fontsize=16,
                fontweight='bold',
            )

            if month.empty:
                ax.text(0.5, 0.5, 'N/A', fontsize=20, ha='center', va='center')

            else:
                squarify.plot(
                    sizes=sizes,
                    label=label,
                    text_kwargs={'clip_on': True, 'fontsize': 12},
                    alpha=.8,
                    edgecolor='white',
                    linewidth=1,
                    color=sns.husl_palette(n_colors=len(label), h=0.05, s=0.7, l=0.6),
                    ax=ax,
                )


        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(True)

        i += 1
    plt.savefig('output.pdf', dpi=100)
    plt.close()


main()
