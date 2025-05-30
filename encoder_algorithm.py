import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class PersonaModel:
    def __init__(self, model_path, data_path):
        self.model = SentenceTransformer(model_path)
        self.data = pd.read_pickle(data_path)
        self.embeddings = self.data['persona_embeddings']

    def find_similar_users(self, target_user_embed, top_n=5):
        similarities = {}
        for user_id, embedding in self.embeddings.items():
            sim_score = cosine_similarity([target_user_embed], [embedding])[0][0]
            similarities[user_id] = sim_score

        similar_users = sorted(similarities.items(), key=lambda x: x[1], reverse=True)[:top_n]
        return similar_users

    def get_unique_facts(self, similar_users):
        new_facts = []
        for user in similar_users:
            idx = user[0]
            facts = self.data['facts'][idx].split('.')
            for fact in facts:
                fact = fact.lower().strip('\n')
                if fact not in new_facts and fact != '':
                    new_facts.append(fact)
        return new_facts


def main():
    model_path = "sch-allie/bert_another_persona"
    data_path = 'FINAL_FINAL_flattened_data.pkl'
    
    persona_model = PersonaModel(model_path, data_path)

    user_input = input("Please enter the persona ")
    user_embedding = persona_model.model.encode(user_input)

    similar_to_user = persona_model.find_similar_users(user_embedding)

    for user in similar_to_user:
        print(persona_model.data['facts'][user[0]]) #similar personas

    unique_facts = persona_model.get_unique_facts(similar_to_user) #facts to use in dialogue

    print("------\nUnique Facts:\n")
    for fact in unique_facts:
        print(fact)


if __name__ == "__main__":
    main()