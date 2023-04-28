from flask import Flask, render_template, request, redirect, url_for, flash
import redis

from dictionary_functions import add_word, edit_word, remove_word, get_words, get_meaning

app = Flask(__name__)
app.secret_key = 'your_secret_key'

r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/')
def index():
    words = get_words(r)
    definitions = {word: get_meaning(r, word) for word in words}
    return render_template('index.html', definitions=definitions)

@app.route('/add_word', methods=['POST'])
def add_word_route():
    word = request.form['word']
    meaning = request.form['meaning']
    if get_meaning(r, word):
        flash(f"La palabra '{word}' ya existe", 'error')
    else:
        add_word(r, word, meaning)
        flash(f"Palabra agregada: {word}", 'success')
    return redirect(url_for('index'))

@app.route('/edit_word/<word>', methods=['POST'])
def edit_word_route(word):
    new_meaning = request.form['new_meaning']
    edit_word(r, word, new_meaning)
    flash(f"Palabra actualizada: {word}", 'success')
    return redirect(url_for('index'))

@app.route('/remove_word/<word>', methods=['POST'])
def remove_word_route(word):
    remove_word(r, word)
    flash(f"Palabra eliminada: {word}", 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


