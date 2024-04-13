import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import jieba

# 模拟的 Rouge 计算函数
def mock_calculate_rouge(r, c):
    # 分词处理
    y_true_seg = [" ".join(jieba.cut(yt)) for yt in r]
    y_pred_seg = [" ".join(jieba.cut(yp)) for yp in c]

    # 模拟得分
    scores = {'rouge-1': {'f': np.random.rand(), 'p': np.random.rand(), 'r': np.random.rand()},
              'rouge-2': {'f': np.random.rand(), 'p': np.random.rand(), 'r': np.random.rand()},
              'rouge-l': {'f': np.random.rand(), 'p': np.random.rand(), 'r': np.random.rand()}}
    return scores

# 绘制饼状图的函数
def plot_pie_chart(data, score_type):
    # 定义得分区间
    intervals = [(0, 0.3), (0.3, 0.5), (0.5, 0.7), (0.7, 1)]
    labels = ['<0.3', '0.3-0.5', '0.5-0.7', '>0.7']
    counts = [data[(data[score_type] > low) & (data[score_type] <= high)].shape[0] for low, high in intervals]

    # 绘制饼状图
    fig, ax = plt.subplots()
    ax.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(f'Rouge Score Distribution: {score_type}')
    plt.show()

# 主函数，读取数据，计算每一条数据的 ROUGE 得分
def main(file_path):
    data = pd.read_excel(file_path)
    results = []

    for index, row in data.iterrows():
        score = mock_calculate_rouge([row['标准答案']], [row['预测答案']])
        results.append(score)

    # 将得分字典列表转换为 DataFrame
    results_df = pd.DataFrame(results)
    # 将字典列展开
    for col in ['rouge-1', 'rouge-2', 'rouge-l']:
        for subcol in ['f', 'p', 'r']:
            results_df[col + '.' + subcol] = results_df[col].apply(lambda x: x[subcol])
        results_df.drop(columns=[col], inplace=True)

    # 绘制饼状图
    for score_type in ['rouge-1.f', 'rouge-2.f', 'rouge-l.f']:
        plot_pie_chart(results_df, score_type)

    # 找到得分最高和最低的 QA 对，并输出详细信息
    for score_type in ['rouge-1.f', 'rouge-2.f', 'rouge-l.f']:
        max_idx = results_df[score_type].idxmax()
        min_idx = results_df[score_type].idxmin()
        print(f"Highest {score_type}:")
        print(f"Score: {results_df.loc[max_idx, score_type]}")
        print(f"Q: {data.loc[max_idx, '问题']}")
        print(f"Reference A: {data.loc[max_idx, '标准答案']}")
        print(f"Predicted A: {data.loc[max_idx, '预测答案']}\n")

        print(f"Lowest {score_type}:")
        print(f"Score: {results_df.loc[min_idx, score_type]}")
        print(f"Q: {data.loc[min_idx, '问题']}")
        print(f"Reference A: {data.loc[min_idx, '标准答案']}")
        print(f"Predicted A: {data.loc[min_idx, '预测答案']}\n")

    return results_df

# 调用主函数并打印结果
file_path = './预测结果.xlsx'
rouge_scores = main(file_path)

