import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Read data from CSV files
from constants import FIG_SIZE, DISPLAY_DIP
from helpers.colors import set_stacked_area_colors

file_spa1 = "../../preprocessed_data/technology/spa1_transport_energy_by_fuel.csv"
file_ssp2 = "../../preprocessed_data/technology/ssp2_transport_energy_by_fuel.csv"


def get_transport_energy_by_fuel_chart(fuel_name):
    df1 = pd.read_csv(file_spa1, index_col=0)
    df1 = df1[df1['input'] == fuel_name]
    df2 = pd.read_csv(file_ssp2, index_col=0)
    df2 = df2[df2['input'] == fuel_name]

    ## format data in following str:

    '''
    Year Region1 Region2 ...
    2000 value1   value2 ...
    
    '''
    pt1 = pd.pivot_table(df1, index=['Year'], values='value', aggfunc=np.sum)
    pt1.reset_index(inplace=True)

    pt2 = pd.pivot_table(df2, index=['Year'], columns=['region'], values='value', aggfunc=np.sum)
    pt2.reset_index(inplace=True)

    # draw stacked area
    cols = [pt2[col_name] for col_name in pt2.columns[1:]]
    labels = pt2.columns[1:]

    fig = plt.figure(figsize=FIG_SIZE, dpi=DISPLAY_DIP)
    ax = plt.subplot(111)
    # set color
    set_stacked_area_colors(ax, option_id=2)

    ax.stackplot(pt2['Year'], *cols,
                 labels=labels,
                 edgecolor='white'
                 )
    ax.plot(pt1['Year'], pt1['value'])
    ax.legend()
    plt.xlabel('Year')
    plt.ylabel('EJ')
    plt.show()


hydrogren = "H2"
electricity = "Electricity"
get_transport_energy_by_fuel_chart(hydrogren)

# TODO: add title, SSP2, SPA1