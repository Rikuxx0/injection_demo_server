from flask import Flask, request
import sqlite3
import subprocess
import xml.etree.ElementTree as ET

app = Flask(__name__)

# DB初期化
def init_db():
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'adminpass')")
    conn.commit()
    conn.close()

@app.route("/")
def index():
    return "Injection Demo Server is running."

@app.route('/xss', methods=['GET'])
def xss_test():
    user_input = request.args.get('input', '')
    return f"<html><body>結果: {user_input}</body></html>"

@app.route("/sql")
def sql():
    username = request.args.get("user", "")
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    try:
        query = f"SELECT * FROM users WHERE username = '{username}'"
        cursor.execute(query)
        result = cursor.fetchall()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@app.route("/cmd")
def cmd():
    filename = request.args.get("filename", "")
    try:
        output = subprocess.check_output(f"ls {filename}", shell=True, stderr=subprocess.STDOUT)
        return output.decode()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.decode()}"

@app.route("/xxe", methods=["POST"])
def xxe():
    xml = request.data.decode()
    try:
        ET.fromstring(xml)  # XXEが効くようなパーサではない（デモ用に表示だけ）
        return "Parsed successfully"
    except Exception as e:
        return f"XML Parse Error: {str(e)}"

@app.route("/ldap")
def ldap():
    user = request.args.get("user", "")
    return f"LDAP search for user: ({user})"  # 実処理は行わない模擬

if __name__ == "__main__":
    init_db()
    app.run(debug=True)