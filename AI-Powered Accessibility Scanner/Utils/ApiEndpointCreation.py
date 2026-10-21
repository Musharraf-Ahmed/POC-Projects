from flask import Flask, request, jsonify
import psycopg2
def CreateApiEndpoint():
    app = Flask(__name__)

    conn = psycopg2.connect(
        host="postgres",
        database="Accessibility_Data",
        user="postgres",
        password="Mprsnl2026"
    )


    @app.route('/violations', methods=['POST'])
    def create_violation():

        data = request.json

        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO accessibility_violations
            (
                page_url,
                rule_id,
                impact,
                description,
                scan_date,
                ai_analysis
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                data['page_url'],
                data['rule_id'],
                data['impact'],
                data['description'],
                data['scan_date'],
                data['ai_analysis']
            )
        )

        violation_id = cur.fetchone()[0]

        conn.commit()
        cur.close()

        return jsonify({
            "id": violation_id,
            "message": "Violation Saved"
        }), 201


    @app.route('/violations', methods=['GET'])
    def get_violations():

        cur = conn.cursor()

        cur.execute("""
            SELECT
                id,
                page_url,
                rule_id,
                impact,
                description,
                scan_date,
                ai_analysis
            FROM accessibility_violations
        """)

        rows = cur.fetchall()

        violations = []

        for row in rows:
            violations.append({
                "id": row[0],
                "page_url": row[1],
                "rule_id": row[2],
                "impact": row[3],
                "description": row[4],
                "scan_date": str(row[5]),
                "ai_analysis": row[6]
            })

        cur.close()

        return jsonify(violations)
    app.run(
    host="127.0.0.1",
    port=5000,
    debug=False,
    use_reloader=False)