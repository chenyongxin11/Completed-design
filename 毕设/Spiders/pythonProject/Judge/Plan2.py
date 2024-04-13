from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import pandas as pd
import jieba
import numpy as np
import matplotlib.pyplot as plt

# 修改 BLEU 计算函数，使其处理单个句子对
def calculate_bleu(reference, candidate):
    smoothie = SmoothingFunction().method4
    return sentence_bleu([jieba.lcut(reference)], jieba.lcut(candidate), smoothing_function=smoothie)

# 绘制饼状图的函数
def plot_pie_chart(data, title):
    intervals = [(0, 0.25), (0.25, 0.50), (0.50, 0.75), (0.75, 1.00)]
    labels = ['0-0.25', '0.25-0.50', '0.50-0.75', '0.75-1.00']
    counts = [sum((score > low) & (score <= high) for score in data) for low, high in intervals]
    plt.figure(figsize=(7, 7))
    plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title(title)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()

# 主函数，读取数据，计算 BLEU 得分，并输出结果
def main(file_path):
    data = pd.read_excel(file_path)
    bleu_scores = []

    for index, row in data.iterrows():
        score = calculate_bleu(row['标准答案'], row['预测答案'])
        bleu_scores.append(score)

    # 绘制饼状图
    plot_pie_chart(bleu_scores, "BLEU Score Distribution")

    # 找到得分最高和最低的问答对，并打印详细信息
    max_idx = np.argmax(bleu_scores)
    min_idx = np.argmin(bleu_scores)

    print("Highest BLEU score:")
    print(f"Score: {bleu_scores[max_idx]}")
    print(f"Q: {data.loc[max_idx, '问题']}")
    print(f"Reference A: {data.loc[max_idx, '标准答案']}")
    print(f"Predicted A: {data.loc[max_idx, '预测答案']}\n")

    print("Lowest BLEU score:")
    print(f"Score: {bleu_scores[min_idx]}")
    print(f"Q: {data.loc[min_idx, '问题']}")
    print(f"Reference A: {data.loc[min_idx, '标准答案']}")
    print(f"Predicted A: {data.loc[min_idx, '预测答案']}\n")

# 指定 Excel 文件路径
file_path = './预测结果.xlsx'
main(file_path)
