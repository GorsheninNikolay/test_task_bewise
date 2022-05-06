from typing import Dict, List, Set
from flask_sqlalchemy import SQLAlchemy
from ..models import Document


def help_add_document(
        hash_table: Set[str],
        ans: Dict[str, List[Dict[str, str or int]]],
        hash_text_question: str,
        doc: Document,
        db: SQLAlchemy) -> None:
    """
    Функция-помощник, чтобы избавиться от повтора кода.
    """
    hash_table.add(hash_text_question)
    ans['result'].append(
        {
            'id': doc.id,
            'text_question': doc.text_question,
            'hash_text_question': doc.hash_text_question,
            'text_answer': doc.text_answer,
            'created_date': doc.created_date.strftime(
                '%Y-%m-%d %H:%M'
            ),
        }
    )
