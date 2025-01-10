# initialize_database.py
#db初期化用ファイル
from blog.models.database import Base, engine
from blog.models.models import User, WikiContent

# テーブルを再作成
def reset_database():
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating new tables...")
    Base.metadata.create_all(bind=engine)
    print("Database initialization complete.")

if __name__ == "__main__":
    reset_database()

