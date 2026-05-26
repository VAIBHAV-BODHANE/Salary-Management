import csv
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


# ============ FILE IMPORT ENDPOINT ============

BATCH_SIZE = 1000


def _get_file_from_request(field_name):
    """Returns file object or None if missing"""
    return request.files.get(field_name)


def _validate_missing_files(first_names_file, last_names_file, csv_file):
    """Check all files exist, return error message or None"""
    missing = []
    if first_names_file is None:
        missing.append("first_names.txt")
    if last_names_file is None:
        missing.append("last_names.txt")
    if csv_file is None:
        missing.append("employee_data.csv")
    if missing:
        return f"Missing required files: {', '.join(missing)}"
    return None


def _validate_csv_headers(csv_file):
    """Peek at CSV headers without consuming stream, return headers or error"""
    csv_file.seek(0)
    text = csv_file.read().decode('utf-8')
    csv_file.seek(0)

    lines = text.strip().split('\n')
    if not lines or not lines[0].strip():
        return None, "employee_data.csv is empty"

    reader = csv.DictReader(lines)
    if not reader.fieldnames:
        return None, "employee_data.csv has no headers"

    required = {"job_title", "country", "salary", "doj", "dob"}
    actual = set(reader.fieldnames)
    missing = required - actual
    if missing:
        return None, f"CSV missing required columns: {', '.join(sorted(missing))}"

    return reader.fieldnames, None


def _stream_text_lines(file_obj):
    """Generator: yield stripped non-empty lines from file"""
    for line in file_obj:
        line_str = line.decode('utf-8').strip()
        if line_str:
            yield line_str


def _stream_csv_rows(file_obj, fieldnames):
    """Generator: yield CSV rows as dicts"""
    file_obj.seek(0)
    text = file_obj.read().decode('utf-8')
    reader = csv.DictReader(text.splitlines(), fieldnames=fieldnames)
    next(reader, None)  # Skip header row
    for row in reader:
        yield row


def _validate_line_counts_streaming(first_names_file, last_names_file, csv_file):
    """Count lines without loading all into memory"""
    first_names_file.seek(0)
    last_names_file.seek(0)
    csv_file.seek(0)

    first_count = sum(1 for _ in first_names_file if _.strip())
    last_count = sum(1 for _ in last_names_file if _.strip())

    csv_file.seek(0)
    csv_text = csv_file.read().decode('utf-8')
    csv_lines = csv_text.strip().split('\n')
    csv_count = len([line for line in csv_lines[1:] if line.strip()])  # Exclude header

    if first_count == 0:
        return None, "first_names.txt is empty"
    if last_count == 0:
        return None, "last_names.txt is empty"
    if csv_count == 0:
        return None, "employee_data.csv has no data rows"

    if first_count != last_count or first_count != csv_count:
        return None, f"Line count mismatch: first_names.txt has {first_count} lines, last_names.txt has {last_count} lines, employee_data.csv has {csv_count} rows"

    return first_count, None


def _stream_combined_rows(first_names_file, last_names_file, csv_file, fieldnames):
    """
    Generator: combine streams by index, yield tuples
    Memory usage: O(1) — only keeps current row in memory
    """
    first_names_file.seek(0)
    last_names_file.seek(0)
    csv_file.seek(0)

    first_reader = _stream_text_lines(first_names_file)
    last_reader = _stream_text_lines(last_names_file)
    csv_reader = _stream_csv_rows(csv_file, fieldnames)

    for first, last, csv_row in zip(first_reader, last_reader, csv_reader):
        try:
            full_name = f"{first} {last}"
            job_title = csv_row.get("job_title", "").strip()
            country = csv_row.get("country", "").strip()
            salary = float(csv_row.get("salary", 0))
            doj = csv_row.get("doj", "").strip()
            dob = csv_row.get("dob", "").strip()

            yield (full_name, job_title, country, salary, doj, dob)
        except (ValueError, KeyError) as e:
            raise ValueError(f"Data format error in row: {str(e)}")


@employee_bp.route("/import", methods=["POST"])
def import_employees():
    """Bulk import employees from three files: first_names.txt, last_names.txt, employee_data.csv"""
    # Get files
    first_names_file = _get_file_from_request("first_names")
    last_names_file = _get_file_from_request("last_names")
    csv_file = _get_file_from_request("employee_data")

    # Step 1: Validate files exist
    error = _validate_missing_files(first_names_file, last_names_file, csv_file)
    if error:
        return jsonify({"error": error}), 400

    # Step 2: Validate CSV headers exist
    fieldnames, error = _validate_csv_headers(csv_file)
    if error:
        return jsonify({"error": error}), 400

    # Step 3: Validate line counts match
    count, error = _validate_line_counts_streaming(first_names_file, last_names_file, csv_file)
    if error:
        return jsonify({"error": error}), 400

    # Step 4: Stream and insert in batches
    db = get_db()
    try:
        batch = []
        imported = 0

        for row_tuple in _stream_combined_rows(first_names_file, last_names_file, csv_file, fieldnames):
            batch.append(row_tuple)

            # Insert when batch reaches size limit
            if len(batch) >= BATCH_SIZE:
                db.executemany(
                    """
                    INSERT INTO employees (full_name, job_title, country, salary, doj, dob)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    batch
                )
                db.commit()
                imported += len(batch)
                batch = []

        # Insert remaining rows
        if batch:
            db.executemany(
                """
                INSERT INTO employees (full_name, job_title, country, salary, doj, dob)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                batch
            )
            db.commit()
            imported += len(batch)

        return jsonify({"imported": imported}), 201

    except ValueError as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 400
