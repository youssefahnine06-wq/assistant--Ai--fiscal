from sentence_transformers import SentenceTransformer


MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


def load_embedding_model():
    print("Chargement du modèle multilingue...")
    model = SentenceTransformer(MODEL_NAME)
    print("Modèle chargé correctement.")
    return model


def generate_embeddings(texts, model):
    if not texts:
        return []

    embeddings = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embeddings
