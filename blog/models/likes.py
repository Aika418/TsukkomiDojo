#お気に入り機能
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# いいね情報をデータベースに保存
@app.route('/like', methods=['POST'])
def like():
    content_id = request.json.get('content_id')
    user_id = request.json.get('user_id')

    conn = sqlite3.connect('likes.db')
    cursor = conn.cursor()

    # いいね情報をデータベースに挿入
    cursor.execute('INSERT INTO likes (content_id, user_id) VALUES (?, ?)', (content_id, user_id))

    conn.commit()
    conn.close()

    return jsonify({'message': 'いいねが成功しました！'})

# コンテンツごとのいいね数を取得
@app.route('/likes/<int:content_id>', methods=['GET'])
def get_likes(content_id):
    conn = sqlite3.connect('likes.db')
    cursor = conn.cursor()

    # コンテンツごとのいいね数を取得
    cursor.execute('SELECT COUNT(*) FROM likes WHERE content_id = ?', (content_id,))
    likes_count = cursor.fetchone()[0]

    conn.close()

    return jsonify({'content_id': content_id, 'likes_count': likes_count})

if __name__ == '__main__':
    app.run(debug=True)
