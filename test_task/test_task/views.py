from typing import Dict
import logging

from flask import request
from flask_restx import Resource
from requests import get
from sqlalchemy.orm import load_only

from test_task import api, db

from .models import Document


@api.route('/api/document')
class GetQuestions(Resource):
    def get(self):
        try:
            data = db.session.query(Document).all()
            ans = {'result': []}
            for doc in data:
                ans['result'].append(
                    {
                        'id': doc.id,
                        'text_question': doc.text_question,
                        'hash_text_question': doc.hash_text_question,
                        'text_answer': doc.text_answer,
                        'created_date': doc.created_date
                    }
                )
            print(ans['result'][:5])
            return ans
        except Exception as error:
            logging.error(error)


@api.route('/api/document/<questions_num>')
class RandomQuestions(Resource):
    def post(self, questions_num: int) -> None:
        try:
            if int(questions_num) <= 0:
                return {'result': []}
            
            url = 'https://jservice.io/api/random'
            resp = get(f'{url}?count={questions_num}').json()
            documents = db.session.query(Document).options(load_only("hash_text_question")).all()

            hash_table = set()  # Хэш таблица
            cnt = 0  # Счетчик повторений

            for doc in documents:
                hash_table.add(doc.hash_text_question)

            for doc in resp:
                hash_text_question = hash(doc['question'])
                if hash_text_question in hash_table:
                    cnt += 1
                else:
                    db.session.add(
                        Document(
                            id=doc['id'],
                            text_question=doc['question'],
                            text_answer=doc['answer'],
                            created_date=doc['created_at']
                        )
                    )
                    hash_table.add(hash_text_question)

            if cnt > 0:
                resp.clear()
                while cnt > 0:
                    if not resp:
                        resp = get(f'{url}?count=200').json()
                    record = resp.pop()
                    hash_text_question = hash(record['question'])
                    if hash_text_question not in hash_table:
                        cnt -= 1
                        hash_table.add(hash_text_question)
                        db.session.add(
                            Document(
                            id=doc['id'],
                            text_question=doc['question'],
                            text_answer=doc['answer'],
                            created_date=doc['created_at']
                            )
                        )
            
            db.session.commit()
            return {'result': 'Created!'}, 201
        except Exception as error:
            logging.error(error)