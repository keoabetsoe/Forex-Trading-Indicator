import tkinter as tk
from tkinter import messagebox
import yfinance as yf
import pandas as pd
import threading
import time

#calculate RSI
def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# trading bot class
class TradingBotApp:
    def __init__(self, master):
        self.master = master
        master.title("Forex RSI Trading Indicator")

        #labels
        self.price_label = tk.Label(master, text="Price: ", font=("Arial", 20))
        self.price_label.pack(pady=10)

        self.rsi_label = tk.Label(master, text="RSI: ", font=("Arial", 20))
        self.rsi_label.pack(pady=10)

        self.signal_label =tk.Label(master, text="Signal: ", font=("Arial", 20, 'bold'))
        self.signal_label.pack(pady=10)

        #start/stop buttons
        self.start_button = tk.Button(master, text="Start Bot", command=self.start_bot)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(master, text="Stop Bot", command=self.stop_bot, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.running = False

    def start_bot(self):
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        threading.Thread(target=self.run_bot, daemon=True).start()

    def stop_bot(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    #real-time check loop (updates every 1 minute)
    def run_bot(self):
        while self.running:
            try:
                #fetch last 100 data points (1-minute interval)
                data = yf.download('EURUSD=X', period='1d', interval='1m', auto_adjust=False)
                data['RSI'] = calculate_rsi(data['Close'])

                latest_rsi = data['RSI'].iloc[-1].item()
                latest_price = data['Close'].iloc[-1].item()
                print(f"Price: {latest_price:.5f} | RSI: {latest_rsi:.2f}")

                #update GUI
                self.price_label.config(text=f"Price: {latest_price:.5f}")
                self.rsi_label.config(text=f"RSI: {latest_rsi:.2f}")

                #check for signals
                if latest_rsi < 30:
                    signal = "BUY SIGNAL"
                    color = "green"
                elif latest_rsi > 70:
                    signal = "SELL SIGNAL"
                    color = "red"
                else:
                    signal = "no signal"
                    color = "black"

                self.signal_label.config(text=f"Signal: {signal}", fg=color)
            
            except Exception as e:
                messagebox.showerror("Error", str(e))
                self.stop_bot()
            
            time.sleep(60)

#run GUI APP
root = tk.Tk()
app = TradingBotApp(root)
root.mainloop()