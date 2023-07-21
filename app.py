from openAi import generate_more, generate_questions, generate_summary
from markupsafe import escape
from flask import Flask, render_template, request, session
import json
import os


data_file = os.path.join('.', 'article.json')
with open(data_file, 'r') as f:
    savedArticleData = json.load(f)
data_file = os.path.join('.', 'questions.json')
with open(data_file, 'r') as f:
    savedQuestionsData = json.load(f)
getStaticData = False

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'


@app.route('/start/')
@app.route('/start/<book>')
def hello(book=None):
    return render_template('start.html', book=book)


@app.route('/article', methods=['POST', 'GET'])
def article():
    articleInfo = dict(base=0)

    if request.method == 'POST':
        book = request.form
        articleInfo['bookTitle'] = book['book']

        # Here you call OpenAI!

        if getStaticData:
            articleInfo['article'] = savedArticleData
        else:
            article = generate_summary(articleInfo)
            # print(article)
            articleInfo['article'] = json.loads(article)

        if getStaticData:
            articleInfo['questions'] = savedQuestionsData
        else:
            articleQuestions = generate_questions(articleInfo)
            try:
                articleInfo['questions'] = json.loads(articleQuestions)
            except:
                articleInfo['questions'] = articleQuestions

        session['articleInfo'] = articleInfo
        return render_template("article.html",
                               book=book,
                               article=articleInfo['article'],
                               questions=articleInfo['questions'])


@app.route('/more/<title>')
@app.route('/more')
def more(title="Error"):
    (para, answers) = generate_more(title, session['articleInfo'])
    print(para)
    print(answers)
    para = json.loads(para,strict=False)
    answers = json.loads(answers, strict=False)

    return render_template("more.html",
                           title=title,
                           para=para,
                           answers=answers)


if __name__ == '__main__':
    app.run(debug=True)
