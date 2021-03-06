import logging
from typing import Dict, List, Tuple

from flask_restx import Resource
from flask import request
from requests import get

from test_task import api, db

from .models import Document
from .utils.help_add import help_add_document


@api.route('/api/document')
class RouteDocument(Resource):
    """
    GET - Получаем первые 100 документов.
    DELETE - Удаляем все документы
    POST - Создаем уникальные документы.

    Мой алгоритм основан на множестве и хеше строк, что
    позволяет быстро находить совпадения и избавляться от них,
    так как нахождение объекта во множестве выполняется за O(1),
    а вычисление хеша строки позволяет не сравнивать
    строки постоянно друг с другом. Если, например, строка была бы
    огромная, и в это же время таких строк было бы много,
    то ответа мы бы вряд ли дождались... 🙂
    """

    def get(self) -> Dict[str, List[Dict[str, str or int]]]:
        try:
            ans = {'result': []}
            docs = db.session.query(Document).limit(100)
            for doc in docs:
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

    def post(self) -> Tuple[Dict[str, List[Dict[str, str]] or str, int]]:
        try:
            ans = {'result': []}
            questions_num = request.json.get('questions_num')

            if not questions_num or int(questions_num) <= 0:
                ans['result'] = "Убедитесь, что тело запроса валидно."
                return ans, 404

            url = 'https://jservice.io/api/random'
            resp = get(f'{url}?count={questions_num}').json()

            # Хэш таблица. В крупном проекте можно было бы использовать Redis
            hash_table = {doc.hash_text_question for doc in
                          db.session.query(Document).distinct()}
            cnt = 0  # Счетчик повторов

            for doc in resp:
                hash_text_question = hash(doc['question'])
                if hash_text_question not in hash_table:
                    hash_table.add(hash_text_question)
                    help_add_document(
                        ans, doc, db
                    )
                    continue
                cnt += 1

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
                        hash_table.add(hash_text_question)
                        help_add_document(
                            ans, doc, db
                        )

            db.session.commit()
            return ans, 201
        except Exception as error:
            logging.error(error)

    def delete(self) -> Tuple[Dict[str, str], int]:
        try:
            db.session.query(Document).delete()
            db.session.commit()
            return {"result": "Deleted!"}, 204
        except Exception as error:
            logging.error(error)


@api.route('/api/document/<document_id>')
class GetDocument(Resource):
    """
    Получаем определенный документ из базы данных.
    """

    def get(self, document_id: int) -> Dict[str, List[Dict[str, str]]]:
        try:
            doc = db.session.query(Document).filter(
                Document.id == int(document_id)
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
