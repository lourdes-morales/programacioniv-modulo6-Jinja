import redis

def connect_to_redis():
    r = redis.Redis(host='localhost', port=6379, db=0)
    return r

def create_document(connection, key, document):
    result = connection.set(key, document)

def add_word(connection, word, meaning):
    key = "word:" + word.lower()
    document = meaning
    create_document(connection, key, document)

def edit_word(connection, word, new_meaning):
    key = "word:" + word.lower()
    connection.set(key, new_meaning)

def remove_word(connection, word):
    key = "word:" + word.lower()
    connection.delete(key)

def get_words(connection):
    keys = connection.keys("word:*")
    return [key.decode('utf-8').split(":")[1] for key in keys]

def get_meaning(connection, word):
    key = "word:" + word.lower()
    meaning = connection.get(key)
    if meaning is not None:
        return meaning.decode('utf-8')
    else:
        return None