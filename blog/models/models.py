from sqlalchemy import Column, Integer, String, Text, DateTime
#from models.database import Base       # データベースの初期化用
from blog.models.database import Base   # 初期化が終わればこちらへ変更
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
 
class WikiContent(Base):　#ユーザーの名前とコメントを保持するテーブル
    __tablename__ = 'wikicontents'
    id = Column(Integer, primary_key=True)
    user = Column(String(128))
    comment = Column(Text)
    
    date = Column(DateTime, default=datetime.now())
 
    def __init__(self, user=None, comment=None, date=None):
        self.user = user
        self.comment = comment
        self.date = date
 

 
#Userクラスを追加。WikiContentの使い回し
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_name = Column(String(128))
    password = Column(String(128))
 
    def __init__(self, user_name=None, password=None):
        self.user_name = user_name
        self.password = password
 
    def __repr__(self):
        return '<Name %r>' % (self.user_name)


class Post(db.Model):　#投稿情報の管理。いいね数カウントのやつ。
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False) #投稿のタイトル
    content = Column(String, nullable=False) #内容
    like_count = Column(Integer, default=0) #いいねカウント


    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120),nullable = False)

def like_post(post_id):
    # ログインしているユーザーの情報
    user = current_user

    # 投稿を取得
    post = Post.query.get_or_404(post_id)

    # ユーザーがすでにこの投稿にいいねをしているかを確認
    existing_like = Like.query.filter_by(user_id=user.id, post_id=post.id).first()
    if not existing_like:
        # まだいいねしていなければ新しい「いいね」を追加
        new_like = Like(user_id=user.id, post_id=post.id)
        db.session.add(new_like)
        post.like_count += 1  # いいね数を増加
        db.session.commit()

    return jsonify({"like_count": post.like_count})


#ユーザーがどの投稿にいいねしたかの中間テーブル
class Like(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, db.ForeignKey('post.id'), nullable=False)

    user = db.relationship('User', backref='likes')
    post = db.relationship('Post', backref='likes')


