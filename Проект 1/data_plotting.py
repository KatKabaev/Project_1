import matplotlib.pyplot as plt
import pandas as pd


def create_and_save_plot(data, ticker, period, filename=None):
    plt.figure(figsize=(10, 8))

    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()

            ax1 = plt.subplot2grid((8, 1), (0, 0), rowspan=5, colspan=1)
            ax2 = plt.subplot2grid((8, 1), (6, 0), rowspan=3, colspan=1)

            ax1.plot(dates, data['Close'].values, label='Close Price')
            ax1.plot(dates, data['Moving_Average'].values, label='Moving Average')
            ax1.set_title(f"{ticker} Цена акций с течением времени")
            ax1.set_ylabel("Цена")
            ax1.legend()
            ax2.plot(dates, data['rsi'].values, label='RSI', color='g')
            ax2.set_title(f"{ticker} RSI")
            ax2.set_xlabel("Дата")
            ax2.legend()
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        plt.plot(data['Date'], data['Close'], label='Close Price')
        plt.plot(data['Date'], data['Moving_Average'], label='Moving Average')
        plt.plot(data['Date'], data['rsi'], label='RSI')


    if filename is None:
        filename = f"{ticker}_{period}_stock_price_chart.png"

    plt.savefig(filename)
    print(f"График сохранен как {filename}")
