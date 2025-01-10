import sys
import os

# プロジェクトのルートディレクトリをモジュール検索パスに追加
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from blog.models.database import init_db

# データベースの初期化
if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")
