import pandas as pd
import numpy as np
import squarify
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import product


def main():
    df = pd.read_csv('sample.csv')
    df['Date'] = pd.to_datetime(df['Date'])

    df['Month'] = df['Date'].dt.to_period('M')
    monthly_categories = df.groupby(['Month', 'Category'], as_index=False)['Value'].sum()
    monthly_categories = monthly_categories.rename(columns={'Month': 'Date'})
    monthly_categories['Date'] = monthly_categories['Date'].dt.to_timestamp(how='start')

    y = year_df(monthly_categories, 2024)
    fig, axes = plt.subplots(nrows=4,
                             ncols=3,
                             figsize=(25, 25),
                             dpi=500)

    visualize(y, fig, axes)


def year_df(df, year):
    return df[df['Date'].dt.year == year]


def month_df(df, month):
    return df[df['Date'].dt.month == month]

def split_year(y):
    all_months = range(1, 13)
    m = []
    for month in all_months:
        m_tmp = month_df(y, month)
        m.append(m_tmp)
    return m


def visualize(df, fig, axes):
    sns.set_style(style="whitegrid")
    y_split = split_year(df)
    fig.subplots_adjust(top=0.95)
    year = df['Date'].dt.year.iloc[0]
    fig.suptitle(f'Personal finance ({year})', fontsize=35, y=.99)
    plt.rcParams.update({
        'font.family': 'DejaVu Sans',
        'text.antialiased': True,
        'font.weight': 'normal'
    })

    all_categories = df['Category'].unique()
    color_palette = sns.husl_palette(h=0.01, s=0.4, l=0.7, n_colors=len(all_categories))
    category_color_map = dict(zip(all_categories, color_palette))

    i = 0
    for ax in axes.flat:
        if i < len(y_split):
            month = y_split[i]
            month = month.sort_values('Value', ascending=True)
            sizes = month["Value"].values
            label = month["Category"]
            total = f"{(sizes.sum() / 1000).round():.0f} k" if not month.empty else '-'
            month_num = i + 1
            month_name = pd.to_datetime(f'{year}-{month_num:02d}-01').strftime('%B')
            ax.set_title(f"{month_name}\n{total}", fontsize=16, fontweight='bold')

            if month.empty:
                ax.text(0.5, 0.5, 'N/A', fontsize=20, ha='center', va='center')
            else:
                colors = [category_color_map[cat] for cat in label]
                squarify.plot(
                    sizes=sizes,
                    label=label,
                    text_kwargs={'clip_on': True, 'fontsize': 14},
                    #alpha=.8,
                    #pad=True,
                    edgecolor='white',
                    linewidth=1,
                    color=colors,
                    ax=ax,
                )
                fig.canvas.draw()

                buffer_factor = 0.8
                for txt, rect in zip(ax.texts, ax.patches):
                    rect_ext = rect.get_window_extent()
                    rect_width, rect_height = rect_ext.width, rect_ext.height

                    rotation = 90 if rect_width < rect_height / 2 else 0 if rect_height < rect_width / 2 else txt.get_rotation()
                    txt.set_rotation(rotation)
                    txt.set_fontsize(14)
                    fig.canvas.draw()

                    current_extent = txt.get_window_extent()
                    if current_extent.width <= rect_width * buffer_factor and current_extent.height <= rect_height * buffer_factor:
                        continue

                    original = txt.get_text()
                    for trunc_length, size in product([6, 5, 4, 3], [14, 12, 10]):
                        if trunc_length >= len(original):
                            continue
                        txt.set_text(original[:trunc_length] + '.')
                        txt.set_fontsize(size)
                        fig.canvas.draw()
                        current_extent = txt.get_window_extent()
                        if current_extent.width <= rect_width * buffer_factor and current_extent.height <= rect_height * buffer_factor:
                            break
                    else:
                        txt.set_visible(False)

        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(True)
        i += 1
    plt.savefig('output.png', dpi=500)
    plt.close()


main()
