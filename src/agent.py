import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from tools import book_demo, create_ticket, check_demo_status, check_ticket_status

PERSIST_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")

def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)

class ConciergeAgent:
    def __init__(self):
        self.vectorstore = load_vectorstore()
        self.history = []

    def run(self, user_input):
        self.history.append(("user", user_input))
        lower = user_input.lower()

        is_status_check = "status" in lower or "check" in lower or "already" in lower

        if "demo" in lower:
            if is_status_check:
                result = check_demo_status(user_input)
            elif "book" in lower:
                result = book_demo(user_input)
            else:
                result = check_demo_status(user_input)
            self.history.append(("assistant", result))
            return result

        if "ticket" in lower:
            if is_status_check:
                result = check_ticket_status(user_input)
            else:
                result = create_ticket(user_input)
            self.history.append(("assistant", result))
            return result

        if "support" in lower and "status" not in lower:
            result = create_ticket(user_input)
            self.history.append(("assistant", result))
            return result

        results = self.vectorstore.similarity_search_with_relevance_scores(user_input, k=3)
        relevant = [doc for doc, score in results if score >= 0.5]

        if not relevant:
            answer = "I'm the TaskFlow concierge for Notion-related questions. I don't have information on that topic here, but I can help with Notion features, pricing, support, booking a demo, or raising a support ticket."
        else:
            context = "\n\n".join([d.page_content for d in relevant[:2]])
            answer = "Based on what I found:\n\n" + context

        self.history.append(("assistant", answer))
        return answer

def build_agent(llm=None):
    return ConciergeAgent()
