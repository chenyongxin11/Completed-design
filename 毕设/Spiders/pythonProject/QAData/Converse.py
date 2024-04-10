import pandas as pd
import json

# Load the Excel file
file_path = './Cleaned_Chemistry_QADATA.xlsx'  # 请替换为实际的文件路径
df = pd.read_excel(file_path)

# Use ffill() to fill NaN values with the previous non-NaN values
df_filled = df.ffill()

# Initialize the list to hold JSON formatted data
json_data = []

# Iterate through each row in the DataFrame and construct the JSON objects
for idx, row in df_filled.iterrows():
    json_obj = {
        "id": idx + 1,
        "firsttitle": row["一级标题"],
        "secondtitle": row["二级标题"],
        "question": row["问题"],
        "answer": row["答案"]
    }
    json_data.append(json_obj)

# Save the json data to a file
json_file_path = 'data.json'  # 您可以根据需要更改保存路径
with open(json_file_path, 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=4)

# 输出文件路径，以便知道文件被保存到了哪里
print(f'JSON文件已保存到：{json_file_path}')
