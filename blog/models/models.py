from sqlalchemy import Column, Integer, String, Text, DateTime
#from models.database import Base       # データベースの初期化用
from blog.models.database import Base   # 初期化が終わればこちらへ変更
from datetime import datetime
 
 
class WikiContent(Base):
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