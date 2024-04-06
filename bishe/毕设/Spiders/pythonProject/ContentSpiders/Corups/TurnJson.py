import pandas as pd
import json
from opencc import OpenCC

# 读取 Excel 文件中的数据
def read_data_from_excel(filename):
    df = pd.read_excel(filename)
    return df

# 将繁体字转换为简体字
def traditional_to_simplified(text):
    cc = OpenCC('t2s')  # 繁体字转简体字
    simplified_text = cc.convert(text)
    return simplified_text

# 处理数据并转换为 JSON 格式
def process_data(df):
    result = []
    for index, row in df.iterrows():
        title = traditional_to_simplified(row['Title'])
        text = row['Content'].replace('\n', '\n\n')  # 将换行符替换为 \n\n
        entry = {
            "id": index,
            "url": row['URL'],
            "title": title,
            "text": text
        }
        result.append(entry)
    return result

# 保存 JSON 数据到文件
def save_to_json(data, filename='result.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Processed data saved to {filename}")

if __name__ == "__main__":
    # 读取 Excel 文件中的数据
    df = read_data_from_excel('../ContentResultProcessed.xlsx')

    # 处理数据并转换为 JSON 格式
    processed_data = process_data(df)

    # 保存 JSON 数据到文件
    save_to_json(processed_data)
