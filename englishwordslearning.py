# very simply program for learning english words faster (and other languages)
import random
from flask import Flask, render_template, request, session, redirect


app = Flask(__name__)
app.secret_key = 'supersecretkey'
learned = []

@app.route('/add-words', methods=['GET', 'POST'])
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


@app.route('/')
def main():
    if 'words_history' in session:
        return render_template('main.html', words_history=session['words_history'])
    else:
        return render_template('main.html', words_history=None)


@app.route('/clear')
def clear():
    session['words_history'] = []
    if 'previous_word_eng' in session:
        del session['previous_word_eng']
    if 'previous_word_rus' in session:
        del session['previous_word_rus']
    if "count" in session:
        del session["count"]
    if "right" in session:
        del session["right"]
    if "mode" in session:
        del session["mode"]
    return redirect('/add-words')


@app.route('/yandex_bde153881c2a5c78.html')
def ya():
    return render_template('yandex_bde153881c2a5c78.html')


@app.route('/to-learn', methods=['GET', 'POST'])
def to_learn():
    answer_res = ''
    if "count" not in session or "right" not in session:
        session["count"] = 0
        session["right"] = 0

    if "mode" not in session:
        session["mode"] = "en_to_ru"  # Режим: "en_to_ru" или "ru_to_en"

    if request.method == 'POST' and 'change_mode' in request.form:
        session["mode"] = "ru_to_en" if session["mode"] == "en_to_ru" else "en_to_ru"
        session.modified = True
        return redirect('/to-learn')

    if len(session['words_history']) < 4:
        return render_template('to_learn.html', random_word_eng=None,
                               random_word_rus=None, answer_res=answer_res,
                               count=session["count"], right=session["right"],
                               progress=0, mode=session["mode"])

    if 'previous_word_eng' not in session or 'previous_word_rus' not in session:
        random_number = random.randint(0, int(len(session['words_history']) - 1))
        while random_number % 2 != 0:
            random_number = random.randint(0, int(len(session['words_history']) - 1))
        session['previous_word_eng'] = session['words_history'][random_number]
        session['previous_word_rus'] = session['words_history'][random_number + 1]

    if request.method == 'POST' and 'user_answer' in request.form:
        user_answer = request.form['user_answer']
        if session["mode"] == "en_to_ru":
            if session['previous_word_rus'].lower() == user_answer.lower():
                answer_res = 'YES, you are right!'
                session["right"] += 1
            else:
                answer_res = f'NO, {session["previous_word_eng"]} - {session["previous_word_rus"]}'
        else:
            if session['previous_word_eng'].lower() == user_answer.lower():
                answer_res = 'YES, you are right!'
                session["right"] += 1
            else:
                answer_res = f'NO, {session["previous_word_rus"]} - {session["previous_word_eng"]}'
        session["count"] += 1

        random_number = random.randint(0, int(len(session['words_history']) - 1))
        while random_number % 2 != 0:
            random_number = random.randint(0, int(len(session['words_history']) - 1))
        session['previous_word_eng'] = session['words_history'][random_number]
        session['previous_word_rus'] = session['words_history'][random_number + 1]

    return render_template('to_learn.html', random_word_eng=session['previous_word_eng'],
                           random_word_rus=session['previous_word_rus'], answer_res=answer_res,
                           count=session["count"], right=session["right"], mode=session["mode"])


@app.route('/clear-stat', methods=['POST'])
def clear_stat():
    if "count" in session:
        del session["count"]
    if "right" in session:
        del session["right"]
    return redirect('/to-learn')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
else:
    print('Запускай файл englishwordslearning.py')