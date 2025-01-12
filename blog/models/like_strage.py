#モデルをインポート
from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_required
from blog.models.models import db, Post

app = Flask(__name__)
#フラスクでエンドポイント？を作る。ネットにつながっている方

@app.route('/like/<int:post_id>', methods=['POST'])
def like_post(post_id):

    post = Post.query.get(post_id)  # 投稿をIDで検索

    #if not post:
        #return jsonify({"message": "投稿が見つかりません"}), 404
    if post:
        post.like_count += 1  # いいね数を1増やす
        db.session.commit()  # データベースに保存

        #return redirect(url_for('index')) #使用例: 例えば、データベースにいいねを保存した後、ユーザーを別のページ（たとえば、トップページや投稿一覧ページなど）にリダイレクトさせたい場合に使用

        return jsonify({"message": "いいねしました！", "like_count": post.like_count}), 200 #いいねボタンを押した際に、ページ遷移せずに現在の「いいね」数をリアルタイムで更新したい場合に使用

    if __name__ == "__main__"
        app.run()


@app.route('/blog/diaryupdate', methods=['POST'])
def update_diary():
    #日記の更新処理
    pass
