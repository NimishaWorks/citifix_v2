from flask import Blueprint, request, jsonify
from database import conn
from utils.auth_middleware import token_required

votes_bp = Blueprint('votes', __name__)

@votes_bp.route('/vote', methods=['POST'])
@token_required
def add_vote():

    try:

        data = request.get_json()

        issue_id = data.get("issue_id")

        # Get user_id from JWT token
        user_id = request.user["user_id"]

        if not issue_id:
            return jsonify({
                "message": "Issue ID is required"
            }), 400

        cursor = conn.cursor()

        cursor.execute("""
            SELECT id
            FROM votes
            WHERE issue_id = %s
            AND user_id = %s
        """, (
            issue_id,
            user_id
        ))

        existing_vote = cursor.fetchone()

        if existing_vote:

            cursor.close()

            return jsonify({
                "message": "You have already voted for this issue"
            }), 409

        cursor.execute("""
            INSERT INTO votes
            (issue_id, user_id)
            VALUES (%s, %s)
        """, (
            issue_id,
            user_id
        ))

        conn.commit()

        cursor.close()

        return jsonify({
            "message": "Vote added successfully"
        }), 201

    except Exception as e:
        conn.rollback()
        return jsonify({
            "error": str(e)
        }), 500
@votes_bp.route('/issues/<int:issue_id>/votes',methods=['GET'])  
def get_vote_count(issue_id):

    try:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM votes
            WHERE issue_id = %s
        """, (issue_id,))

        count = cursor.fetchone()[0]

        cursor.close()

        return jsonify({
            "issue_id": issue_id,
            "votes": count
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500