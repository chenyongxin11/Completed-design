from rouge import Rouge
from nltk.translate.bleu_score import sentence_bleu
from sklearn.metrics import f1_score, accuracy_score
from nltk.translate.bleu_score import SmoothingFunction
import jieba


def calculate_f1_em(y_true, y_pred):
    f1_scores = []
    exact_match = []

    for yt, yp in zip(y_true, y_pred):
        yt_tokens = set(jieba.lcut(yt))
        yp_tokens = set(jieba.lcut(yp))

        common_tokens = yt_tokens.intersection(yp_tokens)
        if len(common_tokens) == 0:
            f1 = 0
        else:
            precision = len(common_tokens) / len(yp_tokens)
            recall = len(common_tokens) / len(yt_tokens)
            f1 = 2 * (precision * recall) / (precision + recall)

        f1_scores.append(f1)
        exact_match.append(yt == yp)

    return {
        'f1': sum(f1_scores) / len(f1_scores) if f1_scores else 0,
        'em': sum(exact_match) / len(exact_match) if exact_match else 0
    }


def calculate_rouge(y_true, y_pred):
    rouge = Rouge()

    # 分词处理
    y_true_seg = [" ".join(jieba.cut(yt)) for yt in y_true]
    y_pred_seg = [" ".join(jieba.cut(yp)) for yp in y_pred]

    # 计算ROUGE分数
    scores = rouge.get_scores(y_pred_seg, y_true_seg, avg=True)
    return scores


def calculate_bleu(y_true, y_pred):
    # 创建一个SmoothingFunction对象
    smoothie = SmoothingFunction().method4
    bleu_scores = [sentence_bleu([jieba.lcut(y)], jieba.lcut(yp), smoothing_function=smoothie) for y, yp in zip(y_true, y_pred)]
    return sum(bleu_scores) / len(bleu_scores) if bleu_scores else 0


# 示例数据
y_true = ["在无机光电材料中，载流子主要通过光激发过程产生。当光照射到材料上时，光子的能量被电子吸收，使电子从价带激发到导带，形成电子和空穴。这些电子和空穴是电荷载流子，它们在材料内部的传输过程受到材料的电子结构和缺陷状态的影响。有效的载流子传输需要良好的材料导电性和最小化的载流子复合，以提高光电转换效率。"]
y_pred = ["无机光电材料中的载流子主要通过光激发生成"]

# 计算评估指标
f1_em_scores = calculate_f1_em(y_true, y_pred)
rouge_scores = calculate_rouge(y_true, y_pred)
bleu_score = calculate_bleu(y_true, y_pred)

print("F1 and EM scores:", f1_em_scores)
print("ROUGE scores:", rouge_scores)
print("BLEU score:", bleu_score)