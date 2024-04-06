import pandas as pd
from opencc import OpenCC

# 读取Excel文件中的数据
def read_data_from_excel(filename):
    df = pd.read_excel(filename)
    return df

# 将DataFrame中的中文繁体字转换为简体字
def convert_to_simplified_chinese(df):
    cc = OpenCC('t2s')  # 繁体字转简体字
    df['Anchor Text'] = df['Anchor Text'].fillna('').apply(lambda x: cc.convert(str(x)))
    return df

# 保存处理后的数据至新的Excel文件
def save_data_to_excel(data, output_filename='Link.xlsx'):
    data.to_excel(output_filename, index=False)
    print(f"Processed data saved to {output_filename}")


if __name__ == "__main__":
    wiki_links_df = read_data_from_excel('Link.xlsx')
    # 将中文繁体字转换为简体字
    simplified_df = convert_to_simplified_chinese(wiki_links_df)
    # 保存处理后的数据至新的Excel文件
    save_data_to_excel(simplified_df)