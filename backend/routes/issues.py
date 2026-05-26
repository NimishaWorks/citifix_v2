from flask import Blueprint, request, jsonify
from database import conn
from utils.auth_middleware import token_required
from utils.auth_middleware import admin_required
issues_bp = Blueprint('issues', __name__)
@issues_bp.route('/test-issue')
def test_issue():
    return "Issue route working"
@issues_bp.route('/issues', methods=['POST'])
@token_required
def create_issue():

    try:

        data = request.get_json()

        title = data.get("title")
        description = data.get("description")
        issue_type = data.get("type")
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        location = data.get("location")
        image = data.get("image")
        status = data.get("status", "Reported")
        user_id = request.user["user_id"]

        if not title or not description:
            return jsonify({
                "message": "Title and Description are required"
            }), 400

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO issues
            (
                title,
                description,
                type,
                latitude,
                longitude,
                location,
                image,
                status,
                user_id
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            title,
            description,
            issue_type,
            latitude,
            longitude,
            location,
            image,
            status,
            user_id
        ))

        conn.commit()

        cursor.close()

        return jsonify({
            "message": "Issue created successfully"
        }), 201

    except Exception as e:
        conn.rollback()
        return jsonify({
            "error": str(e)
        }), 500
@issues_bp.route('/issues', methods=['GET'])
def get_issues():

    try:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                title,
                description,
                type,
                latitude,
                longitude,
                location,
                image,
                status,
                user_id
            FROM issues
            ORDER BY id DESC
        """)

        issues = cursor.fetchall()

        cursor.close()

        result = []

        for issue in issues:

            result.append({
                "id": issue[0],
                "title": issue[1],
                "description": issue[2],
                "type": issue[3],
                "latitude": issue[4],
                "longitude": issue[5],
                "location": issue[6],
                "image": issue[7],
                "status": issue[8],
                "user_id": issue[9]
            })

        return jsonify(result), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500
@issues_bp.route('/issues/<int:issue_id>', methods=['PUT'])
def update_issue(issue_id):

    try:
        data=request.get_json()
        status=data.get("status")
        if not status:
            return jsonify(
                {
                    "message":"Status is required"
                }
            ),400
        cursor=conn.cursor()
        cursor.execute(""" 
           UPDATE issues
                       SET status=%s
                       where id=%s
                       """,(status,issue_id))
        conn.commit()
        if cursor.rowcount==0:
            cursor.close()
            return jsonify({
                "message":"Issue not found"
            }),404
        cursor.close()
        return jsonify({
            "message":"Issue status updated successfully"
        }),200
    except Exception as e:
        conn.rollback()
        return jsonify({
            "error":str(e)
        }),500
    
@issues_bp.route('/issues/<int:issue_id>', methods=['DELETE'])
@admin_required
def delete_issue(issue_id):

    try:

        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM issues
            WHERE id = %s
        """, (issue_id,))

        conn.commit()

        if cursor.rowcount == 0:
            cursor.close()

            return jsonify({
                "message": "Issue not found"
            }), 404

        cursor.close()

        return jsonify({
            "message": "Issue deleted successfully"
        }), 200

    except Exception as e:
        conn.rollback()
        return jsonify({
            "error": str(e)
        }), 500
    
@issues_bp.route('/my-issues/<int:user_id>', methods=['GET'])
@token_required
def get_my_issues(user_id):

    try:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                title,
                description,
                type,
                status
            FROM issues
            WHERE user_id = %s
            ORDER BY id DESC
        """, (user_id,))

        issues = cursor.fetchall()

        cursor.close()

        result = []

        for issue in issues:

            result.append({
                "id": issue[0],
                "title": issue[1],
                "description": issue[2],
                "type": issue[3],
                "status": issue[4]
            })

        return jsonify(result), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500 
@issues_bp.route(
    "/issues/<int:issue_id>/status",
    methods=["PUT"]
)
@token_required
def update_status(issue_id):

    try:

        data =request.get_json()

        status = data.get("status")

        cursor =conn.cursor()

        cursor.execute("""
            UPDATE issues
            SET status = %s
            WHERE id = %s
        """, (
            status,
            issue_id
        ))

        conn.commit()

        cursor.close()

        return jsonify({
            "message":
            "Status updated"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500     