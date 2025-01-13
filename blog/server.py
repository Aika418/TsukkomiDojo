# Blueprint（pyファイルを分割するための関数）をインポート
from flask import Blueprint

#「app」を「Blueprint()」を使って定義
#「blog」の部分は、url_for("blog.top")で使用
app = Blueprint('blog', __name__, template_folder='templates')


# 必要なモジュールをインポート
import os
from datetime import datetime, timedelta, timezone
from flask import Flask, session, redirect, url_for, render_template,request
#「/blog/models/models.py」の「WikiContent」と「User」を呼び出す
from blog.models.models import WikiContent,User
#「/blog/models/database.py」の「db_session」を呼び出す
from blog.models.database import db_session

from werkzeug.utils import secure_filename

@app.route('/like/<ID>', methods=['post'])
def like(ID):
    if "user_name" not in session:
        return redirect(url_for("blog.top", status="not_logged_in"))
    
    user_name = session["user_name"]
    user = User.query.filter_by(user_name=user_name).first()
    diary = WikiContent.query.get(ID)

    if not user or not diary:
        return redirect(url_for("blog.index"))

    if diary in user.liked_posts:
        # いいね解除
        user.liked_posts.remove(diary)
        diary.likes -= 1
    else:
        # いいね追加
        user.liked_posts.append(diary)
        diary.likes += 1

    db_session.commit()
    return redirect(url_for("blog.index"))



@app.route("/mypage")
def mypage():
    # セッションからユーザー名を取得
    name = session.get("user_name", "")  # セッションがない場合は空文字を返す
    status = request.args.get("status")

    user = User.query.filter_by(user_name=name).first()
    liked_posts = user.liked_posts if user else []

    return render_template("blog/mypage.html", name=name, status=status, liked_posts=liked_posts)


#「/」へアクセスがあった場合
@app.route('/')
def index():  # 一覧画面
    if "user_name" in session:
        # セッションがログイン状態であれば「blog/index.html」を返す
        name = session["user_name"]
        all_diary= WikiContent.query.all()
        search = ""
        return render_template('blog/index.html',name=name, all_diary=all_diary,search=search)
    else:
        # ログイン状態でなければ「/blog/top」ページへ移動
        return redirect(url_for("blog.top"))

#「/logout」へアクセスがあった場合「/blog/top」ページへ移動
@app.route('/logout')
def logout():
    session.pop("user_name", None)
    return redirect(url_for("blog.top",status="logout"))

#「/create」へアクセスがあった場合「blog/edit.html」を返す
@app.route('/create')
def create():  #新規作成
    name = session["user_name"]
    return render_template('blog/edit.html',name=name)


#「/diary/<ID>」へアクセスがあった場合「blog/diary.html」を返す
@app.route('/diary/<ID>')
def diary(ID):  #参照
    name = session["user_name"]
    diary = WikiContent.query.get(ID)
    return render_template('blog/diary.html',name=name,diary=diary)


#「/diarysave」へアクセスがあった場合「/blog/index」ページへ移動
@app.route('/diarysave', methods=['post'])
def diarysave():  #保存
    
    
    # データベースに保存
    name = name = session["user_name"]
    comment = request.form["comment"]
    # JSTタイムゾーンを作成
    jst = timezone(timedelta(hours=9), 'JST')
    date = datetime.now(jst)
    content = WikiContent(name,comment,date)
    db_session.add(content)
    db_session.commit()
    return redirect(url_for("blog.index"))



#「/diaryupdate」へアクセスがあった場合「/blog/index」ページへ移動
@app.route('/diaryupdate', methods=['post'])
def diaryupdate():  #更新
    content = WikiContent.query.get(request.form.get("ID"))
    
    # データベースを更新
    
    content.comment = request.form["comment"]
    db_session.commit()
    return redirect(url_for("blog.index"))


#「/delete/<ID>」へアクセスがあった場合「/blog/index」ページへ移動
@app.route('/delete/<ID>')
def delete(ID):  #削除
    content = WikiContent.query.get(ID)
    db_session.delete(content)
    db_session.commit()
    return redirect(url_for("blog.index"))


@app.route('/all_delete')
def all_delete():  #全削除
    WikiContent.query.delete()
    db_session.commit()
    return redirect(url_for("blog.index"))


#「/search」へアクセスがあった場合「blog/index.html」を返す
@app.route('/search', methods=['post'])
def search():  # 検索
    name = session["user_name"]
    all_diary= WikiContent.query.all()
    search = request.form["search"]
    return render_template('blog/index.html',name=name, all_diary=all_diary,search=search)


# top
#「/login」へアクセスがあった場合
@app.route("/login",methods=["post"])
def login():
    # 入力された「ユーザー名」が既に存在するか確認
    user_name = request.form["user_name"]
    user = User.query.filter_by(user_name=user_name).first()
    if user:
        #「ユーザー名」が存在した場合
        #「パスワード」が一致するか確認（「key.SALT」で暗号化）
        password = request.form["password"]
        
        if user.password == password:
            #「パスワード」が一致した場合「/blog/index」ページへ移動
            session["user_name"] = user_name
            return redirect(url_for("blog.index"))
        else:
            #「パスワード」が一致しない場合「/blog/top」ページへ移動
            return redirect(url_for("blog.top",status="wrong_password"))
    else:
        #「ユーザー名」が存在しなかった場合「/blog/top」ページへ移動
        return redirect(url_for("blog.top",status="user_notfound"))

#「/registar」へアクセスがあった場合
# 新規登録画面で「新規登録」ボタンが押された時
@app.route("/registar",methods=["post"])
def registar():
    # 入力された「ユーザー名」が既に存在するか確認
    user_name = request.form["user_name"]
    user = User.query.filter_by(user_name=user_name).first()
    if user:
        #「ユーザー名」が存在した場合「/blog/newcomer」ページへ移動
        return redirect(url_for("blog.newcomer",status="exist_user"))
    else:
        
        password = request.form["password"]
        
        user = User(user_name, password)
        # データベースに追加して保存
        db_session.add(user)
        db_session.commit()
        session["user_name"] = user_name
        #「/blog/index」ページへ移動
        return redirect(url_for("blog.index"))

#「/top」へアクセスがあった場合「blog/top.html」を返す
@app.route("/top")
def top():
    status = request.args.get("status")
    return render_template("blog/top.html",status=status)




#「/newcomer」へアクセスがあった場合「blog/newcomer.html」を返す
@app.route("/newcomer")
def newcomer():
    status = request.args.get("status")
    return render_template("blog/newcomer.html",status=status)


