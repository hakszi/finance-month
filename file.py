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
        if m_tmp.empty:
            month_year = pd.to_datetime(f'{year}-{month:02d}-01')
            m_tmp = pd.DataFrame({'Category': ['N/A'], 'Value': [0], 'Date': [month_year]})
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
            sizes = month["Value"].values
            label = month["Category"]
            min_label_size = 1000
            if label.iloc[0] == 'N/A':
                title = month["Date"].dt.strftime('%B').iloc[0]
                ax.text(0.5, 0.5, f'N/A\n{title}', fontsize=20, ha='center', va='center')

            else:
                font_sizes = np.clip(6 + (sizes / sizes.max()) * 4, 6, 10).astype(int)
                text_labels = [f"{label.iloc[i]}" if sizes[i] > min_label_size else '' for i in range(len(label))]

                sns.set_style(style="whitegrid")
                squarify.plot(sizes=sizes,
                              label=text_labels,
                              text_kwargs={'clip_on': True, 'fontsize': 8},
                              alpha=0.6,
                              ax=ax,
                              edgecolor='white',
                              linewidth=1, pad=True
                              )
                ax.set_title(f"{month['Date'].dt.month_name().iloc[0]}",
                             fontsize=12,
                             fontweight='bold',
                             )
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(True)

        i += 1
    plt.savefig('output.pdf', dpi=100)
    plt.close()


main()
