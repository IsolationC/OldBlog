from flask import Flask, render_template, request, session, redirect, jsonify
import db


app = Flask(__name__)
app.config.from_object('config')


@app.route('/')
def index():
    sql = "select * from t_article_type"
    results = db.query_all(sql, ())
    return render_template('index.html', types=results)


@app.route('/regist', methods=['POST', 'GET'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        confirmPass = request.form.get('confirmPass')
        sex = request.form.get('sex')
        email = request.form.get('email')

        if username == "":
            return render_template('regist.html', error="用户名为空")
        if password != confirmPass:
            return render_template('regist.html', error2="两次密码不同")

        sql = "insert into t_user(username, password, sex, email) value(%s, %s, %s, %s)"
        row = db.update(sql, (username, password, sex, email))
        if row > 0:
            return redirect('/')
        else:
            return '失败。。'


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
    else:
        return render_template('login.html')

    sql = "select * from t_user where username=%s and password=%s"
    result = db.query(sql, (username, password))
    session['username'] = username
    if result:
        return redirect('/')
    else:
        return '登录名或密码错误'


@app.route('/check_name')
def checked_name():
    name = request.args.get('uname')
    result = db.query('select * from t_user where username=%s', (name))

    if result:
        return 'fail'
    else:
        return 'success'


@app.route('/get_articles')
def get_articles():
    page_no = int(request.args.get('pageNo'))

    sql = "select art.*, type.type_name " \
          "from t_article art, t_article_type type " \
          "where art.type_id = type.type_id " \
          "limit %s,3"

    results = db.query_all(sql, (page_no * 3))
    return jsonify(results)


@app.route('/list_article')
def list_article():
    type_id = request.args.get('typeId')

    sql1 = "select * from t_article_type"
    results = db.query_all(sql1, ())

    sql = "select art.*, type.type_name " \
          "from t_article art, t_article_type type " \
          "where art.type_id = type.type_id "

    if type_id:
        sql += 'and type.type_id=%s'

    articles = db.query_all(sql, (type_id) if type_id else ())
    return render_template('list_article.html', types=results, articles=articles)


@app.route('/article')
def article():
    article_id = request.args.get('articleId')

    sql1 = "select art.*, type.type_name " \
           "from t_article art, t_article_type type " \
           "where art.type_id = type.type_id and art.article_id=%s"

    sql2 = "select comm.*, usr.username,usr.portrait " \
           "from t_comment comm, t_user usr " \
           "where comm.user_id=usr.user_id and comm.article_id = %s"

    result = db.query(sql1, (article_id))
    results = db.query_all(sql2, (article_id))

    return render_template('article.html', comments=results, article=result)


@app.route('/check_login')
def check_login():
    username = session.get('username')
    if username:
        return 'ok'
    else:
        return 'forbid'


@app.route('/mgr_articles')
def mgr_articles():
    sql = 'select art.*, type.type_name ' \
          'from t_article art, t_article_type type ' \
          'where art.type_id=type.type_id '
    results = db.query_all(sql)
    return render_template('mgr_articles.html', articles=results)


@app.route('/delete_article')
def delete_article():
    article_id = request.args.get('articleId')
    row = db.update('delete from t_article where article_id=%s', (article_id))
    if row > 0:
        return redirect('/mgr_articles')
    else:
        return '删除失败'


@app.route('/delete_articles')
def delete_articles():
    article_ids = request.args.get('articleIds')
    sql = "delete from t_article where article_id in("+article_ids+")"
    row = db.update(sql, ())
    if row > 0:
        return 'ok'
    else:
        return 'notok'


@app.route('/comment', methods=['POST', 'GET'])
def comment():
    new_comment = request.form.get('new_comment')
    article_id = request.args.get('articleId')
    username = session.get('username')
    sql1 = "select user_id from t_user where username=%s"
    user_id = db.query(sql1, (username))

    sql = "insert into t_comment(content, user_id, article_id) value(%s, %s, %s)"
    row = db.update(sql, (new_comment, user_id['user_id'], article_id))
    if row > 0:
        return 'ok'
    else:
        return 'notok'


if __name__ == '__main__':
    app.run()
