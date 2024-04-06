from sentence_transformers import SentenceTransformer, util

# 加载预训练的中文Sentence-BERT模型
model = SentenceTransformer('distiluse-base-multilingual-cased-v2')


def compute_sas_similarity(sentence1, sentence2):
    # 分别对两个句子进行编码
    embedding1 = model.encode(sentence1, convert_to_tensor=True)
    embedding2 = model.encode(sentence2, convert_to_tensor=True)

    # 计算两个嵌入向量之间的余弦相似度
    sim = util.pytorch_cos_sim(embedding1, embedding2)

    return sim.item()


# 示例句子
sentence1 = "在无机光电材料中，载流子主要通过光激发过程产生。当光照射到材料上时，光子的能量被电子吸收，使电子从价带激发到导带，形成电子和空穴。这些电子和空穴是电荷载流子，它们在材料内部的传输过程受到材料的电子结构和缺陷状态的影响。有效的载流子传输需要良好的材料导电性和最小化的载流子复合，以提高光电转换效率。"
sentence2 = "无机光电材料中的载流子主要通过光激发生成"

similarity = compute_sas_similarity(sentence1, sentence2)
print(f"SAS语义相似度: {similarity}")
