import os
import openai
import pinecone
import tiktoken
import asyncio
from dotenv import load_dotenv

import json
from pathlib import Path

# llama index
from llama_index import VectorStoreIndex, ResponseSynthesizer, ServiceContext, LLMPredictor
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.query_engine import RetrieverQueryEngine, SubQuestionQueryEngine
from llama_index.vector_stores import PineconeVectorStore
from llama_index.vector_stores.types import ExactMatchFilter, MetadataFilters
from llama_index.indices.vector_store.retrievers.retriever import VectorIndexRetriever


load_dotenv()

def get_vectorstoreindex() -> VectorStoreIndex:
    # 파인콘 config
    pinecone.init(
        api_key=os.getenv("PINECONE_API_KEY"),
        environment=os.getenv("PINECONE_ENVIRONMENT"),
    )
    pinecone_index = pinecone.Index(os.getenv("PINECONE_INDEX"))
    # 출력에서 사용 토크나이저 계산
    vector_store = PineconeVectorStore(
        pinecone_index=pinecone_index, tokenizer=tiktoken.get_encoding("cl100k_base")
    )

    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    return index


def get_retrievers(
    index: VectorStoreIndex, selected_files: list[str], top_k: int = 2
) -> dict[str, VectorIndexRetriever]:
    """
    file이름이 list로 들어오면 for문을 돌면서 파일하나당 retrieval를 만들어서
    {파일이름: retrieval객체, ..}로 반환해주는 함수

    """
    retrievers = {}
    for file_name in selected_files:
        exact_match_filter = [ExactMatchFilter(key="file_name", value=file_name)]
        metadata_filter = MetadataFilters(filters=exact_match_filter)
        retrievers[file_name] = index.as_retriever(
            similarity_top_k=top_k, filters=metadata_filter, 
        )

    return retrievers


def make_synthesizer() -> ResponseSynthesizer: #responsemode: str = "compact"
    """
    subquery로 얻은 정보를 통해 최종답변 방식 설정하는것
    """
    responseSynthesizer = ResponseSynthesizer.from_args(
        verbose=True
    ) #response_mode=responsemode, 
    return responseSynthesizer


def make_engine(
    retreivers: dict, responseSynthesizer: ResponseSynthesizer
    ) -> dict[str, RetrieverQueryEngine]:
    """
    엔진만들기
    """
    engines = {}
    for file_name in retreivers:
        engines[file_name] = RetrieverQueryEngine(
            retriever=retreivers[file_name], response_synthesizer=responseSynthesizer
        )

    return engines


def make_subqueryengine(
    engines: dict[str, RetrieverQueryEngine]
    ) -> SubQuestionQueryEngine:
    """
    engine으로 subqeury enigine만들기
    """

    query_engine_tools = [
        QueryEngineTool(
            query_engine=query_engine,
            metadata=ToolMetadata(
                name=file_name.split('.')[0],
                description=f"""Provide infomration about {file_name}""" 
            ),
        )
        for file_name, query_engine in engines.items()
    ]
    query_engine = SubQuestionQueryEngine.from_defaults(
        query_engine_tools=query_engine_tools,
    )
    print(query_engine_tools)
    return query_engine


def final_engine(options):
    index = get_vectorstoreindex()
    responseSynthesizer = make_synthesizer()
    retrievers = get_retrievers(index=index, selected_files=options)
    engines = make_engine(retrievers, responseSynthesizer)
    if len(options) == 1:
        engine = engines[options[0]]
    else:
        engine = make_subqueryengine(engines)
    return engine


# async def final_engine(options):
#     index = await asyncio.to_thread(get_vectorstoreindex)
#     responseSynthesizer = await asyncio.to_thread(make_synthesizer)
#     retrievers = await asyncio.to_thread(get_retrievers, index=index, selected_files=options)
#     engines = await asyncio.to_thread(make_engine, retrievers, responseSynthesizer)
#     if len(options) == 1:
#         engine = engines[options[0]]
#     else:
#         engine = await asyncio.to_thread(make_subqueryengine, engines)
#     return engine

# 체크함수들
def check_index(index: VectorStoreIndex, query: str) -> None:
    """
    index 확인 코드
    """   
    index_test = index.as_retriever()
    qury_node = index_test.retrieve(query)
    ans = qury_node[0]
    print(ans.node.metadata)
    print(ans.node.text)


def check_retrievers(selected_files, retreivers, query):
    """
    retriever 확인하는 함수
    """
    for name in selected_files:
        print(name)
        vectorindexretriever = retreivers['우리은행_WON플러스 예금.pdf']
        nodes = vectorindexretriever.retrieve(query)

        if not nodes:
            print("뽑아온 노드 없음")

        for node in nodes:
            print(f"노드출력: {node}")
            if node.node.metadata:
                print(node.node.metadata)
            else:
                print("없어용")

# def summary(file_name):
#     file = file_name.split(".")[0]
#     json_path = str(Path(__file__).resolve().parent.parent)+"\summary_prompt.json"
#     with open(json_path, "r", encoding="utf-8") as f:
# 	    data = json.load(f)
#     summary = data[file]
#     description = f"""Provides information about {file_name}, and the summary of the information is enclosed in triple backticks(```)
#         ```{summary}```"""
#     return description


# async def query_response(query_engine, query):
#     response = await query_engine.aquery(query)
#     return response


# async def get_response(question, options, is_sub_question: bool=True): 
#     openai.api_key = os.getenv("OPENAI_API_KEY")

#     index = get_vectorstoreindex()
#     responseSynthesizer = make_synthesizer()
#     retrievers = get_retrievers(index=index, selected_files=options)
#     engines = make_engine(retrievers, responseSynthesizer)

#     if is_sub_question:
#         subq_engine = make_subqueryengine(engines)
#         response = await query_response(subq_engine, question)
#     else:
#         response = await query_response(engines[options[0]], question)

#     return response

# async def main():
#     load_dotenv()
#     openai.api_key = os.getenv("OPENAI_API_KEY")
#     question = "우리은행과 신한은행의 가입대상에 대해서 각각 자세히 알려줘"
#     options = ["우리은행_WON플러스 예금.pdf", "신한은행_땡겨요 적금.pdf"]
#     index = get_vectorstoreindex()
#     check_index(index, question)
#     responseSynthesizer = make_synthesizer()
#     retrievers = get_retrievers(index=index, selected_files=options)
#     check_retrievers(options, retrievers, question)
#     engines = make_engine(retrievers, responseSynthesizer)
#     subq_engine = make_subqueryengine(engines)
#     response = await query_response(subq_engine, question)
#     print(response)



# if __name__ == "__main__":
#     # asyncio.run(main())




