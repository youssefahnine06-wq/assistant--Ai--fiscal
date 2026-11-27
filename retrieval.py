import json
from pathlib import Path

import faiss
import numpy as np

from embedding_model import load_embedding_model, generate_embeddings


class DocumentRetriever:
    def __init__(self, top_k=5):
        self.top_k = top_k

        print("Chargement de l'index FAISS...")
        self.index = faiss.read_index(
            "embeddings/faiss_index.bin"
        )

        print("Chargement des métadonnées...")
        with open(
            "embeddings/metadata.json",
            "r",
            encoding="utf-8"
        ) as file:
            self.documents = json.load(file)

        print("Chargement du modèle d'embeddings...")
        self.model = load_embedding_model()

        print("Moteur de recherche documentaire prêt.")

    def search(self, question):
        if not question.strip():
            return []

        question_vector = self.model.encode(
            [question],
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        question_vector = np.ascontiguousarray(
            question_vector.astype("float32")
        )

        scores, indices = self.index.search(
            question_vector,
            self.top_k
        )

        results = []

        for score, index_position in zip(
            scores[0],
            indices[0]
        ):
            if index_position < 0:
                continue

            document = self.documents[int(index_position)].copy()
            document["score"] = float(score)

            results.append(document)

        return results


if __name__ == "__main__":
    retriever = DocumentRetriever()

    question = input("\nPose ta question fiscale : ")

    results = retriever.search(question)

    print("\nPassages documentaires trouvés :\n")

    for result in results:
        print("=" * 60)
        print("Document :", result["filename"])
        print("Page :", result["page"])
        print("Catégorie :", result["category"])
        print("Pertinence :", round(result["score"], 4))
        print("Contenu :")
        print(result["content"])
        print()
