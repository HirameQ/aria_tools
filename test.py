import aria_tools
import numpy as np

tools = aria_tools.AriaTools("mqtt://localhost:1883", "http://localhost:3000")

if __name__ == '__main__':
    # 送信するCSVデータ（文字列）
    csv_data = """col1,col2,col3
1,2,3
4,5,6
7,8,9"""
    print(tools.save_server_csv("/file_upload", "create_string", csv_data))

    point_df = tools.get_server_csv_pandas("/csv", "2024-02-06_20-24-31_aria.csv")
    print(point_df)
    point_df['mycolumn'] = np.random.rand(len(point_df.index))
    print(point_df)
    file_name = tools.save_server_csv_pandas("/file_upload", "create_pandas", point_df)
    print(file_name)

    print(tools.get_mqtt_pandas("/stat/send", 1))
    stat_df = tools.get_mqtt_pandas("/stat/send", 2)
    print(stat_df)
    stat_df['mycolumn'] = np.random.rand(len(stat_df.index))
    print(stat_df)
    tools.save_mqtt_pandas("/stat/send", stat_df)
