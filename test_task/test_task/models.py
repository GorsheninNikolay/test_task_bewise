from test_task import db


class Document(db.Model):
    __tablename__ = 'document'

    id = db.Column(db.Integer, primary_key=True)
    text_question = db.Column(db.Text)  # Текст вопроса
    hash_text_question = db.Column(db.Text)  # Хеш вопроса
    text_answer = db.Column(db.Text)  # Текст ответа
    created_date = db.Column(db.Date)  # Дата создания

    def __init__(
            self, id: int,
            text_question: str,
            text_answer: str,
            created_date: str) -> None:
        self.id = id
        self.text_question = text_question
        self.hash_text_question = hash(text_question)
        self.text_answer = text_answer
        self.created_date = created_date
