import websocket
import json
import csv
from datetime import datetime

# Websocket URL
websocket_url = "wss://functionup.fintarget.in/ws?id=fintarget-functionup"

# OLHC data storage
olhc_data = {"Nifty": [], "Banknifty": [], "Finnifty": []}

# Moving average window
ma_window = 3
ma_data = {"Nifty": [], "Banknifty": [], "Finnifty": []}

# CSV file path
csv_file_path = "olhc_data.csv"

def on_message(ws, message):
    try:
        data = json.loads(message)
        for key, value in data.items():
            timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            olhc_data[key].append([timestamp, value, value, value, value])
            
            if len(olhc_data[key]) >= ma_window:
                # Calculate Simple Moving Average
                close_prices = [float(item[4]) for item in olhc_data[key][-ma_window:]]
                ma = sum(close_prices) / ma_window
                ma_data[key].append([timestamp, ma])

                # Save OLHC data to CSV
                with open(csv_file_path, 'a', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow([key] + olhc_data[key][-1])

                # Save SMA data to CSV (starting from the 3rd minute)
                if len(ma_data[key]) >= 3:
                    with open("sma_data.csv", 'a', newline='') as smafile:
                        sma_writer = csv.writer(smafile)
                        sma_writer.writerow([key] + ma_data[key][-1])

    except Exception as e:
        print(f"Error processing message: {e}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Closed connection")

def on_open(ws):
    print("Connection opened")

if __name__ == "__main__":
    ws = websocket.WebSocketApp(websocket_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open

    ws.run_forever()