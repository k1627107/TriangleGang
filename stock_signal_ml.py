import yfinance as yf
import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import MACD
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import matplotlib.pyplot as plt

# 1. Fetch Data Function
def get_stock_data(ticker, start_date, end_date):
    df = yf.download(ticker, start=start_date, end=end_date)
    df.dropna(inplace=True)
    return df

# 2. Add Indicators
def add_technical_indicators(df):
    df['RSI'] = RSIIndicator(df['Close'], window=14).rsi()
    macd = MACD(df['Close'])
    df['MACD'] = macd.macd()
    df['Signal_Line'] = macd.macd_signal()
    df['MACD_Hist'] = macd.macd_diff()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['SMA_200'] = df['Close'].rolling(window=200).mean()
    df['Price_Change'] = df['Close'].pct_change()
    df.dropna(inplace=True)
    return df

# 3. Label Creation: 1 if price goes up next day, 0 if down/stays
def create_labels(df):
    df['Target'] = np.where(df['Close'].shift(-1) > df['Close'], 1, 0)
    return df

# 4. Prepare Features & Labels
def prepare_data(df):
    features = ['RSI', 'MACD', 'Signal_Line', 'MACD_Hist', 'SMA_50', 'SMA_200']
    X = df[features]
    y = df['Target']
    return X, y

# 5. Train Model
def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))
    return model

# 6. Correlation Analysis
def correlation_analysis(df):
    corr = df.corr()
    print("Correlation Matrix:\n", corr[['Target']])
    plt.matshow(corr)
    plt.title('Correlation Matrix Heatmap')
    plt.colorbar()
    plt.show()

# Main Execution
ticker = 'AAPL'
start_date = '2020-01-01'
end_date = '2024-12-31'

df = get_stock_data(ticker, start_date, end_date)
df = add_technical_indicators(df)
df = create_labels(df)
X, y = prepare_data(df)
correlation_analysis(df)
model = train_model(X, y)
