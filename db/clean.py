from db.db_handler import db
from db.models import Word, Form


words = db.query(Word).all()

data = {}


def hash(w):
    return w.word + w.description + w.category + str(len(w.forms))

for w in words:
    if hash(w) in data:
        db.delete(data[hash(w)])
        print("deleted", w.word)

    data[hash(w)] = w

db.commit()