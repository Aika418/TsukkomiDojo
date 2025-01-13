from sqlalchemy import Column, Integer, String, Text, DateTime,Table, ForeignKey
#from models.database import Base       # データベースの初期化用
from blog.models.database import Base   # 初期化が終わればこちらへ変更
from datetime import datetime
from sqlalchemy.orm import relationship
 
 #中間テーブルの定義
likes_table = Table(
    'likes', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('wikicontent_id', Integer, ForeignKey('wikicontents.id'))
)
 
class WikiContent(Base):
    __tablename__ = 'wikicontents'
    id = Column(Integer, primary_key=True)
    user = Column(String(128))
    comment = Column(Text)
    likes = Column(Integer, default=0)  # いいね数を保持するカラム
    liked_by = relationship("User", secondary=likes_table, back_populates="liked_posts")
    date = Column(DateTime, default=datetime.now())

 
    def __init__(self, user=None, comment=None, date=None,likes=0):
        self.user = user
        self.comment = comment
        self.likes = likes
        self.date = date
 

 
#Userクラスを追加。WikiContentの使い回し
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_name = Column(String(128))
    password = Column(String(128))
    liked_posts = relationship("WikiContent", secondary=likes_table, back_populates="liked_by")
 
    def __init__(self, user_name=None, password=None):
        self.user_name = user_name
        self.password = password
 
    def __repr__(self):
        return '<Name %r>' % (self.user_name)