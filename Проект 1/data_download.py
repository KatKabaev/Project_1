import yfinance as yf


def fetch_stock_data(ticker, period='1mo'):
    '''
    :param ticker: тикер акции
    :param period: период акции
    :return: DataFrame с историческими данными об акциях для указанного тикера и временного периода
    '''
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data


def add_moving_average(data, window_size=5):
    '''
    Добавляет в DataFrame колонку со скользящим средним, рассчитанным на основе цен закрытия.
    :param data: DataFrame с данными
    :param window_size: количество точек данных, используемых для вычисления скользящего среднего
    :return: DataFrame с колонкой со скользящим средним
    '''
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data

def calculate_and_display_average_price(data):
    '''
    Функция для расчёта средней цены закрытия акций.
    :param data: DataFrame с данными
    :return: средняя цена закрытия акции
    '''
    average_price = round(data['Close'].mean(), 2)
    return average_price