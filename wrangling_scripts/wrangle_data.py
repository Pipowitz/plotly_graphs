import pandas as pd
import plotly.graph_objs as go
import requests
from collections import defaultdict

# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `data/file_name.csv`

def sort_data(r):
    """
    Turns the request object into a useable dataframe
    
    Args:
        r (request): The request object containing the data
        
    Returns:
        df (pandas DataFrame): A dataframe consisting of the country, the years and the values
    """
    data = defaultdict(list)
    for entry in r.json()[1]:
        # check if country is already in dictionary. If so, append the new x and y values to the lists
        if data[entry['country']['value']]:
            data[entry['country']['value']][0].append(int(entry['date']))
            data[entry['country']['value']][1].append(float(entry['value']))       
        else: # if country not in dictionary, then initialize the lists that will hold the x and y values
            data[entry['country']['value']] = [[],[]] 
    
    df = pd.DataFrame(columns=["country", "year", "value"])
    # turn the dict into a pandas Dataframe
    for country in data:
        df_country = pd.DataFrame({"country":[country]*len(data[country][0]), "year":data[country][0], "value":data[country][1]})
        df_country.sort_values("year", inplace=True)
        df=df.append(df_country, ignore_index=True)
        
    return df

def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """
    
    payload = {'format': 'json', 'per_page': '500', 'date':'1990:2022'}
    r = requests.get('http://api.worldbank.org/v2/countries/cn;in/indicators/SP.POP.GROW', params=payload)
    
    df_one=sort_data(r)
    countrylist = df_one.country.unique().tolist()
    # first chart plots arable land from 1990 to 2015 in top 10 economies 
    # as a line chart
    graph_one = []    
    for country in countrylist:
        x_val = df_one[df_one['country'] == country].year.tolist()
        y_val =  df_one[df_one['country'] == country].value.tolist()
    
        graph_one.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = country
          )
        )

    layout_one = dict(title = 'Population growth',
                xaxis = dict(title = 'year'),
                yaxis = dict(title = 'Population growth [%]'),
                )

# second chart plots ararble land for 2015 as a bar chart    

    
    df_one_bar = df_one[df_one["year"]== 2020]
    x_val=df_one_bar.country.tolist()
    y_val=df_one_bar.value.tolist()
    graph_two = []

    graph_two.append(
      go.Bar(
      x = x_val,
      y = y_val,
      )
    )

    layout_two = dict(title = 'Population growth in 2022',
                xaxis = dict(title = 'country'),
                yaxis = dict(title = 'Population growth [%]'),
                )


# third chart plots percent of population that is rural from 1990 to 2015
    payload = {'format': 'json', 'per_page': '500', 'date':'1990:2022'}
    r = requests.get('http://api.worldbank.org/v2/countries/cn;in/indicators/SP.RUR.TOTL.ZG', params=payload)
    
    df_two=sort_data(r)
    countrylist = df_two.country.unique().tolist()
    # first chart plots arable land from 1990 to 2015 in top 10 economies 
    # as a line chart
    graph_three = []
    for country in countrylist:
        x_val = df_two[df_two['country'] == country].year.tolist()
        y_val =  df_two[df_two['country'] == country].value.tolist()
    
        graph_three.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name=country
          )
        )

    layout_three = dict(title = 'Population growth',
                xaxis = dict(title = 'year'),
                yaxis = dict(title = 'Population growth [%]'),
                )
    
# fourth chart shows rural population vs arable land
    graph_four = []
    df_four=df_one.merge(df_two, on=['country', 'year'])

    for country in countrylist:
        x_val = df_four[df_four['country'] == country].value_x.tolist()
        y_val = df_four[df_four['country'] == country].value_y.tolist()
        year = df_four[df_four['country'] == country].year.tolist()
        country_label = df_four[df_four['country'] == country].country.tolist()

        text = []
        for country, year in zip(country_label, year):
            text.append(str(country) + ' ' + str(year))

        graph_four.append(
            go.Scatter(
                x = x_val,
                y = y_val,
                mode = 'markers',
                text = text,
                name = country,
                textposition = 'top'
                )
            )


    layout_four = dict(title = 'Chart Four',
                xaxis = dict(title = 'x-axis label'),
                yaxis = dict(title = 'y-axis label'),
                )
    
    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))

    return figures