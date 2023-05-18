import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

import sys

from helpers.io import save

sys.path.append("../../")
from constants import FIG_SINGLE_WIDTH, mm2inch
from helpers.colors import set_stacked_area_colors

plt.style.use('./styles/stacked_area_sidebyside.mplstyle')

file_spa1 = "./preprocessed_data/technology/spa1_transport_energy_by_fuel.csv"
file_ssp2 = "./preprocessed_data/technology/ssp2_transport_energy_by_fuel.csv"
colors = ['thistle', 'yellow', 'skyblue', 'pink', 'palegreen']


# sns.color_palette("Set3", 5)

def get_transport_energy_by_fuel_chart(fuel_name, ax, xlable='Year', ylabel='', label=''):
    df1 = pd.read_csv(file_spa1, index_col=0)
    df1 = df1[df1['input'] == fuel_name]
    df1['region'].replace("Africa_Western", "Western Africa", inplace=True)
    df2 = pd.read_csv(file_ssp2, index_col=0)
    df2 = df2[df2['input'] == fuel_name]
    df2['region'].replace("Africa_Western", "Western Africa", inplace=True)

    ## format data in following str:

    '''
    Year Region1 Region2 ...
    2000 value1   value2 ...
    
    '''
    pt1 = pd.pivot_table(df1, index=['Year'], values='value', aggfunc=np.sum)
    pt1.reset_index(inplace=True)

    pt2 = pd.pivot_table(df2, index=['Year'], columns=['region'], values='value', aggfunc=np.sum)
    pt2.reset_index(inplace=True)

    pt3 = pd.pivot_table(df2, index=['Year'], values='value', aggfunc=np.sum)
    pt3.reset_index(inplace=True)

    # draw stacked area
    cols = [pt2[col_name] for col_name in pt2.columns[1:]]
    labels = pt2.columns[1:]

    ## calcualte area coverage for each region
    total = pt2.sum(axis=0)[1:].sum()
    area_coverage_percentage = [(sum / total) * 100 for sum in pt2.sum(axis=0)[1:]]

    # set color
    set_stacked_area_colors(ax, option_id=2)

    ax.stackplot(pt2['Year'], *cols,
                 labels=labels,
                 edgecolor='black',
                 linewidth=0.25,
                 colors=colors,
                 alpha=1
                 )

    ## add percentage of area coverage
    total_y = 0
    for i, coverage in enumerate(area_coverage_percentage):
        y = cols[i][len(cols[i]) - 1]
        x_pos = 2108 if 'Hydrogen' in ylabel else 2110
        y_pos = total_y + y / 1.5
        ax.text(x_pos, y_pos, f"{coverage:.1f}%", ha="center", va="top", fontsize='small')
        total_y += y

    ax.plot(pt1['Year'], pt1['value'], color='darkorange', linewidth=0.5, marker='.', markersize=0.8, label='SSP1')
    # draw plot at the uppermost surface of stacked area chart
    ax.plot(pt3['Year'], pt3['value'], color='seagreen', linewidth=0.5, marker='.', markersize=0.8, label='SSP2')

    years = [2020, 2040, 2060, 2080, 2100]

    ax.set_xticks(years)

    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlable)

    # give label to subplot

    ax.text(-0.15, 1.05, label, transform=ax.transAxes, fontsize='medium', fontweight='bold', va='top')


hydrogren = "H2"
electricity = "Electricity"
_, axs = plt.subplots(1, 2, figsize=(FIG_SINGLE_WIDTH, mm2inch(45)))

get_transport_energy_by_fuel_chart(hydrogren, axs[1], ylabel='Hydrogen (EJ)', label='b')
get_transport_energy_by_fuel_chart(electricity, axs[0], ylabel='Electricity (EJ)', label='a')
plt.legend(bbox_to_anchor=(-0.15, -0.35), loc='lower center', ncol=7)

plt.subplots_adjust(bottom=0.25)
# save('transport_energy_by_fuel')
plt.show()
