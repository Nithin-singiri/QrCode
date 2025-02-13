from flask import Flask, request, render_template, jsonify
import sqlite3

app = Flask(__name__)

# Connect to the database
DB_PATH = "qr_usage.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Route for the home page
@app.route("/")
def index():
    return render_template("index.html")

# API to check QR code
@app.route("/scan", methods=["POST"])
def scan_qr():
    qr_data = request.json.get("qr_data", "").strip()
    
    if not qr_data:
        return jsonify({"status": "error", "message": "Invalid QR code"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the QR code exists in the database
    cursor.execute("SELECT * FROM qr_status WHERE paper_id = ?", (qr_data,))
    record = cursor.fetchone()

    if record:
        if record["scanned"] == 0:
            # First-time scan, update the database
            cursor.execute("UPDATE qr_status SET scanned = 1 WHERE paper_id = ?", (qr_data,))
            conn.commit()

            # Fetch details
            cursor.execute("SELECT * FROM members WHERE paper_id = ?", (qr_data,))
            member = cursor.fetchone()

            conn.close()
            if member:
                return jsonify({"status": "success", "message": "QR code scanned successfully", "data": dict(member)})
            else:
                return jsonify({"status": "error", "message": "No details found"})

        else:
            conn.close()
            return jsonify({"status": "used", "message": "QR code already used"})
    else:
        conn.close()
        return jsonify({"status": "error", "message": "Invalid QR code"})

if __name__ == "__main__":
    app.run(debug=True)