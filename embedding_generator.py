import json
import numpy as np
from pathlib import Path

from document_loader import load_all_pdfs
from embedding_model import load_embedding_model, generate_embeddings


def create_and_save_embeddings():
    print("Chargement des documents et création des chunks...")
    documents = load_all_pdfs()

    if not documents:
        print("Aucun segment trouvé.")
        return

    print(f"Nombre de chunks : {len(documents)}")

    print("\nChargement du modèle...")
    model = load_embedding_model()

    texts = [doc["content"] for doc in documents]

    print("\nGénération des embeddings...")
    embeddings = generate_embeddings(texts, model)

    output_dir = Path("embeddings")
    output_dir.mkdir(exist_ok=True)

    np.save(output_dir / "vectors.npy", embeddings)

    with open(output_dir / "metadata.json", "w", encoding="utf-8") as file:
        json.dump(documents, file, ensure_ascii=False, indent=2)

    print("\nGénération terminée.")
    print(f"Nombre de vecteurs : {len(embeddings)}")
    print(f"Dimension des vecteurs : {embeddings.shape[1]}")
    print("Fichiers sauvegardés dans le dossier embeddings.")


if __name__ == "__main__":
    create_and_save_embeddings()
