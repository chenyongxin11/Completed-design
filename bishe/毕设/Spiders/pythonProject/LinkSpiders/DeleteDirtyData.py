import pandas as pd

# 读取Excel文件中的数据
def read_data_from_excel(filename):
    df = pd.read_excel(filename)
    return df

# 删除不正确的链接（不包含http头部）和Anchor Text为空的数据，以及包含指定关键词的数据
def remove_invalid_links_and_empty_anchor_texts(df, keywords):
    # 删除不正确的链接（不包含http头部）和Anchor Text为空的数据
    df = df[df['Link URL'].str.startswith('http') & ~df['Anchor Text'].isnull()]
    # 删除包含指定关键词的数据
    for keyword in keywords:
        df = df[~df['Anchor Text'].str.contains(keyword)]
    # 删除不包含中文或英文字符的数据
    df = df[df['Anchor Text'].str.contains(r'[\u4e00-\u9fff]|[a-zA-Z]')]
    return df

# 删除非中文维基百科链接
def remove_non_chinese_wikipedia_links(df):
    df = df[df['Link URL'].str.startswith('https://zh.wikipedia.org')]
    return df

# 删除链接中同时含有指定字符串的数据
def remove_links_with_strings(df, strings):
    for string in strings:
        df = df[~df['Link URL'].str.contains(string)]
    return df

# 保存处理后的数据至新的Excel文件
def save_data_to_excel(data, output_filename='Link.xlsx'):
    data.to_excel(output_filename, index=False)
    print(f"Processed data saved to {output_filename}")

if __name__ == "__main__":
    # 读取Link.xlsx文件中的数据
    df = read_data_from_excel('Link.xlsx')

    # 要删除的关键词列表
    keywords_to_remove = ['使用条款', '维基媒体基金会', '非营利慈善机构', '隐私政策', '行为准则', '开发者', '统计', 'Cookie声明', '维基', '协议', '手机版视图', '编', '查', 'ISBN', '论', '改善这篇条目', '改善本条目']
    # 删除不正确的链接（不包含http头部），Anchor Text为空的数据，以及包含指定关键词的数据
    df = remove_invalid_links_and_empty_anchor_texts(df, keywords_to_remove)

    # 删除非中文维基百科链接
    df = remove_non_chinese_wikipedia_links(df)

    # 删除链接中同时含有指定字符串的数据
    strings_to_remove = ['Category', 'Template_talk', 'Template']
    df = remove_links_with_strings(df, strings_to_remove)

    # 保存处理后的数据至新的Excel文件
    save_data_to_excel(df)
