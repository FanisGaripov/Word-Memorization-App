# very simply program for learning english words faster (and other languages)
import random
from flask import Flask, render_template, request, session, redirect


app = Flask(__name__)
app.secret_key = 'supersecretkey'


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'words_history' not in session:
        session['words_history'] = []
    if request.method == 'POST':
        user_input = request.form['user_input']
        word_translate = request.form['word_translate']
        session['words_history'].append(user_input)
        session['words_history'].append(word_translate)
        session.modified = True
        return render_template('index.html', user_input=user_input, words_list=session['words_history'])
    return render_template('index.html', user_input=None, words_list=session['words_history'])


@app.route('/clear')
def clear():
    session['words_history'] = []
    if 'previous_word_eng' in session:
        del session['previous_word_eng']
    if 'previous_word_rus' in session:
        del session['previous_word_rus']
    return redirect('/')


@app.route('/yandex_bde153881c2a5c78.html')
def ya():
    return render_template('yandex_bde153881c2a5c78.html')


@app.route('/to-learn', methods=['GET', 'POST'])
def to_learn():
    answer_res = ''
    if len(session['words_history']) < 4:
        return render_template('to_learn.html', random_word_eng=None,
                               random_word_rus=None, answer_res=answer_res)
    if 'previous_word_eng' not in session or 'previous_word_rus' not in session:
        random_number = random.randint(0, int(len(session['words_history']) - 1))
        while random_number % 2 != 0:
            random_number = random.randint(0, int(len(session['words_history']) - 1))
        session['previous_word_eng'] = session['words_history'][random_number]
        session['previous_word_rus'] = session['words_history'][random_number + 1]
    if request.method == 'POST':
        user_answer = request.form['user_answer']
        if session['previous_word_rus'].lower() == user_answer.lower():
            answer_res = 'YES, you are right!'
            print(answer_res)
        else:
            answer_res = f'NO, {session["previous_word_eng"]} - {session["previous_word_rus"]}'
            print(answer_res)
        random_number = random.randint(0, int(len(session['words_history']) - 1))
        while random_number % 2 != 0:
            random_number = random.randint(0, int(len(session['words_history']) - 1))
        session['previous_word_eng'] = session['words_history'][random_number]
        session['previous_word_rus'] = session['words_history'][random_number + 1]

    return render_template('to_learn.html', random_word_eng=session['previous_word_eng'], random_word_rus=session['previous_word_rus'], answer_res=answer_res)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
