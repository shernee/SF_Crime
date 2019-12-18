import pandas as pd
import numpy as np

from bokeh.plotting import figure, show
from bokeh.models import NumeralTickFormatter,ColumnDataSource 
from bokeh.palettes import magma
from bokeh.core.properties import value
from bokeh.models.widgets import PreText, Select, CheckboxGroup
from bokeh.layouts import row,column,WidgetBox

from bokeh.io import output_notebook,push_notebook,show,curdoc
output_notebook()

#load data from pickle file
df_data = pd.read_pickle('../Appdata.pkl')

#set initial District values
available_dist = df_data['PdDistrict'].unique().tolist()
dist_selection = CheckboxGroup(labels=available_dist, active=[0])
init_dist = [dist_selection.labels[i] for i in dist_selection.active]

#get available Crime Categories (only the Top 10) based on the selected Districts
def get_available_cat(dist):
    
    df_dist = df_data[df_data['PdDistrict'].isin(dist)]
    available_cat = df_dist.groupby('Category')['PdId'].count().nlargest(10).sort_values(ascending = False).index.tolist()
    
    return available_cat

available_cat = get_available_cat(init_dist)
    
#set up data to be used as a source for plots based on selected Districts and Categories
def make_data(dist, cat):
    
    df_distcat = df_data[(df_data['PdDistrict'].isin(dist)) & (df_data['Category'].isin(cat))]
    df_grouped = df_distcat.groupby('DayOfWeek')[['PdId']].count().sort_values('PdId',ascending=False)
    
    df_hour_dist = df_distcat.groupby([df_distcat.index.hour, 'PdDistrict'])['PdId'].count().unstack()
    
    bar_palette = magma(len(df_grouped))
    bar_source = ColumnDataSource(dict(
                x = df_grouped.index.tolist(),
                top = df_grouped['PdId'],
                color = bar_palette))
    
    numlines = df_hour_dist.shape[1]
    line_source = ColumnDataSource(dict(
                            x = [df_hour_dist.index.values] * numlines,
                            y = [df_hour_dist[name].values for name in df_hour_dist],
                            color = magma(numlines),
                            label = [name for name in df_hour_dist]))
    
    return bar_source, line_source

# set up plot
def make_plot(bar_source, line_source, dist, cat):
    
    x = bar_source.data['x']
    bar = figure(title =f'Number of Crimes wrt Day of Week for {cat} in {dist} District(s)', height =400, width =600,                 x_range =x)
    bar.vbar(x ='x', top ='top', bottom =0, width =0.5, color ='color', source =bar_source)
    bar.xaxis.axis_label = 'Day of Week'
    bar.yaxis.axis_label = 'Number of crimes'
    bar.xaxis.major_label_orientation = 45
    bar.yaxis.formatter = NumeralTickFormatter(format = '0,0')
    
    line = figure(title ='Hourly Crime Rate w.r.t. the selected Districts and Categories', width =600, height =400)
    line.multi_line(xs ='x', ys ='y', legend_label ='label', line_color ='color', line_width =2, source =line_source)
    line.xaxis.axis_label = 'n-th Hour'
    line.yaxis.axis_label = 'Number of crimes'
    line.yaxis.formatter = NumeralTickFormatter(format = '0,0')
    
    return bar, line


# set up widgets    
dist_head = PreText(text ='Select one or more Districts:',style ={'color':'Black', 'font-size':'large'})
cat_selection = CheckboxGroup(labels = available_cat,active = [0])
#cat_text = PreText(text =f'The top 10 Categories of Crime in the selected District(s)', style ={'color':'green', 'font-size':'large'}, width =550)
cat_head = PreText(text ='Select one or more Categories:',style ={'color':'Black', 'font-size':'large'})

#get initial data for the initial plot
init_cat = [cat_selection.labels[i] for i in cat_selection.active]
bar_source, line_source = make_data(init_dist,init_cat)


# set up callbacks
def dist_change(attrname, old, new):
    if new:
        new_dist = [available_dist[i] for i in new]
        new_cat = get_available_cat(new_dist)
        cat_selection.labels = new_cat
        old_active_cat = cat_selection.active
        update('active', old_active_cat, [0])
        update_cattext(1)
    else:
        update_cattext(0)

    
def update(attrname, old, new):
    
    dist = [dist_selection.labels[i] for i in dist_selection.active]
    cat = [cat_selection.labels[i] for i in new]
    new_barsource, new_linesource = make_data(dist,cat)
    
    bar.x_range.factors = new_barsource.data['x']
    bar_source.data.update(new_barsource.data)
    line_source.data.update(new_linesource.data)
    

def update_cattext(dist):
    if dist==0:
        cat_text.text = f'Please select a District'
        cat_text.style = {'color':'red', 'font-size':'large'}
    else:
        cat_text.text = f'The top 10 Categories of Crime in the selected District(s):'
        cat_text.style = {'color':'green', 'font-size':'large'}
    

# make initial graphs
bar, line=make_plot(bar_source, line_source, init_dist, init_cat)

#call back 'calls' for checkbox selection 
dist_selection.on_change('active', dist_change)
cat_selection.on_change('active', update)


# set up layout
dist_column = column(WidgetBox(dist_head, dist_selection, height=275))
cat_column = column(WidgetBox(cat_head, cat_selection, height=275))
sub_row = row(dist_column, cat_column)
graph_row = row(bar, line)
layout = column(sub_row, graph_row)

curdoc().add_root(layout)
curdoc().title='Bar Graph: No. of Crimes wrt Day of Week'