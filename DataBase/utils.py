from DataBase.config import db


def connect(request):
    def wrapper(*args, **kwargs):
        db.connect(reuse_if_open=True)
        result = request(*args, **kwargs)
        db.close()
        return result
    return wrapper
