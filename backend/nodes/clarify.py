from langchain_core.messages import SystemMessage

from llm import llm
from utils.context import prepare_messages


CLARIFICATION_PROMPT = """
The user is trying to submit a leave request.

Ask ONE concise clarification question.

Only ask for information that is still missing.

Never ask again for information already provided.

Do not call tools.

Do not guess dates.

Keep the reply short.
"""


def clarify_node(state):

    system_prompt = SystemMessage(content=CLARIFICATION_PROMPT)

    prompt = prepare_messages(system_prompt, state)

    response = llm.invoke(prompt)

    return {
        "messages": [response]
    }