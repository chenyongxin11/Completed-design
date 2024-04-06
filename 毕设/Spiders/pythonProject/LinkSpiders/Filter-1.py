import pandas as pd

# 读取Excel文件中的数据
def read_data_from_excel(filename):
    df = pd.read_excel(filename)
    return df

# 删除包含特定字符的行以及空数据的行
def filter_and_drop_data(df, keywords):
    for keyword in keywords:
        df = df[~df['Anchor Text'].astype(str).str.contains(keyword)]
    df = df.dropna()  # 删除空数据的行
    return df

# 保存处理后的数据至新的Excel文件
def save_data_to_excel(data, output_filename='wiki_links_filtered.xlsx'):
    data.to_excel(output_filename, index=False)
    print(f"Processed data saved to {output_filename}")

# 示例用法
if __name__ == "__main__":
    # 读取Excel文件中的数据
    wiki_links_df = read_data_from_excel('wiki_links_simplified.xlsx')

    # 删除包含特定字符的行以及空数据的行
    keywords_to_exclude = ['天', '航', '空', '·']
    filtered_df = filter_and_drop_data(wiki_links_df, keywords_to_exclude)

    # 保存处理后的数据至新的Excel文件
    save_data_to_excel(filtered_df)
