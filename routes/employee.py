from flask import Blueprint, jsonify, request, abort
from db import get_db

employee_bp = Blueprint("employee", __name__, url_prefix="/employees")

REQUIRED_FIELDS = ["full_name", "job_title", "country", "salary", "doj", "dob"]


def _row_to_dict(row):
    return dict(row)


@employee_bp.route("", methods=["POST"])
def create_employee():
    if not request.is_json:
        abort(415)
    body = request.get_json()
    missing = [f for f in REQUIRED_FIELDS if f not in body]
    if missing:
        return jsonify({"error": "Missing fields", "fields": missing}), 400

    db = get_db()
    cursor = db.execute(
        """
        INSERT INTO employees (full_name, job_title, country, salary, doj, dob)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (body["full_name"], body["job_title"], body["country"],
         body["salary"], body["doj"], body["dob"]),
    )
    db.commit()
    return jsonify({"empid": cursor.lastrowid}), 201


@employee_bp.route("", methods=["GET"])
def list_employees():
    db = get_db()
    rows = db.execute("SELECT * FROM employees").fetchall()
    return jsonify([_row_to_dict(r) for r in rows]), 200


@employee_bp.route("/<int:empid>", methods=["GET"])
def get_employee(empid):
    db = get_db()
    row = db.execute(
        "SELECT * FROM employees WHERE empid = ?", (empid,)
    ).fetchone()
    if row is None:
        abort(404)
    return jsonify(_row_to_dict(row)), 200


@employee_bp.route("/<int:empid>", methods=["PUT"])
def update_employee(empid):
    if not request.is_json:
        abort(415)
    body = request.get_json()
    missing = [f for f in REQUIRED_FIELDS if f not in body]
    if missing:
        return jsonify({"error": "Missing fields", "fields": missing}), 400

    db = get_db()
    cursor = db.execute(
        """
        UPDATE employees
        SET full_name=?, job_title=?, country=?, salary=?, doj=?, dob=?
        WHERE empid=?
        """,
        (body["full_name"], body["job_title"], body["country"],
         body["salary"], body["doj"], body["dob"], empid),
    )
    db.commit()
    if cursor.rowcount == 0:
        abort(404)
    row = db.execute(
        "SELECT * FROM employees WHERE empid = ?", (empid,)
    ).fetchone()
    return jsonify(_row_to_dict(row)), 200


@employee_bp.route("/<int:empid>", methods=["DELETE"])
def delete_employee(empid):
    db = get_db()
    cursor = db.execute(
        "DELETE FROM employees WHERE empid = ?", (empid,)
    )
    db.commit()
    if cursor.rowcount == 0:
        abort(404)
    return jsonify({"deleted": empid}), 200
