import torch
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("Sakil/sentence_similarity_semantic_search")

def calc_similarity(news, other_news):
    news_emb = model.encode(news)

    similarities = []
    for i in range(len(other_news)):
        paragraphs = other_news[i]
        all_sent = []
        for j in range(len(paragraphs)):
            sentences = paragraphs[j].split('.')
            for k in range(len(sentences)):
                if (len(sentences[k])>10):
                    all_sent.append(sentences[k])
        embeddings = model.encode(all_sent)
        other_news[i]=all_sent
        cos_sim = util.cos_sim(news_emb, embeddings)
        similarities.append(cos_sim)
    
    return similarities, other_news

def decision(similarities, other_news):
    threshold_similarity =0.5
    threshold_truth =0.7

    count = 0
    for i in range(len(similarities)):
        val = torch.max(similarities[i])
        idx = torch.argmax(similarities[i])
        print(val, idx)
        print(other_news[i][idx])
        if (val > threshold_similarity):
            count+=1

    if (count> threshold_truth*len(similarities)):
        return "True News"
    else:
        return "False News"
    
if __name__=="__main__":
    print("Hello")