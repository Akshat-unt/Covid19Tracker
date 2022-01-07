import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def export_to_pdf(data):
    """
    Creating and exporting plot to a PDF file basing on the given data.
    :param data: Number of total cases, deaths, active cases, fetched from the API
    :return: void
    """

    days = np.array([])
    confirmed_cases = np.array([])
    deaths = np.array([])
    active_cases = np.array([])

    # Looping over every index of JSON data
    for day, data_elem in enumerate(data):
        days = np.append(days, day)
        confirmed_cases = np.append(confirmed_cases, data_elem['Confirmed'])
        deaths = np.append(deaths, data_elem['Deaths'])
        active_cases = np.append(active_cases, data_elem['Active'])

    # Creating a plot
    plt.plot(days, confirmed_cases, color='black', label='Confirmed cases', linewidth=3)
    plt.plot(days, deaths, color='red', label='Deaths', linewidth=3)
    plt.plot(days, active_cases, color='green', label='Active cases', linewidth=3)
    plt.title(f"{data[-1]['Country']} COVID-19 statistics")

    # Creating and displaying table in a program's console using pandas
    table = [['Numbers', confirmed_cases[-1], deaths[-1], active_cases[-1]]]
    df_table = pd.DataFrame(table)
    df_table.columns = (f"{data[-1]['Country']}", 'Confirmed cases', 'Deaths', 'Active cases')
    print(df_table)

    # Setting axis and saving the plot to a PDF file
    plt.xlabel('Days since the first confirmed case')
    plt.legend()
    plt.savefig(f"./stats/{data[-1]['Country']}.pdf")
    plt.clf()
