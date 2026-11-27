import streamlit as st
import uuid
from rag_pipeline import RAGPipeline

st.set_page_config(
    page_title="Assistant IA Fiscal Marocain",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# DESIGN ET COULEURS
# ==========================================

st.markdown("""
<style>

/* Fond général */
.stApp {
    background-color: #FAFAF6;
    color: #12345A;
}

/* En-tête */
[data-testid="stHeader"] {
    background-color: #FAFAF6;
}

/* Barre latérale */
[data-testid="stSidebar"] {
    background-color: #EAF5FF;
    border-right: 1px solid #D3E5F5;
}

[data-testid="stSidebar"] > div:first-child {
    background-color: #EAF5FF;
    padding-top: 20px;
}

/* Titres et textes */
h1, h2, h3, p, label {
    color: #12345A !important;
}

h1, h2, h3 {
    font-weight: 800 !important;
}

/* Titre de gauche */
[data-testid="stSidebar"] h1 {
    font-size: 19px !important;
    line-height: 1.3;
}

/* Boutons */
.stButton > button {
    background-color: #D7EAFB !important;
    color: #12345A !important;
    border: 1px solid #B9D5EE !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    min-height: 40px;
}

.stButton > button:hover {
    background-color: #C4DFF5 !important;
    border-color: #8FB9DE !important;
}

/* Messages de conversation */
[data-testid="stChatMessage"] {
    background-color: #D7EAFB !important;
    border: 1px solid #B9D5EE !important;
    border-radius: 14px !important;
    padding: 18px !important;
    margin-bottom: 14px !important;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    color: #12345A !important;
}

/* Barre de question */
[data-testid="stChatInput"] {
    background-color: #D7EAFB !important;
    border: 1px solid #B9D5EE !important;
    border-radius: 14px !important;
}

[data-testid="stChatInput"] textarea {
    background-color: #D7EAFB !important;
    color: #12345A !important;
    font-weight: 600 !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #45627F !important;
}

/* Zone inférieure */
[data-testid="stBottom"] {
    background-color: #FAFAF6 !important;
}

[data-testid="stBottom"] > div {
    background-color: #FAFAF6 !important;
}

/* Séparateurs */
hr {
    border-color: #D3E5F5 !important;
}

/* Texte secondaire */
[data-testid="stCaptionContainer"] {
    color: #45627F !important;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# CHARGEMENT DU SYSTEME RAG
# ==========================================

@st.cache_resource
def get_rag():
    return RAGPipeline()


# ==========================================
# GESTION DES CONVERSATIONS
# ==========================================

if "conversations" not in st.session_state:
    first_id = str(uuid.uuid4())

    st.session_state.conversations = {
        first_id: {
            "title": "Nouvelle conversation",
            "messages": []
        }
    }

    st.session_state.active_conversation = first_id


# ==========================================
# BARRE LATERALE
# ==========================================

with st.sidebar:

    st.title("Assistant IA Fiscal Marocain")

    if st.button(
        "＋ Nouvelle conversation",
        type="primary",
        use_container_width=True
    ):
        new_id = str(uuid.uuid4())

        st.session_state.conversations[new_id] = {
            "title": "Nouvelle conversation",
            "messages": []
        }

        st.session_state.active_conversation = new_id
        st.rerun()

    st.divider()

    st.subheader("Historique")

    for conv_id, conv in reversed(
        list(st.session_state.conversations.items())
    ):
        if st.button(
            conv["title"],
            key=conv_id,
            use_container_width=True
        ):
            st.session_state.active_conversation = conv_id
            st.rerun()


# ==========================================
# CONVERSATION ACTIVE
# ==========================================

active_id = st.session_state.active_conversation
conversation = st.session_state.conversations[active_id]


# ==========================================
# TITRE ET SLOGAN
# ==========================================

st.markdown("""
<h2 style="color:#12345A; font-weight:800;">
Votre partenaire intelligent pour comprendre,
analyser et maîtriser la fiscalité marocaine.
</h2>

<p style="color:#45627F; font-size:16px;">
Posez vos questions en fiscalité, comptabilité
et réglementation des entreprises au Maroc.
</p>
""", unsafe_allow_html=True)

st.divider()


# ==========================================
# AFFICHAGE DES MESSAGES
# ==========================================

for message in conversation["messages"]:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ==========================================
# SAISIE ET TRAITEMENT DES QUESTIONS
# ==========================================

question = st.chat_input("Posez votre question fiscale...")

if question:

    conversation["messages"].append({
        "role": "user",
        "content": question
    })

    if conversation["title"] == "Nouvelle conversation":
        conversation["title"] = question[:35] + (
            "..." if len(question) > 35 else ""
        )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Analyse des documents en cours..."):

            try:
                rag = get_rag()
                answer = rag.answer_question(question)

            except Exception as error:
                answer = f"Une erreur est survenue : {error}"

        st.markdown(answer)

    conversation["messages"].append({
        "role": "assistant",
        "content": answer
    })

