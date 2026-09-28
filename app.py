import sqlite3
from flask import Flask, request, jsonify, session, send_from_directory, g

app = Flask(__name__, static_folder="static", static_url_path="/static")
app.secret_key = "change-this-secret"
DB = "court.db"
ADMIN = ("admin", "admin123")

# table: (primary key, editable columns)
T = {
    "court": ("co_id", ["co_name", "co_address", "co_city", "co_zipcode"]),
    "judge": ("j_id", ["j_name", "j_phone", "j_address", "co_id"]),
    "attorney": ("a_id", ["a_name", "a_email", "a_address"]),
    "client": ("c_id", ["c_fname", "c_lname", "c_address", "c_sex"]),
    "cases": ("case_id", ["case_desp", "status", "filing_date", "c_id", "a_id", "co_id"]),
    "hearing": ("h_id", ["case_id", "j_id", "hearing_date", "hearing_type", "notes"]),
    "jury": ("jury_id", ["case_id", "no_of_jurors", "verdict"]),
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS court(co_id INTEGER PRIMARY KEY AUTOINCREMENT, co_name TEXT NOT NULL, co_address TEXT, co_city TEXT, co_zipcode TEXT);
CREATE TABLE IF NOT EXISTS judge(j_id INTEGER PRIMARY KEY AUTOINCREMENT, j_name TEXT NOT NULL, j_phone TEXT, j_address TEXT, co_id INTEGER REFERENCES court(co_id));
CREATE TABLE IF NOT EXISTS attorney(a_id INTEGER PRIMARY KEY AUTOINCREMENT, a_name TEXT NOT NULL, a_email TEXT, a_address TEXT);
CREATE TABLE IF NOT EXISTS client(c_id INTEGER PRIMARY KEY AUTOINCREMENT, c_fname TEXT NOT NULL, c_lname TEXT, c_address TEXT, c_sex TEXT);
CREATE TABLE IF NOT EXISTS cases(case_id INTEGER PRIMARY KEY AUTOINCREMENT, case_desp TEXT NOT NULL, status TEXT DEFAULT 'Pending', filing_date TEXT,
  c_id INTEGER REFERENCES client(c_id), a_id INTEGER REFERENCES attorney(a_id), co_id INTEGER REFERENCES court(co_id));
CREATE TABLE IF NOT EXISTS hearing(h_id INTEGER PRIMARY KEY AUTOINCREMENT, case_id INTEGER REFERENCES cases(case_id), j_id INTEGER REFERENCES judge(j_id),
  hearing_date TEXT, hearing_type TEXT, notes TEXT);
CREATE TABLE IF NOT EXISTS jury(jury_id INTEGER PRIMARY KEY AUTOINCREMENT, case_id INTEGER REFERENCES cases(case_id), no_of_jurors INTEGER, verdict TEXT);
"""

SEED = [
    "INSERT INTO court(co_name,co_address,co_city,co_zipcode) VALUES('District Court Pune','Court Road','Pune','411001'),('District Court Belhe','Main Road','Belhe','412410')",
    "INSERT INTO judge(j_name,j_phone,j_address,co_id) VALUES('Emily Johnson','555-2345','456 Maple St',1),('David Lee','555-3456','789 Oak St',2)",
    "INSERT INTO attorney(a_name,a_email,a_address) VALUES('Rahul Patil','rahul@law.in','FC Road, Pune'),('Sneha Joshi','sneha@law.in','Belhe')",
    "INSERT INTO client(c_fname,c_lname,c_address,c_sex) VALUES('John','Smith','123 Main St','M'),('Jane','Doe','456 Maple St','F')",
    "INSERT INTO cases(case_desp,status,filing_date,c_id,a_id,co_id) VALUES('Property dispute','Pending','2026-01-10',1,1,1),('Traffic violation','Hearing','2026-02-05',2,2,2)",
    "INSERT INTO hearing(case_id,j_id,hearing_date,hearing_type,notes) VALUES(1,1,'2026-10-05','Preliminary','Initial hearing')",
]


def db():
    if "db" not in g:
        g.db = sqlite3.connect(DB)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys=ON")
    return g.db


@app.teardown_appcontext
def close(_):
    d = g.pop("db", None)
    if d:
        d.close()


def init_db():
    con = sqlite3.connect(DB)
    con.executescript(SCHEMA)
    if con.execute("SELECT COUNT(*) FROM court").fetchone()[0] == 0:
        for s in SEED:
            con.execute(s)
    con.commit()
    con.close()


@app.before_request
def guard():
    open_paths = ("/", "/api/login")
    if request.path.startswith("/api/") and request.path not in open_paths and not session.get("user"):
        return jsonify(error="Please log in"), 401


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.post("/api/login")
def login():
    d = request.get_json(force=True)
    if (d.get("username"), d.get("password")) == ADMIN:
        session["user"] = d["username"]
        return jsonify(ok=True)
    return jsonify(error="Wrong username or password"), 401


@app.post("/api/logout")
def logout():
    session.clear()
    return jsonify(ok=True)


@app.get("/api/me")
def me():
    return jsonify(user=session.get("user"))


@app.get("/api/stats")
def stats():
    q = lambda s: db().execute(s).fetchone()[0]
    return jsonify(
        cases=q("SELECT COUNT(*) FROM cases"),
        pending=q("SELECT COUNT(*) FROM cases WHERE status!='Closed'"),
        hearings=q("SELECT COUNT(*) FROM hearing WHERE hearing_date>=date('now')"),
        judges=q("SELECT COUNT(*) FROM judge"),
    )


@app.get("/api/<t>")
def list_rows(t):
    if t not in T:
        return jsonify(error="Unknown table"), 404
    rows = db().execute(f"SELECT * FROM {t} ORDER BY {T[t][0]} DESC").fetchall()
    return jsonify([dict(r) for r in rows])


@app.post("/api/<t>")
def create(t):
    if t not in T:
        return jsonify(error="Unknown table"), 404
    d = request.get_json(force=True)
    cols = [c for c in T[t][1] if c in d and d[c] != ""]
    try:
        cur = db().execute(
            f"INSERT INTO {t}({','.join(cols)}) VALUES({','.join('?' * len(cols))})",
            [d[c] for c in cols],
        )
        db().commit()
    except sqlite3.Error as e:
        return jsonify(error=str(e)), 400
    return jsonify(id=cur.lastrowid), 201


@app.put("/api/<t>/<int:i>")
def update(t, i):
    if t not in T:
        return jsonify(error="Unknown table"), 404
    d = request.get_json(force=True)
    cols = [c for c in T[t][1] if c in d]
    try:
        db().execute(
            f"UPDATE {t} SET {','.join(c + '=?' for c in cols)} WHERE {T[t][0]}=?",
            [d[c] if d[c] != "" else None for c in cols] + [i],
        )
        db().commit()
    except sqlite3.Error as e:
        return jsonify(error=str(e)), 400
    return jsonify(ok=True)


@app.delete("/api/<t>/<int:i>")
def delete(t, i):
    if t not in T:
        return jsonify(error="Unknown table"), 404
    try:
        db().execute(f"DELETE FROM {t} WHERE {T[t][0]}=?", (i,))
        db().commit()
    except sqlite3.Error:
        return jsonify(error="This record is used by another record. Delete that one first."), 400
    return jsonify(ok=True)


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
