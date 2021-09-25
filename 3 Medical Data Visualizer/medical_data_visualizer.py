import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column
df["height"] = 0.01 * df["height"]
df = df.assign(overweight =  (df.weight) / (2 ** df.height))
df.loc[df['overweight'] <= 25, 'overweight'] = 0
df.loc[df['overweight'] > 25, 'overweight'] = 1
df['overweight'] = df['overweight'].astype('int64')

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.

df.loc[df['cholesterol'] <= 1, 'cholesterol'] = 0
df.loc[df['cholesterol'] > 1, 'cholesterol'] = 1
df.loc[df['gluc'] <= 1, 'gluc'] = 0
df.loc[df['gluc'] > 1, 'gluc'] = 1

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, id_vars=['cardio'],value_vars=[
                'active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'])


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat = df_cat.groupby(['cardio', 'variable','value'])[['value']].count().rename({'value': 'total'},axis=1).reset_index()

    # Draw the catplot with 'sns.catplot()'

    sns.catplot(data = df_cat,
           x='variable',
           y='total',
           kind='bar',
           hue='value',
           col='cardio')

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df.loc[df['ap_hi'] < df['ap_lo'], 'ap_lo'] = df['ap_lo']/10
    df['ap_lo'] = df['ap_lo'].astype('int64')

    df.loc[df['height'] < df['height'].quantile(0.025), 'height'] = 1.5
    df.loc[df['height'] > df['height'].quantile(0.975), 'height'] = 1.8
    df.loc[df['weight'] < df['weight'].quantile(0.025), 'weight'] = 51.0
    df.loc[df['weight'] > df['weight'].quantile(0.975), 'weight'] = 108.0

    df_heat = None
    

    # Calculate the correlation matrix
    corr = df.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(corr)



    # Set up the matplotlib figure
    fig, ax = plt.figure(figsize = (12,8))

    # Draw the heatmap with 'sns.heatmap()'

    sns.heatmap(corr, annot=True, mask = mask, center=0,
            linewidths=.5, square=True,
            vmin=-0.15, vmax=0.3, fmt='0.1f')
    plt.show()

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
