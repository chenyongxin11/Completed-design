import pandas as pd
from opencc import OpenCC
import re

# 读取Excel文件中的数据
def read_data_from_excel(filename):
    df = pd.read_excel(filename)
    return df

def remove_pattern_texts(df):
    df['Content'] = df['Content'].apply(lambda x: re.sub(r'^\d+.*♠$', '', x))
    return df

# 删除 content 中的最后一个换行符
def remove_trailing_newline(df):
    df['Content'] = df['Content'].str.rstrip('\n')
    return df

# 繁体字转简体字
def traditional_to_simplified(text):
    cc = OpenCC('t2s')  # 繁体字转简体字
    simplified_text = cc.convert(text)
    return simplified_text

# 将内容中的繁体字转换为简体字
def convert_traditional_to_simplified(df):
    df['Content'] = df['Content'].apply(traditional_to_simplified)
    return df

# 删除 content 中所有包含 "(英语：...)" 格式的字段
def remove_english_translation(df):
    df['Content'] = df['Content'].apply(lambda x: re.sub(r'\（.*?\）', '', x))
    return df

# 保存结果至Excel文件
def save_to_excel(df, output_filename='ContentResultProcessed.xlsx'):
    df.to_excel(output_filename, index=False)
    print(f"Processed data saved to {output_filename}")


if __name__ == "__main__":
    # 读取数据
    df = read_data_from_excel('result.xlsx')

    # 删除 content 中的最后一个换行符
    df = remove_trailing_newline(df)

    # 删除 content 中以数字开头，以♠结尾的文本
    df = remove_pattern_texts(df)

    # 将内容中的繁体字转换为简体字
    df = convert_traditional_to_simplified(df)

    # 删除 content 中所有包含 "(英语：...)" 格式的字段
    df = remove_english_translation(df)

    # 保存结果至Excel文件
    save_to_excel(df)
