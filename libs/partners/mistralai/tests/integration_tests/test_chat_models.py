"""Test ChatMistral chat model."""
from langchain_mistralai.chat_models import ChatMistralAI


def test_stream() -> None:
    """Test streaming tokens from ChatMistralAI."""
    llm = ChatMistralAI()

    for token in llm.stream("I'm Pickle Rick"):
        assert isinstance(token.content, str)


async def test_astream() -> None:
    """Test streaming tokens from ChatMistralAI."""
    llm = ChatMistralAI()

    async for token in llm.astream("I'm Pickle Rick"):
        assert isinstance(token.content, str)


async def test_abatch() -> None:
    """Test streaming tokens from ChatMistralAI"""
    llm = ChatMistralAI()

    result = await llm.abatch(["I'm Pickle Rick", "I'm not Pickle Rick"])
    for token in result:
        assert isinstance(token.content, str)


async def test_abatch_tags() -> None:
    """Test batch tokens from ChatMistralAI"""
    llm = ChatMistralAI()

    result = await llm.abatch(
        ["I'm Pickle Rick", "I'm not Pickle Rick"], config={"tags": ["foo"]}
    )
    for token in result:
        assert isinstance(token.content, str)


def test_batch() -> None:
    """Test batch tokens from ChatMistralAI"""
    llm = ChatMistralAI()

    result = llm.batch(["I'm Pickle Rick", "I'm not Pickle Rick"])
    for token in result:
        assert isinstance(token.content, str)


async def test_ainvoke() -> None:
    """Test invoke tokens from ChatMistralAI"""
    llm = ChatMistralAI()

    result = await llm.ainvoke("I'm Pickle Rick", config={"tags": ["foo"]})
    assert isinstance(result.content, str)


def test_invoke() -> None:
    """Test invoke tokens from ChatMistralAI"""
    llm = ChatMistralAI()

    result = llm.invoke("I'm Pickle Rick", config=dict(tags=["foo"]))
    assert isinstance(result.content, str)


def test_structred_output() -> None:
    llm = ChatMistralAI(model="mistral-large-latest", temperature=0)
    schema = {
        "title": "AnswerWithJustification",
        "description": (
            "An answer to the user question along with justification for the answer."
        ),
        "type": "object",
        "properties": {
            "answer": {"title": "Answer", "type": "string"},
            "justification": {"title": "Justification", "type": "string"},
        },
        "required": ["answer", "justification"],
    }
    structured_llm = llm.with_structured_output(schema)
    result = structured_llm.invoke(
        "What weighs more a pound of bricks or a pound of feathers"
    )
    assert isinstance(result, dict)
