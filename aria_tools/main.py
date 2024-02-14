import json
import string
import requests
import pandas
import io
import re
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish


def remove_trailing(path: string, cut: string):
    if path.endswith(cut):
        return path[:-len(cut)]  # 末尾の "/" を削除して返す
    else:
        return path


def add_beginning(path: string, add: string):
    return add + remove_beginning(path, add)


def remove_beginning(path: string, cut: string):
    pattern = r'^' + cut
    return re.sub(pattern, '', path)


def extract_hostname_and_port(input_string):
    match = re.match(r'([^:]+):(\d+)', input_string)
    if match:
        hostname = match.group(1)
        port = match.group(2)
        return hostname, port
    else:
        return None, None


class AriaTools:

    def __init__(self, mqtt_domain: string, file_domain: string = ""):
        self.__file_domain = remove_trailing(file_domain, "/")
        self.__mqtt_domain = remove_trailing(mqtt_domain, "/")

    # CSVの文字列データをサーバーにアップロードします
    #
    # path: 保存先を指定します　例　/upload_file
    # file_name: ファイル名を指定します　例　aria
    # csv_data: 保存するデータ 例　col1,col2,col3
    def save_server_csv(self, path: string, file_name: string, csv_data: string):
        # ファイルデータを準備
        files = {
            'file': (remove_trailing(file_name, ".csv") + '.csv', csv_data, "text/csv")  # (ファイル名, ファイルデータ)のタプル
        }

        # POSTリクエストを送信してフォームデータとCSVデータをアップロードする
        response = requests.post(self.__file_domain + add_beginning(remove_trailing(path, "/"), "/"), files=files)
        if response.status_code != 200:
            return None
        else:
            # レスポンスを確認
            json = response.json()
            return json['file']

    # PandasデータをCSVにしてサーバーにアップロードします
    #
    # path: 保存先を指定します　例　/upload_file
    # file_name: ファイル名を指定します　例　aria
    # pandas_data: 保存するデータ
    def save_server_csv_pandas(self, path: string, file_name: string, pandas_data: pandas):
        csv_data = pandas_data.to_csv(index=False)
        print(csv_data)
        return self.save_server_csv(path, file_name, csv_data)

    # サーバーからダウンロードして、CSVの文字列データとして返します
    #
    # path: ダウンロード先を指定します　例　/csv
    # file_name: ファイル名を指定します　例　aria.csv
    def get_server_csv(self, path: string, file_name: string):
        # GETリクエストを送信してファイルをダウンロードする
        response = requests.get(
            self.__file_domain +
            add_beginning(remove_trailing(path, "/"), "/") +
            "/" +
            remove_trailing(file_name, ".csv") +
            ".csv"
        )
        if response.status_code != 200:
            return None
        else:
            return response.text

    # サーバーからダウンロードして、Pandasデータとして返します
    #
    # path: ダウンロード先を指定します　例　/csv
    # file_name: ファイル名を指定します　例　aria.csv
    def get_server_csv_pandas(self, path: string, file_name: string):
        response = self.get_server_csv(path, file_name)
        if response is not None:
            return pandas.read_csv(io.StringIO(response))
        else:
            return None

    # 文字列データをMQTTの指定されたトピックに送信します
    #
    # path: 保存先を指定します　例　/stat/send
    # data_string: 送信するデータ
    def save_mqtt_string(self, topic: string, data_string: string):
        hostname, port = extract_hostname_and_port(
            remove_beginning(
                remove_beginning(
                    self.__mqtt_domain,
                    "mqtt://"
                ),
                "mqtts://"
            )
        )
        publish.single(topic, data_string, hostname=hostname, port=int(port))

    # PandasデータをJSONにしてMQTTの指定されたトピックに送信します
    #
    # path: 保存先を指定します　例　/stat/send
    # pandas_data: 保存するデータ
    def save_mqtt_pandas(self, topic: string, pandas_data: pandas):
        data_list = json.loads(pandas_data.to_json(orient="records"))

        for item in data_list:
            self.save_mqtt_string(topic, json.dumps(item))

    # MQTTの指定されたトピックを指定された個数受信して、CSVの文字列データとして返します
    #
    # path: ダウンロード先を指定します　例　/stat/send
    # msg_count: 取得したいデータ数を指定します
    def get_mqtt_string(self, topic: string, msg_count: int = 1):
        hostname, port = extract_hostname_and_port(
            remove_beginning(
                remove_beginning(
                    self.__mqtt_domain,
                    "mqtt://"
                ),
                "mqtts://"
            )
        )
        msg = subscribe.simple(topic, hostname=hostname, port=int(port), msg_count=msg_count)
        if msg_count == 1:
            # print("%s %s" % (msg.topic, msg.payload))
            return msg.payload.decode("utf-8")
        else:
            return list(map(lambda m: m.payload.decode("utf-8"), msg))

    # MQTTの指定されたトピックを指定された個数受信して、Pandasデータとして返します
    #
    # path: ダウンロード先を指定します　例　/stat/send
    # msg_count: 取得したいデータ数を指定します
    def get_mqtt_pandas(self, topic: string, msg_count: int = 1):
        data = self.get_mqtt_string(topic, msg_count)
        if msg_count == 1:
            return pandas.read_json(io.StringIO(f"[{data}]"))
        else:
            return pandas.read_json(io.StringIO(f"[{','.join(data)}]"))
