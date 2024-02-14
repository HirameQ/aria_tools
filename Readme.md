# 解析ツールの使用方法

## インストール

下記のコマンドを実行してください。

```jsx
pip install git+https://github.com/HirameQ/aria_tools.git
```

Jupyter Notebookのみで使用する場合は下記の方法で行うこともできます。

```jsx
!pip install git+https://github.com/HirameQ/aria_tools.git
```

## 使用方法

ツールをインポートし、MQTTのサーバーアドレスとファイルサーバのアドレスを指定します。

一番初めに初期化するとよいでしょう

```python
import aria_tools
tools = aria_tools.AriaTools("mqtt://localhost:1883", "http://localhost:3000")
```

データを取得したい場合は下記のコマンドを実行します。

関数名としてget_[取得先]_[データフォーマット]の命名規則になっています。

```python
# CSVのファイルを取得してPandasフォーマットのデータで欲しいとき
# /csv/2024-02-06_20-24-31_aria.csvのファイルを取得します
tools.get_server_csv_pandas("/csv", "2024-02-06_20-24-31_aria.csv")

# MQTTのデータを取得してPandasフォーマットのデータで欲しいとき
# /stat/sendに来るデータを2件取得する
tools.get_mqtt_pandas("/stat/send", 2)
```

データを保存したい場合は下記のコマンドを実行します。

関数名としてsave_[取得先]_[データフォーマット]の命名規則になっています。

```python
# PandasフォーマットのデータをCSVのファイルとして保存するようにリクエストを投げます
# /file_uploadのパスにhttpのformデータでファイル名と一緒にCSVのデータとして送信します
file_name = tools.save_server_csv_pandas("/file_upload", "create_pandas", point_df)

# PandasフォーマットのデータをMQTTで送信します
# /stat/sendに来るデータを2件取得する
tools.save_mqtt_pandas("/stat/send", stat_df)
```

## 関数について

### `save_server_csv`

CSVの文字列データをサーバーにアップロードします

path: 保存先を指定します　例　/upload_file
file_name: ファイル名を指定します　例　aria
csv_data: 保存するデータ 例　col1,col2,col3

`save_server_csv(path: string, file_name: string, csv_data: string)`

### `save_server_csv_pandas`

PandasデータをCSVにしてサーバーにアップロードします

path: 保存先を指定します　例　/upload_file
file_name: ファイル名を指定します　例　aria
pandas_data: 保存するデータ

`save_server_csv_pandas(path: string, file_name: string, pandas_data: pandas)`

### `get_server_csv`

サーバーからダウンロードして、CSVの文字列データとして返します

path: ダウンロード先を指定します　例　/csv
file_name: ファイル名を指定します　例　aria.csv

`get_server_csv(self, path: string, file_name: string)`

### `get_server_csv_pandas`

サーバーからダウンロードして、Pandasデータとして返します

path: ダウンロード先を指定します　例　/csv
file_name: ファイル名を指定します　例　aria.csv

`get_server_csv_pandas(self, path: string, file_name: string)`

### `save_mqtt_string`

文字列データをMQTTの指定されたトピックに送信します

path: 保存先を指定します　例　/stat/send
data_string: 送信するデータ

`save_mqtt_string(self, topic: string, data_string: string)`

### `save_mqtt_pandas`

PandasデータをJSONにしてMQTTの指定されたトピックに送信します

path: 保存先を指定します　例　/stat/send
pandas_data: 保存するデータ

`save_mqtt_pandas(self, topic: string, pandas_data: pandas)`

### `get_mqtt_string`

MQTTの指定されたトピックを指定された個数受信して、CSVの文字列データとして返します

path: ダウンロード先を指定します　例　/stat/send
msg_count: 取得したいデータ数を指定します

`get_mqtt_string(self, topic: string, msg_count: int = 1)`

### `get_mqtt_pandas`

MQTTの指定されたトピックを指定された個数受信して、Pandasデータとして返します

path: ダウンロード先を指定します　例　/stat/send
msg_count: 取得したいデータ数を指定します

`get_mqtt_pandas(self, topic: string, msg_count: int = 1)`