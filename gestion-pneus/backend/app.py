from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="gestion_pneus"
)

cursor = db.cursor(dictionary=True)

@app.route("/stock", methods=["GET"])
def stock():

    cursor.execute("SELECT * FROM stock_pneus")

    result = cursor.fetchall()

    return jsonify(result)

@app.route("/ajouter", methods=["POST"])
def ajouter():

    data = request.json

    sql = """
    INSERT INTO stock_pneus
    (marque, dimension, type_pneu, quantite, prix)
    VALUES (%s,%s,%s,%s,%s)
    """

    values = (
        data["marque"],
        data["dimension"],
        data["type_pneu"],
        data["quantite"],
        data["prix"]
    )

    cursor.execute(sql, values)

    db.commit()

    return jsonify({
        "success": True
    })

@app.route("/supprimer/<int:id>", methods=["DELETE"])
def supprimer(id):

    cursor.execute(
        "DELETE FROM stock_pneus WHERE id=%s",
        (id,)
    )

    db.commit()

    return jsonify({
        "success": True
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)