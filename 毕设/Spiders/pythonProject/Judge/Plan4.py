import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer, util, CrossEncoder
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import jieba

# 加载模型
cosine_model = SentenceTransformer('distiluse-base-multilingual-cased-v2')
cross_encoder_model = CrossEncoder('sentence-transformers/paraphrase-xlm-r-multilingual-v1')


def compute_cosine_similarity(sentence1, sentence2):
    embedding1 = cosine_model.encode(sentence1, convert_to_tensor=True)
    embedding2 = cosine_model.encode(sentence2, convert_to_tensor=True)
    sim = util.pytorch_cos_sim(embedding1, embedding2)
    return sim.item()


def compute_cross_similarity(sentence1, sentence2):
    similarity = cross_encoder_model.predict([(sentence1, sentence2)])
    return similarity[0]


def compute_bleu(reference, candidate):
    smoothie = SmoothingFunction().method4
    return sentence_bleu([jieba.lcut(reference)], jieba.lcut(candidate), smoothing_function=smoothie)


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
    cosine_results = []
    cross_results = []

    for index, row in data.iterrows():
        sentence1 = row['标准答案']
        sentence2 = row['预测答案']
        cosine_similarity = compute_cosine_similarity(sentence1, sentence2)
        cross_similarity = compute_cross_similarity(sentence1, sentence2)
        bleu_score = compute_bleu(sentence1, sentence2)

        len_ratio = len(sentence2) / len(sentence1)
        if len_ratio < 2 / 3:
            final_cosine_score = 0.3 * cosine_similarity + 0.7 * bleu_score
            final_cross_score = 0.3 * cross_similarity + 0.7 * bleu_score
        else:
            final_cosine_score = 0.7 * cosine_similarity + 0.3 * bleu_score
            final_cross_score = 0.7 * cross_similarity + 0.3 * bleu_score

        cosine_results.append(final_cosine_score)
        cross_results.append(final_cross_score)

    # 绘制最终得分的饼状图
    plot_pie_chart(cosine_results, "Cosine Similarity Combined Score Distribution")
    plot_pie_chart(cross_results, "SAS Combined Score Distribution")

    # 输出最高和最低得分的问答对
    print_scores(data, cosine_results, "Cosine Similarity")
    print_scores(data, cross_results, "SAS Similarity")


def print_scores(data, results, method):
    max_idx = np.argmax(results)
    min_idx = np.argmin(results)
    print(f"Highest {method} Score:")
    print_details(data, results, max_idx)
    print(f"Lowest {method} Score:")
    print_details(data, results, min_idx)


def print_details(data, results, idx):
    print(f"Score: {results[idx]}")
    print(f"Q: {data.loc[idx, '问题']}")
    print(f"Reference A: {data.loc[idx, '标准答案']}")
    print(f"Predicted A: {data.loc[idx, '预测答案']}\n")


# 指定 Excel 文件路径
file_path = './预测结果.xlsx'
main(file_path)
