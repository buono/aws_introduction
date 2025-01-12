import json

def lambda_handler(event, context):
    # event の中身をログで確認するとわかりやすい
    print("event:", event)

    # body が無い、または空の場合を考慮
    if "body" not in event or not event["body"]:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "No body found"})
        }

    try:
        # body は JSON文字列として入っているので、json.loads でパース
        body_data = json.loads(event["body"])
        temp = body_data.get("temperature")
    except Exception as e:
        print("JSON parse error:", e)
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid JSON format"})
        }

    # temperatureが取れない場合はエラー
    if temp is None:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Bad Request: temperature or humidity not provided"})
        }

    # 快適性を判定 (例)
    if temp < 20:
        comfort_level = "Too cold!"
    elif temp > 26:
        comfort_level = "Too hot!"
    else:
        comfort_level = "Comfortable!!"

    # 応答データ
    result = {
        "temperature": temp,
        "comfort_level": comfort_level
    }

    return {
        "statusCode": 200,
        "body": json.dumps(result)  # json 文字列にして返す
    }
