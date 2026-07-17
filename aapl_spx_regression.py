import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

START_DATE = "2021-01-01"
END_DATE = "2025-12-31"
AAPL_CSV = Path(__file__).with_name("aapl.csv")
PLOT_PATH = Path(__file__).with_name("aapl_spy_regression.png")


def _download_close_series(ticker: str) -> pd.Series:
    data = yf.download(ticker, start=START_DATE, end=END_DATE, progress=False)
    if data.empty:
        raise RuntimeError(f"No data returned from yfinance for {ticker}.")

    if isinstance(data.columns, pd.MultiIndex):
        close = data.xs("Close", axis=1, level=0)
    else:
        close = data["Close"]

    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]

    return close.astype(float)


def load_aapl_data() -> pd.DataFrame:
    if AAPL_CSV.exists():
        df = pd.read_csv(AAPL_CSV, parse_dates=["Date"])
        df = df.dropna(subset=["Date"]).copy()
        df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
        df["Return"] = pd.to_numeric(df["Return"], errors="coerce")
        df = df[["Date", "Close", "Return"]].dropna()
        df = df.rename(columns={"Return": "AAPL_Return", "Close": "AAPL_Close"})
        return df

    close = _download_close_series("AAPL")
    return pd.DataFrame({"Date": close.index, "AAPL_Close": close}).reset_index(drop=True)


def load_spy_data() -> pd.DataFrame:
    close = _download_close_series("SPY")
    return pd.DataFrame({"Date": close.index, "SPY_Close": close}).reset_index(drop=True)


def run_regression() -> None:
    aapl = load_aapl_data()
    spy = load_spy_data()

    merged = aapl.merge(spy, on="Date", how="inner").dropna()
    merged = merged.sort_values("Date").reset_index(drop=True)

    if "AAPL_Return" not in merged.columns:
        merged["AAPL_Return"] = merged["AAPL_Close"].pct_change().fillna(0.0)
    if "SPY_Return" not in merged.columns:
        merged["SPY_Return"] = merged["SPY_Close"].pct_change().fillna(0.0)

    x = merged["SPY_Return"].to_numpy(dtype=float)
    y = merged["AAPL_Return"].to_numpy(dtype=float)

    slope, intercept = np.polyfit(x, y, 1)
    fitted = intercept + slope * x
    residuals = y - fitted

    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot else np.nan
    correlation = np.corrcoef(x, y)[0, 1]

    print("Linear Regression: AAPL Returns vs SPY Returns")
    print("=" * 48)
    print(f"Slope (beta): {slope:.6f}")
    print(f"Intercept (alpha): {intercept:.6f}")
    print(f"R-squared: {r_squared:.6f}")
    print(f"Correlation: {correlation:.6f}")
    print()
    print("Return comparison")
    print("-" * 48)
    print(f"AAPL mean return: {y.mean():.6f}")
    print(f"SPY mean return: {x.mean():.6f}")
    print(f"AAPL std return: {y.std():.6f}")
    print(f"SPY std return: {x.std():.6f}")
    print()
    print("Model")
    print("-" * 48)
    print(f"AAPL_Return = {intercept:.6f} + {slope:.6f} * SPY_Return")
    print()
    print("First 5 matched rows")
    print(merged.head().to_string(index=False))

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    axes[0].plot(merged["Date"], merged["AAPL_Close"], label="AAPL", linewidth=1.5)
    axes[0].plot(merged["Date"], merged["SPY_Close"], label="SPY", linewidth=1.5)
    axes[0].set_title("AAPL vs SPY Prices")
    axes[0].set_xlabel("Date")
    axes[0].set_ylabel("Price")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].scatter(merged["SPY_Return"], merged["AAPL_Return"], alpha=0.6)
    x_line = np.linspace(merged["SPY_Return"].min(), merged["SPY_Return"].max(), 100)
    axes[1].plot(x_line, intercept + slope * x_line, color="red", label="Regression line")
    axes[1].set_title("AAPL Returns vs SPY Returns")
    axes[1].set_xlabel("SPY Return")
    axes[1].set_ylabel("AAPL Return")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(PLOT_PATH, dpi=300, bbox_inches="tight")
    print(f"Plot saved to {PLOT_PATH}")
    plt.close(fig)


if __name__ == "__main__":
    run_regression()
