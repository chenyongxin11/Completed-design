import pandas as pd
import re

# Function to check if a string contains Chinese characters
def contains_chinese(s):
    return any('\u4e00' <= c <= '\u9fff' for c in s)

# Load the Excel file
file_path = './Chemistry_QADATA.xlsx'
data = pd.read_excel(file_path)

# Remove "*" characters from the "答案" column
data['答案'] = data['答案'].astype(str).str.replace('*', '', regex=False)


# Remove rows containing gibberish or non-Chinese characters in the "问题" and "答案" columns
# Assume gibberish means characters not typically used in Chinese texts
data = data[data['问题'].apply(contains_chinese) & data['答案'].apply(contains_chinese)]

# Save the cleaned DataFrame back to an Excel file
cleaned_file_path = './Cleaned_Chemistry_QADATA.xlsx'
data.to_excel(cleaned_file_path, index=False)
