import json
import uuid
from llama_index.response.schema import Response

#확정
async def make_dict_sub(question: str, response: Response) -> dict:
    source_nodes = response.source_nodes
    info = {
        "question": question,
        "response": response.response,
        "type": "subquery",
        "chat_id": str(uuid.uuid4()),
        "subqa": []
    }
    for node in source_nodes:
        sub_q_a = node.node.text
        info['subqa'].append(sub_q_a)
    return info


async def make_dict_single(question: str, response: Response) -> dict:
    source_nodes = response.source_nodes
    info = {
        "question": question,
        "response": response.response,
        "type": "single query",
        "chat_id": str(uuid.uuid4()),
        "ref_docs": []
    }
    for node in source_nodes:
        page_label =  node.node.extra_info["page_label"]
        file_name = node.node.extra_info["file_name"]
        text = node.node.text
        info["ref_docs"].append({"page_label": page_label, "file_name": file_name, "text": text })
    return info


