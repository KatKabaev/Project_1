import data_download as dd
import data_plotting as dplt


def main():
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print("Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print("Общие периоды времени для данных о запасах включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, макс.")

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc):» ").upper()
    period = input("Введите период для данных (например, '1mo' для одного месяца), для указания конкретной даты "
                   "нажмите Enter: ")

    # Fetch stock data
    if not period:
        start_date = input("Введите дату начала анализа в формате 'ГГГГ-ММ-ДД': ")
        end_date = input("Введите дату окончания анализа в формате 'ГГГГ-ММ-ДД': ")
        stock_data = dd.fetch_stock_data(ticker, start_date=start_date, end_date=end_date)
    else:
        stock_data = dd.fetch_stock_data(ticker, period)


    # Add moving average to the data
    stock_data = dd.add_moving_average(stock_data)

    # Display average price to the data
    print(f'Средняя цена закрытия акций за заданный период: {dd.calculate_and_display_average_price(stock_data)}')

    # Notify of strong fluctuations
    dd.notify_if_strong_fluctuations(stock_data, 5)

    # Add rsi to the data
    dd.calculate_rsi(stock_data)

    # Create a csv-file with the selected data
    # dd.export_data_to_csv(stock_data, 'stock_data.csv')

    # Optionally select a style
    style = input("Можете выбрать стиль графика (например, 'ggplot', 'bmh', 'fivethirtyeight'), либо нажать Enter: ")

    # Plot the data
    if style:
        if period:
            dplt.create_and_save_plot(stock_data, ticker, period, style=style)
        else:
            dplt.create_and_save_plot(stock_data, ticker, start_date=start_date, end_date=end_date, style=style)

    elif period:
        dplt.create_and_save_plot(stock_data, ticker, period)
    else:
        dplt.create_and_save_plot(stock_data, ticker, start_date=start_date, end_date=end_date)


if __name__ == "__main__":
    main()
