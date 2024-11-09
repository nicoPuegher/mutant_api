from flask import Flask, request, jsonify
from db.database import Base, engine, get_db
from db.models import DNASequence
from dna_analysis.dna_checker import is_mutant

app = Flask(__name__)

# Create tables
Base.metadata.create_all(bind=engine)


@app.route("/mutant/", methods=["POST"])
def mutant():
    data = request.get_json()
    dna = data.get("dna")

    if not dna or not isinstance(dna, list) or any(len(row) != len(dna) for row in dna):
        return jsonify({"error": "Invalid DNA format"}), 400

    if is_mutant(dna):
        return jsonify({"message": "Mutant detected"}), 200
    else:
        return jsonify({"message": "Forbidden"}), 403


if __name__ == "__main__":
    app.run(debug=True)
