from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        content = request.form["content"]

        conn = sqlite3.connect("notes.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO notes (content) VALUES (?)",
            (content,)
        )
        conn.commit()
        conn.close()

        return redirect("/")

    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()
    conn.close()

    return render_template("index.html", notes=notes)

@app.route("/edit/<int:note_id>", methods=["GET", "POST"])
def edit(note_id):
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()

    if request.method == "POST":
        new_content = request.form["content"]

        cursor.execute(
            "UPDATE notes SET content = ? WHERE id = ?",
            (new_content, note_id)
        )

        conn.commit()
        conn.close()
        return redirect("/")

    cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
    note = cursor.fetchone()
    conn.close()

    return render_template("edit.html", note=note)

@app.route("/delete/<int:note_id>")
def delete(note_id):
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM notes WHERE id = ?",
        (note_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")
  
if __name__ == "__main__":
    app.run(debug=True)
