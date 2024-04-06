import pandas as pd

# 读取Excel文件中的数据
def read_data_from_excel(filename):
    df = pd.read_excel(filename)
    return df

# 清理冗余数据
def clean_data(df):
    cleaned_df = df.drop_duplicates()
    return cleaned_df

# 保存处理后的数据至新的Excel文件
def save_data_to_excel(data, output_filename='Link.xlsx'):
    data.to_excel(output_filename, index=False)
    print(f"Cleaned data saved to {output_filename}")

# 示例用法
if __name__ == "__main__":
    # 读取Excel文件中的数据
    wiki_links_df = read_data_from_excel('Link.xlsx')

    # 清理冗余数据
    cleaned_df = clean_data(wiki_links_df)

    # 保存处理后的数据至新的Excel文件
    save_data_to_excel(cleaned_df)
