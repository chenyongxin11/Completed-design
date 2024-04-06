import re
import pandas as pd

# 假设的Markdown内容读取流程
markdown_file_path = '主题.md'  # 实际使用时，请确保这里的路径是正确的

# 由于在这个环境中无法直接读取文件，以下是逻辑上正确的代码示例
# 你可以将这部分代码应用于你的实际环境中

# 初始化变量
data = []
current_second_level_title = ""
current_third_level_title = ""

with open(markdown_file_path, 'r', encoding='utf-8') as file:
    markdown_content = file.read()

# 解析Markdown内容
lines = markdown_content.split('\n')
for line in lines:
    if line.startswith('## '):  # 捕获二级标题，并去除编号
        title_without_number = re.sub(r'^\d+\.\s', '', line[3:]).strip()
        current_second_level_title = title_without_number
    elif line.startswith('### '):  # 捕获三级标题，并去除编号
        title_without_number = re.sub(r'^\d+\.\s', '', line[4:]).strip()
        current_third_level_title = title_without_number
    elif bool(re.match(r'^\d+\.', line)):  # 捕获问题，假设它们以数字点开头
        question_text = re.sub(r'^\d+\.\s', '', line).strip()  # 移除问题编号
        data.append([current_second_level_title, current_third_level_title, question_text])

# 创建DataFrame
df = pd.DataFrame(data, columns=["二级标题", "三级标题", "问题"])

# 在实际环境中，以下行将保存DataFrame到Excel文件
excel_filename = '主题.xlsx'
df.to_excel(excel_filename, index=False)

excel_filename

print(f'数据已保存至 {excel_filename}')
