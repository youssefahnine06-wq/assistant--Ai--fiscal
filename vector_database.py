import faiss
import numpy as np
from pathlib import Path


def create_faiss_index():
    vectors_path = Path("embeddings/vectors.npy")
    index_path = Path("embeddings/faiss_index.bin")

    print("Chargement des vecteurs...")
    vectors = np.load(vectors_path)
    vectors = np.ascontiguousarray(vectors.astype("float32"))

    if vectors.ndim != 2 or vectors.shape[0] == 0:
        raise ValueError("Les vecteurs sont absents ou invalides.")

    print("Création de l'index FAISS...")
    dimension = vectors.shape[1]

    index = faiss.IndexFlatIP(dimension)
    index.add(vectors)

    print("Sauvegarde de l'index...")
    faiss.write_index(index, str(index_path))

    print("Index FAISS créé avec succès.")
    print("Nombre de vecteurs :", index.ntotal)
    print("Dimension :", index.d)


if __name__ == "__main__":
    create_faiss_index()
