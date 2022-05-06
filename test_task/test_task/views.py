import logging
from typing import Dict, List, Tuple

from flask_restx import Resource
from requests import get
from sqlalchemy.orm import load_only

from test_task import api, db
from .utils.help_add import help_add_document


from .models import Document


@api.route('/api/document/<document_id>')
class GetQuestions(Resource):
    """
    Получаем вс записи из базы данных.
    """

    def get(self, document_id: int) -> Dict[str, List[Dict[str, str]]]:
        try:
            doc = db.session.query(Document).filter(
                Document.id == document_id
            ).one()
            ans = {'result': []}
            if doc:
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
            return ans
        except Exception as error:
            logging.error(error)


@api.route('/api/document/<questions_num>')
class RandomQuestions(Resource):
    """
    Создаем уникальные документы.

    Мой алгоритм основан на множествах и хеше строк, что
    позволяет быстро находить совпадения и избавляться от них,
    так как нахождение объекта во множестве выполняется за O(1),
    а вычисление хеша строки позволяет не сравнивать
    строки постоянно друг с другом, если, например, строка была бы
    огромная, и в это же время таких строк было бы много,
    то ответа мы бы вряд ли дождались... 🙂
    """

    def post(self, questions_num: int) -> Tuple[Dict[str, str], int]:
        try:
            ans = {'result': []}

            if int(questions_num) <= 0:
                return ans

            url = 'https://jservice.io/api/random'
            resp = get(f'{url}?count={questions_num}').json()
            documents = db.session.query(Document).options(
                load_only("hash_text_question")
            ).all()

            # Хэш таблица
            hash_table = {doc.hash_text_question for doc in documents}
            cnt = 0  # Счетчик повторов

            for doc in resp:
                hash_text_question = hash(doc['question'])
                if hash_text_question in hash_table:
                    cnt += 1
                    continue
                help_add_document(
                    hash_table, ans, hash_text_question, doc, db
                    )

            # Если повторы все-таки есть...
            if cnt > 0:
                resp.clear()
                while cnt > 0:
                    if not resp:
                        resp = get(f'{url}?count=50').json()
                    doc = resp.pop()
                    hash_text_question = hash(doc['question'])
                    if hash_text_question not in hash_table:
                        cnt -= 1
                        help_add_document(
                            hash_table, ans, hash_text_question, doc, db
                        )

            db.session.commit()
            return {'Created!': []}, 201
        except Exception as error:
            logging.error(error)
