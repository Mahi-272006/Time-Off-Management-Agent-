from langchain_core.tools import tool
from rag.retriever import retriever
import re


@tool
def search_policy(query: str,country: str) -> str:
    """
    Search Acme Corp's PTO policy documents.

    Use this tool whenever the user asks about company
    leave policies, including:

    - Annual leave
    - Sick leave
    - Maternity leave
    - Parental leave
    - Carry forward rules
    - Public holidays
    - Eligibility
    - Leave approval process
    - Blackout periods
    - PTO policies

    Input:
        query: The user's policy question in natural language.

    Returns:
        Relevant sections from the company policy documents.

    Never answer policy questions from memory.
    If no relevant policy is found, explain that no policy
    information was retrieved instead of making up an answer.
    """

    search_query = f"""
    Country: {country}

    Question:
    {query}
    """

    docs = retriever.invoke(search_query)

    print("=" * 80)
    print("Retrieved docs:", len(docs))
    print("=" * 80)

    for i, doc in enumerate(docs):
        print(f"\n----- DOC {i+1} -----")
        print(doc.page_content)
        print("-" * 80)

    if not docs:
        return "No relevant policy found."

    return "\n\n".join(doc.page_content for doc in docs)