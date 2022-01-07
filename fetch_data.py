import requests


def get_data(country):
    """
    Function fetching data and statistics about CoVid-19
    :param country: Name of the country passed from the user
    :return: JSON data
    """
    url = f'https://api.covid19api.com/total/dayone/country/{country}'
    response = requests.get(url)
    return response

