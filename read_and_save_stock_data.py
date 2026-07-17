# -*- coding: utf-8 -*-
"""
Corrected code to download stock data using yfinance.
"""

import os
import pandas as pd
import yfinance as yf

def get_stock(ticker, start_date, end_date, s_window, l_window):
    """Retrieve stock data and compute indicators."""
    try:
        # Download stock data
        df = yf.download(ticker, start=start_date, end=end_date)
        if df.empty:
            print(f"No data found for {ticker}")
            return None

        # Newer yfinance versions return MultiIndex columns (e.g. ('Close', 'AAPL'))
        # even for a single ticker; flatten to plain column names.
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Calculate daily returns
        df['Return'] = df['Close'].pct_change().fillna(0)

        # Process date attributes
        df.reset_index(inplace=True)
        df['Date'] = pd.to_datetime(df['Date'])
        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.month
        df['Day'] = df['Date'].dt.day
        df['Weekday'] = df['Date'].dt.day_name()
        df['Week_Number'] = df['Date'].dt.strftime('%U')
        df['Year_Week'] = df['Date'].dt.strftime('%Y-%U')

        # Round price columns
        price_cols = ['Open', 'High', 'Low', 'Close']
        df[price_cols] = df[price_cols].round(2)

        # Calculate moving averages
        df['Short_MA'] = df['Close'].rolling(window=s_window, min_periods=1).mean()
        df['Long_MA'] = df['Close'].rolling(window=l_window, min_periods=1).mean()

        # Reorder columns
        col_order = [
            'Date', 'Year', 'Month', 'Day', 'Weekday', 'Week_Number', 'Year_Week',
            'Open', 'High', 'Low', 'Close', 'Volume', 'Return',
            'Short_MA', 'Long_MA'
        ]
        return df[col_order]

    except Exception as e:
        print(f"Error processing {ticker}: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    try:
        ticker = "aapl"
        output_file = os.path.join(os.getcwd(), f"{ticker}.csv")

        # Get stock data
        df = get_stock(
            ticker=ticker,
            start_date="2021-01-01",
            end_date="2025-12-31",
            s_window=14,
            l_window=50
        )

        # Save to CSV if data exists
        if df is not None:
            df.to_csv(output_file, index=False)
            print(f"Successfully saved {len(df)} records to {output_file}")
        else:
            print("No data available to save.")

    except Exception as e:
        print(f"Main execution error: {str(e)}")