from seaborn import distplot, boxplot, regplot
from matplotlib.pyplot import subplots, tight_layout, savefig, close, scatter, legend
# 
from pandas import concat as pdconcat, DataFrame as pdDataFrame
from numpy import log10 as np_log10
from io import BytesIO

from classes.side_functions import get_meaning_count, custom_round

def _2_arr_make_boxplot(arr1, arr2, 
    color='#92cb9e', sizes=(9, 5), dpi=100, labels=('X1', 'X2'), percentage = 0.1):
    fig, ax = subplots(figsize=sizes)
    fig.patch.set_facecolor('#eeeeee')
    ax = boxplot(
        x='label', 
        y='arr', 
        linewidth=2,
        color=color,
        zorder=5,
        data=pdconcat(
            [
                pdDataFrame(
                    data={'arr' : arr1, 'label': [labels[0]] * len(arr1)}
                ),
                pdDataFrame(
                    data={'arr' : arr2, 'label': [labels[1]] * len(arr2)}
                ),
            ]
        )
    )

    ax.xaxis.grid('Vertical', zorder=0)
    ax.set_title('Диаграмма размаха выборок', fontsize='xx-large')        
    ax.set_xlabel('Выборки', fontsize='xx-large')
    ax.set_ylabel('Значения', fontsize='xx-large')
    
    gmin = min(arr1[0], arr2[0])
    gmax = max(arr1[-1], arr2[-1])
    
    ax.axis(
            ymin=gmin - (gmax-gmin) * percentage,
            ymax=gmax + (gmax-gmin) * percentage,
    )


    tight_layout()
    
    
    buf = BytesIO()
    savefig(buf, dpi=dpi, facecolor=fig.get_facecolor(), transparent=True)
    close(fig)
    
    return buf

def _2_arr_reg_plot(arr1, arr2, 
    color='#92cb9e', sizes=(9, 5), dpi=100, labels=('X1', 'X2'), percentage=0.01):
    fig, ax = subplots(figsize=sizes)
    fig.patch.set_facecolor('#eeeeee')
    ax = regplot(
        x=arr1, 
        y=arr2,
        color=color,
        scatter_kws={

            'linewidth' : 1,
            'alpha' : 0.8,
            's' : 100,
            'marker' : 'o',
            'zorder' : 5,
            
        },
        line_kws={
            'color' : '#114b5f',
            'linestyle' : '--',
            'linewidth' : 2,
            'zorder' : 2,
            'alpha' : 0.8,
            'label' : 'Прогноз'
        },
        label= 'Данные'
    )
    ax.set_xlabel('Значения {}'.format(labels[0]), fontsize='xx-large')
    ax.set_ylabel('Значения {}'.format(labels[1]), fontsize='xx-large')
    ax.set_title('Визуализация выборок и \nсоответствующая модель линейной регрессии', fontsize='xx-large')
    
    delta = max(arr1) - min(arr1)
    ax.axis(
        xmin=min(arr1) - delta * percentage,
        xmax=max(arr1) + delta * percentage)
    
    ax.yaxis.grid(zorder=0)
    ax.xaxis.grid(zorder=0)
    
    legend()
    
    tight_layout()

    buf = BytesIO()

    tight_layout()
    savefig(buf, dpi=dpi, facecolor=fig.get_facecolor(), transparent=True)
    close(fig)

    return buf

def _1_arr_make_hist(arr, color='#92cb9e', sizes=(9, 5), dpi=100, percentage=0.01):
    meaning_count_of_array = max([get_meaning_count(el) for el in arr])

    delta = max(arr) - min(arr)

    bins_count = delta / (1 + 3.3 * np_log10(len(arr)))
    if bins_count < 5:
        bins_count = 5

    fig, ax = subplots(figsize=sizes)
    fig.patch.set_facecolor('#eeeeee')
    ax = distplot(x=arr,
                  bins=int(round(bins_count, 0)),
                  rug=True,
                  hist_kws={'linewidth': 2,                        
                            'color': color,
                            'zorder': 10,
                            'alpha': 1,
                            'edgecolor': 'grey'  # "k"#
                            },
                  kde_kws={
                      'linewidth': 3,
                      'alpha': 1,
                      "color": '#114b5f',
                      'zorder': 15
                  },
    )


    ax.set_xticks(arr, )    
    arr_meaning = [custom_round(el, meaning_count_of_array) for el in arr]
    ax.set_xticklabels(arr, rotation=90, fontsize='medium')


    ax.yaxis.grid('Vertical', zorder=0)
    ax.set_ylabel('Частота значений (Абсолютная)', fontsize='xx-large')
    ax.set_xlabel('Значения', fontsize='xx-large')
    ax.set_title('Комбинированный график гистограммы \nи кривой распределения заначений', fontsize='xx-large')

    ax.axis(
        xmin=min(arr) - delta * percentage,
        xmax=max(arr) + delta * percentage)
    #         _ = ax.set_ylabel('')
    tight_layout()

    buf = BytesIO()

    tight_layout()
    savefig(buf, dpi=dpi, facecolor=fig.get_facecolor(), transparent=True)
    close(fig)

    return buf

    histplot


def _1_arr_make_boxplot(arr, color='#88d498', sizes=(9, 5), dpi=100, percentage=0.01):
    fig, ax = subplots(figsize=sizes)
    fig.patch.set_facecolor('#eeeeee')
    delta = max(arr) - min(arr)
    ax = boxplot(
        x=arr,
        orient='h',
        linewidth=2,
        color=color,
    )

    ax.xaxis.grid('Vertical', zorder=0)
    ax.set_title('Диаграмма размаха выборки', fontsize='xx-large')        
    ax.set_xlabel('Значения', fontsize='xx-large')
    ax.axis(
            xmin=min(arr) - delta * percentage,
            xmax=max(arr) + delta * percentage)


    tight_layout()
    
    
    buf = BytesIO()
    savefig(buf, dpi=dpi, facecolor=fig.get_facecolor(), transparent=True)
    close(fig)

    return buf

def _1_true_plot(arr, true_value, color='#88d498', sizes=(9, 5), dpi=100):
    fig, ax = subplots(figsize=sizes)
    fig.patch.set_facecolor('#eeeeee')
    scatter(
        x=range(1, len(arr)+1),
        y=arr,
        linewidth=8,
        alpha=0.9,
        color=color,
        zorder=6,
        label='X эксп'
    )

    ax.xaxis.grid('Vertical', zorder=0)
    ax.set_title('Точечная диаграмма', fontsize='xx-large')        
    ax.set_xlabel('Значения', fontsize='xx-large')
    
    ax.axhline(
        xmin=0, 
        xmax=5 ,
        y=true_value, 
        color='#114b5f',
        linewidth=2,
        linestyle='--',
        zorder=1, 
        label='X действ')

    legend()
    tight_layout()    
    
    buf = BytesIO()
    savefig(buf, dpi=dpi, facecolor=fig.get_facecolor(), transparent=True)
    close(fig)

    return buf

# import numpy as np
# import seaborn as sns

# sns.set_theme()

# # Create a random dataset across several variables
# rs = np.random.default_rng(0)
# n, p = 40, 8
# d = rs.normal(0, 2, (n, p))
# d += np.log(np.arange(1, p + 1)) * -5 + 10

# # Show each distribution with both violins and points
# sns.violinplot(data=d, palette="light:g", inner="points", orient="h")