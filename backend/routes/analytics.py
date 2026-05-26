from flask import Blueprint, jsonify
from database import conn
from utils.auth_middleware import token_required

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics', methods=['GET'])
@token_required
def get_analytics():

    try:

        cursor = conn.cursor()

        # Total Issues
        cursor.execute("""
            SELECT COUNT(*)
            FROM issues
        """)
        total_issues = cursor.fetchone()[0]

        # Reported Issues
        cursor.execute("""
            SELECT COUNT(*)
            FROM issues
            WHERE status = 'Reported'
        """)
        reported = cursor.fetchone()[0]

        # In Progress Issues
        cursor.execute("""
            SELECT COUNT(*)
            FROM issues
            WHERE status = 'In Progress'
        """)
        in_progress = cursor.fetchone()[0]

        # Resolved Issues
        cursor.execute("""
            SELECT COUNT(*)
            FROM issues
            WHERE status = 'Resolved'
        """)
        resolved = cursor.fetchone()[0]

        # Total Comments
        cursor.execute("""
            SELECT COUNT(*)
            FROM comments
        """)
        total_comments = cursor.fetchone()[0]

        # Total Votes
        cursor.execute("""
            SELECT COUNT(*)
            FROM votes
        """)
        total_votes = cursor.fetchone()[0]

        cursor.close()

        return jsonify({
            "total_issues": total_issues,
            "reported": reported,
            "in_progress": in_progress,
            "resolved": resolved,
            "total_comments": total_comments,
            "total_votes": total_votes
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500
    
@analytics_bp.route('/analytics/types', methods=['GET'])
@token_required
def issue_type_analytics():

    try:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT type, COUNT(*)
            FROM issues
            GROUP BY type
            ORDER BY COUNT(*) DESC
        """)

        data = cursor.fetchall()

        cursor.close()

        result = {}

        for row in data:
            result[row[0]] = row[1]

        return jsonify(result), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500    
    
@analytics_bp.route('/analytics/top-issues', methods=['GET'])
@token_required
def top_issues():

    try:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                issues.id,
                issues.title,
                COUNT(votes.id) AS vote_count
            FROM issues
            LEFT JOIN votes
                ON issues.id = votes.issue_id
            GROUP BY issues.id, issues.title
            ORDER BY vote_count DESC
            LIMIT 10
        """)

        data = cursor.fetchall()

        cursor.close()

        result = []

        for row in data:

            result.append({
                "issue_id": row[0],
                "title": row[1],
                "votes": row[2]
            })

        return jsonify(result), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500   