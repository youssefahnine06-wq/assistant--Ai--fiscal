from retrieval import DocumentRetriever
from gemini_client import ask_gemini


class RAGPipeline:
    def __init__(self, top_k=5):
        print("Initialisation du système RAG...")
        self.retriever = DocumentRetriever(top_k=top_k)
        print("Système RAG prêt.")

    def answer_question(self, question):
        if not question.strip():
            return "Veuillez saisir une question."

        print("\nRecherche dans les documents fiscaux...")
        results = self.retriever.search(question)

        if not results:
            return "Aucun passage pertinent trouvé dans les documents."

        context_parts = []

        for i, result in enumerate(results, start=1):
            context_parts.append(
                f"""
SOURCE {i}
Document : {result['filename']}
Catégorie : {result['category']}
Page : {result['page']}
Extrait :
{result['content']}
"""
            )

        context = "\n".join(context_parts)

        prompt = f"""
Tu es un assistant spécialisé en fiscalité marocaine,
comptabilité et réglementation des entreprises au Maroc.

Réponds à la question en utilisant prioritairement
les extraits documentaires fournis ci-dessous.

QUESTION :
{question}

DOCUMENTS RETROUVÉS :
{context}

INSTRUCTIONS :
1. Réponds en français, de manière claire et structurée.
2. Appuie tes explications sur les extraits fournis.
3. Cite le nom du document et le numéro de page utilisé.
4. N'invente jamais un article, une règle ou une référence juridique.
5. Si les extraits ne permettent pas de répondre avec certitude,
   indique clairement cette limite.
6. Ne présente pas une information ancienne comme une règle actuelle
   sans pouvoir confirmer sa validité.
7. Distingue les règles comptables des règles fiscales.

RÉPONSE :
"""

        print("Analyse des documents par Gemini...")
        response = ask_gemini(prompt)

        return response


if __name__ == "__main__":
    rag = RAGPipeline()

    print("\nASSISTANT IA FISCAL MAROCAIN")

    question = input("\nPose ta question fiscale : ")

    answer = rag.answer_question(question)

    print("\n" + "=" * 60)
    print("RÉPONSE DE L'ASSISTANT")
    print("=" * 60)
    print(answer)
