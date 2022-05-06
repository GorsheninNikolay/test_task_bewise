from typing import Dict, List, Set
from flask_sqlalchemy import SQLAlchemy
from ..models import Document


def help_add_document(
        hash_table: Set[str],
        ans: Dict[str, List[Dict[str, str or int]]],
        hash_text_question: str,
        doc: Dict[str, str or int],
        db: SQLAlchemy) -> None:
    """
    Функция-помощник, чтобы избавиться от повтора кода.
    """
    hash_table.add(hash_text_question)
    print(doc)
    ans['result'].append(
        {
            'id': doc['id'],
            'text_question': doc['question'],
            'text_answer': doc['answer'],
            'created_date': doc['created_at']
        }
    )
    db.session.add(
        Document(
            id=doc['id'],
            text_question=doc['question'],
            text_answer=doc['answer'],
            created_date=doc['created_at']
        )
    )
