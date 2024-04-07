from openpyxl import Workbook
import re

# 定义文件路径
file_path = './ChemistryQADATA.md'  # 修改为你的Markdown文件路径

# 读取Markdown文件内容
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.readlines()

# 初始化工作簿和工作表
wb = Workbook()
ws = wb.active

# 添加表头
ws.append(['一级标题', '二级标题', '问题', '答案'])

# 正则表达式，用于匹配H2标题、H3标题和问题
h2_pattern = r'^## (.*)$'
h3_pattern = r'^### (.*)$'
question_pattern = r'\*\*(.*?)\*\*(.*)'

# 变量，用于存储当前的H2和H3标题及其写入状态
current_h2, current_h2_written = None, False
current_h3, current_h3_written = None, False

# 处理文件内容
for line in content:
    h2_match = re.match(h2_pattern, line)
    h3_match = re.match(h3_pattern, line)
    question_match = re.search(question_pattern, line)

    if h2_match:
        current_h2, current_h2_written = h2_match.group(1), False
        current_h3, current_h3_written = None, False  # 重置二级标题
    elif h3_match:
        current_h3, current_h3_written = h3_match.group(1), False
    elif question_match:
        question = question_match.group(1).strip()
        answer = question_match.group(2).strip()

        # 根据是否已写入，决定是否包含标题
        h2_to_write = current_h2 if not current_h2_written else ""
        h3_to_write = current_h3 if not current_h3_written else ""

        # 将匹配到的数据写入Excel表格
        ws.append([h2_to_write, h3_to_write, question, answer])

        # 标记当前标题已写入
        current_h2_written, current_h3_written = True, True

# 保存工作簿
output_file_path = './Chemistry_QADATA.xlsx'  # 修改为你希望保存的Excel文件路径
wb.save(output_file_path)
