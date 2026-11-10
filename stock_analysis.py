#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from curl_cffi import requests
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# 解决图表中文显示乱码问题（Windows常用 SimHei，Mac常用 Arial Unicode MS）
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def plot_stock_data(ticker, start_date, end_date):
    # 1. 抓取指定时间段的股票历史数据
    print(f"正在获取 {ticker} 从 {start_date} 到 {end_date} 的数据...")
    session = requests.Session(impersonate="chrome", verify=False)
    stock = yf.Ticker(ticker, session=session)
    df = stock.history(start=start_date, end=end_date)

    if df.empty:
        print("未获取到数据，请检查股票代码或日期范围是否正确。")
        return

    # 2. 创建画布和上下两个子图（共享 X 轴，高度比例 3:1）
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(12, 8), sharex=True, 
        gridspec_kw={'height_ratios': [3, 1]}
    )

    # 3. 绘制上方子图：每日收盘价曲线
    ax1.plot(df.index, df['Close'], color='#1f77b4', linewidth=2, label='收盘价 (Close)')
    ax1.set_title(f"{ticker} 每日收盘价与成交量 ({start_date} 至 {end_date})", fontsize=14, fontweight='bold')
    ax1.set_ylabel("收盘价", fontsize=12)
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend(loc='upper left')

    # 4. 绘制下方子图：每日成交量（涨红跌绿）
    colors = ['#d62728' if close >= open_ else '#2ca02c' for close, open_ in zip(df['Close'], df['Open'])]
    ax2.bar(df.index, df['Volume'], color=colors, alpha=0.8, width=0.8)
    ax2.set_ylabel("成交量", fontsize=12)
    ax2.set_xlabel("日期", fontsize=12)
    ax2.grid(True, linestyle='--', alpha=0.6)

    # 5. 优化 X 轴日期显示格式
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    # 6. 调整布局并保存/展示图表
    plt.tight_layout()
    fig.autofmt_xdate()  # 自动旋转日期标签防止重叠
    plt.savefig(f"{ticker}_chart.png", dpi=300)  # 保存高清图片到本地
    print(f"图表已保存为 {ticker}_chart.png")
    plt.show()

if __name__ == "__main__":
    # 示例：获取SPCX 2026年上市后的行情数据
    # 股票代码格式参考：
    # 美股直接写代码：'SPCX' (太空探索), 'NVDA' (英伟达)
    # 港股加 .HK：'0700.HK' (腾讯控股)
    # A股上海加 .SS，深圳加 .SZ：'600519.SS' (贵州茅台), '000858.SZ' (五粮液)
    plot_stock_data(ticker="SPCX", start_date="2026-06-12", end_date="2026-11-11")
