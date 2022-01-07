from plyer import notification


def output_message(newest_data):
    title = f"COVID-19 {newest_data['Country']}"
    date = f"{newest_data['Date'][:10]}"

    message = f"Total cases: {newest_data['Confirmed']:,d}\n" \
              f"Deaths: {newest_data['Deaths']:,d}\n" \
              f"Recovered: {newest_data['Recovered']:,d}\n" \
              f"Active cases: {newest_data['Active']:,d}"

    notification.notify(title, message, app_name='COVID-19 app', app_icon='./img/icon.ico', timeout=2)

    return title, date, message
