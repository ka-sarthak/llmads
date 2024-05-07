import json
import os

from langchain_community.llms.ollama import Ollama
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from typing import List, Optional
from langchain_core.pydantic_v1 import BaseModel, Field
import uuid
from typing import List, TypedDict
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    ToolMessage,
)


llm = Ollama(model='llama3:70b')
llm.base_url = 'http://172.28.105.30/backend'


class Program(BaseModel):
    """Information about the program"""

    name: Optional[str] = Field(
        ..., description='The name of the program used to run the simulation.'
    )
    version: Optional[str] = Field(..., description='Version of the program.')
    compilation_datetime: Optional[float] = Field(
        ..., description='Date the program was compiled with respect to the UNIX epoch.'
    )


class NOMADData(BaseModel):
    """Extracted NOMAD simulation data."""

    program: Program


class Example(TypedDict):
    """A representation of an example consisting of text input and expected tool calls.

    For extraction, the tool calls are represented as instances of pydantic model.
    """

    input: str  # This is the example text
    tool_calls: List[BaseModel]  # Instances of pydantic model that should be extracted


def tool_example_to_messages(example: Example) -> List[BaseMessage]:
    """Convert an example into a list of messages that can be fed into an LLM.

    This code is an adapter that converts our example to a list of messages
    that can be fed into a chat model.

    The list of messages per example corresponds to:

    1) HumanMessage: contains the content from which content should be extracted.
    2) AIMessage: contains the extracted information from the model
    3) ToolMessage: contains confirmation to the model that the model requested a tool correctly.

    The ToolMessage is required because some of the chat models are hyper-optimized for agents
    rather than for an extraction use case.
    """
    messages: List[BaseMessage] = [HumanMessage(content=example['input'])]
    openai_tool_calls = []
    for tool_call in example['tool_calls']:
        openai_tool_calls.append(
            {
                'id': str(uuid.uuid4()),
                'type': 'function',
                'function': {
                    # The name of the function right now corresponds
                    # to the name of the pydantic model
                    # This is implicit in the API right now,
                    # and will be improved over time.
                    'name': tool_call.__class__.__name__,
                    'arguments': tool_call.json(),
                },
            }
        )
    messages.append(
        AIMessage(content='', additional_kwargs={'tool_calls': openai_tool_calls})
    )
    tool_outputs = example.get('tool_outputs') or [
        'You have correctly called this tool.'
    ] * len(openai_tool_calls)
    for output, tool_call in zip(tool_outputs, openai_tool_calls):
        messages.append(ToolMessage(content=output, tool_call_id=tool_call['id']))
    return messages


parser = JsonOutputParser(pydantic_object=NOMADData)

# Define a custom prompt to provide instructions and any additional context.
# 1) You can add examples into the prompt template to improve extraction quality
# 2) Introduce additional parameters to take context into account (e.g., include metadata
#    about the document from which the text was extracted.)
prompt = ChatPromptTemplate.from_messages(
    [
        (
            'system',
            'You are an expert extraction algorithm. '
            'Only extract relevant information from the text. '
            'If you do not know the value of an attribute asked '
            "to extract, return null for the attribute's value."
            'Wrap the output in ```json\n{format_instructions}```',
        ),
        # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
        MessagesPlaceholder('examples'),  # <-- EXAMPLES!
        # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
        ('human', '{text}'),
    ]
).partial(format_instructions=parser.get_format_instructions())

examples_dir = 'tests/data/examples'

examples = []
for n in range(1, 2):
    with (
        open(os.path.join(examples_dir, f'example{n:d}.json')) as f_json,
        open(os.path.join(examples_dir, f'example{n:d}.outcar')) as f_outcar,
    ):
        json_data = json.load(f_json)['program']
        examples.append((f_outcar.read(), Program(**json_data)))

messages = []

for text, tool_call in examples:
    messages.extend(
        tool_example_to_messages({'input': text, 'tool_calls': [tool_call]})
    )

prompt.invoke({'text': 'this is some text', 'examples': messages})

chain = prompt | llm | parser

with open(os.path.join(examples_dir, 'OUTCAR')) as f:
    res = chain.invoke(
        {
            'text': f.read(),
            'examples': messages,
        }
    )
