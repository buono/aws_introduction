# Thonnyに下記コードを書く

import network
import time
import machine
import dht
import urequests

# ---------- Wi-Fi 接続設定 ----------
SSID = "xxxx"
PASSWORD = "xxxx"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    time.sleep(0.5)
print("Wi-Fi connected:", wlan.ifconfig())

# ---------- DHT11 設定 ----------
dht_pin = machine.Pin(2)  # GP2 を使用
sensor = dht.DHT11(dht_pin)

# ---------- API Gatewayエンドポイント ----------
API_ENDPOINT = "https://xxxx.execute-api.ap-northeast-1.amazonaws.com/judge"

while True:
    try:
        # センサ計測
        sensor.measure()
        temp = sensor.temperature()

        # コンソール表示(Thonny上で確認)
        #print("Temperature:", temp, "C")

        # Lambda (API Gateway) に送るデータ
        payload = {
            "temperature": temp
        }

        # POSTリクエスト
        response = urequests.post(API_ENDPOINT, json=payload)
        # レスポンスを取得して表示
        if response.status_code == 200:
            json_data = response.json()
            print("Lambda Response:", json_data)
        else:
            print("Error:", response.status_code, response.text)

        response.close()

        time.sleep(5)  # 5秒に1回実行

    except Exception as e:
        print("Error:", e)
        time.sleep(5)

