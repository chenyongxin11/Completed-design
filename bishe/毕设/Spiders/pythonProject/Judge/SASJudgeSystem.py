from sentence_transformers import CrossEncoder

# 加载预训练的跨编码器模型
model = CrossEncoder('sentence-transformers/paraphrase-xlm-r-multilingual-v1')


def compute_cross_similarity(sentence1, sentence2):
    # 直接使用跨编码器模型计算两个句子的相似度
    similarity = model.predict([(sentence1, sentence2)])

    return similarity[0]


# 示例句子
sentence1 = "在无机光电材料中，载流子主要通过光激发过程产生。当光照射到材料上时，光子的能量被电子吸收，使电子从价带激发到导带，形成电子和空穴。这些电子和空穴是电荷载流子，它们在材料内部的传输过程受到材料的电子结构和缺陷状态的影响。有效的载流子传输需要良好的材料导电性和最小化的载流子复合，以提高光电转换效率。"
sentence2 = "无机光电材料中的载流子主要通过光激发生成"

similarity = compute_cross_similarity(sentence1, sentence2)
print(f"跨编码器语义相似度: {similarity}")
