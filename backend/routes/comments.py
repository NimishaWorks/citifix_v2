from flask import Blueprint, request, jsonify
from database import conn
from utils.auth_middleware import token_required

comments_bp = Blueprint('comments', __name__)
@comments_bp.route('/comments', methods=['POST'])
@token_required
def add_comment():

    try:

        data = request.get_json()

        issue_id = data.get("issue_id")
        comment = data.get("comment")

        # Get user_id from JWT token
        user_id = request.user["user_id"]

        if not issue_id or not comment:
            return jsonify({
                "message": "Issue ID and Comment are required"
            }), 400

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO comments
            (issue_id, user_id, comment)
            VALUES (%s, %s, %s)
        """, (
            issue_id,
            user_id,
            comment
        ))

        conn.commit()

        cursor.close()

        return jsonify({
            "message": "Comment added successfully"
        }), 201

    except Exception as e:
        conn.rollback()
        return jsonify({
            "error": str(e)
        }), 500
@comments_bp.route('/comments/<int:issue_id>', methods=['GET'])    
def get_comments(issue_id):

    try:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                issue_id,
                user_id,
                comment,
                created_at
            FROM comments
            WHERE issue_id = %s
            ORDER BY created_at DESC
        """, (issue_id,))

        comments = cursor.fetchall()

        cursor.close()

        result = []

        for comment in comments:

            result.append({
                "id": comment[0],
                "issue_id": comment[1],
                "user_id": comment[2],
                "comment": comment[3],
                "created_at": str(comment[4])
            })

        return jsonify(result), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500    
    
@comments_bp.route('/comments/count/<int:issue_id>', methods=['GET'])
def get_comment_count(issue_id):

    try:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM comments
            WHERE issue_id = %s
        """, (issue_id,))

        count = cursor.fetchone()[0]

        cursor.close()

        return jsonify({
            "issue_id": issue_id,
            "comments": count
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500