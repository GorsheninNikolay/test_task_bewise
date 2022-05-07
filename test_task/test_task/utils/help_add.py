from typing import Dict, List
from flask_sqlalchemy import SQLAlchemy
from ..models import Document


def help_add_document(
        ans: Dict[str, List[Dict[str, str or int]]],
        doc: Dict[str, str or int],
        db: SQLAlchemy) -> None:
    """
    Функция-помощник, чтобы избавиться от повтора кода.
    """
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
