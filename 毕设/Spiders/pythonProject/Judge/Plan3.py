import pandas as pd
from sentence_transformers import SentenceTransformer, util, CrossEncoder
import numpy as np
import matplotlib.pyplot as plt

# 加载模型
cosine_model = SentenceTransformer('distiluse-base-multilingual-cased-v2')
cross_encoder_model = CrossEncoder('sentence-transformers/paraphrase-xlm-r-multilingual-v1')

def compute_sas_similarity(sentence1, sentence2):
    embedding1 = cosine_model.encode(sentence1, convert_to_tensor=True)
    embedding2 = cosine_model.encode(sentence2, convert_to_tensor=True)
    sim = util.pytorch_cos_sim(embedding1, embedding2)
    return sim.item()

def compute_cross_similarity(sentence1, sentence2):
    similarity = cross_encoder_model.predict([(sentence1, sentence2)])
    return similarity[0]

def plot_pie_chart(data, title):
    intervals = [(0, 0.25), (0.25, 0.50), (0.50, 0.75), (0.75, 1.00)]
    labels = ['0-0.25', '0.25-0.50', '0.50-0.75', '0.75-1.00']
    counts = [sum((score > low) & (score <= high) for score in data) for low, high in intervals]
    plt.figure(figsize=(7, 7))
    plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title(title)
    plt.axis('equal')
    plt.show()

def main(file_path):
    data = pd.read_excel(file_path)
    sas_results = []
    cross_results = []

    for index, row in data.iterrows():
        sentence1 = row['标准答案']
        sentence2 = row['预测答案']
        sas_similarity = compute_sas_similarity(sentence1, sentence2)
        cross_similarity = compute_cross_similarity(sentence1, sentence2)
        sas_results.append(sas_similarity)
        cross_results.append(cross_similarity)

    # 绘制饼状图
    plot_pie_chart(sas_results, "SAS Similarity Distribution")
    plot_pie_chart(cross_results, "Cross Encoder Similarity Distribution")

    # 找到并打印得分最高和最低的问答对
    max_sas_idx = np.argmax(sas_results)
    min_sas_idx = np.argmin(sas_results)
    max_cross_idx = np.argmax(cross_results)
    min_cross_idx = np.argmin(cross_results)

    print("Highest SAS Cosine Similarity Score:")
    print_details(data, sas_results, max_sas_idx)

    print("Lowest SAS Cosine Similarity Score:")
    print_details(data, sas_results, min_sas_idx)

    print("Highest Cross Encoder Similarity Score:")
    print_details(data, cross_results, max_cross_idx)

    print("Lowest Cross Encoder Similarity Score:")
    print_details(data, cross_results, min_cross_idx)

def print_details(data, results, idx):
    print(f"Score: {results[idx]}")
    print(f"Q: {data.loc[idx, '问题']}")
    print(f"Reference A: {data.loc[idx, '标准答案']}")
    print(f"Predicted A: {data.loc[idx, '预测答案']}\n")

# 指定 Excel 文件路径
file_path = './预测结果.xlsx'
main(file_path)
