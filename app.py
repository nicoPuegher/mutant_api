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

    is_dna_mutant = is_mutant(dna)
    sequence_str = "".join(dna)

    db = next(get_db())
    existing_dna = (
        db.query(DNASequence).filter(DNASequence.sequence == sequence_str).first()
    )

    if not existing_dna:
        new_dna_record = DNASequence(
            sequence=sequence_str, is_mutant=int(is_dna_mutant)
        )
        db.add(new_dna_record)
        db.commit()

    if is_dna_mutant:
        return jsonify({"status": "Mutant detected"}), 200
    else:
        return jsonify({"status": "Not a mutant"}), 403


@app.route("/stats", methods=["GET"])
def stats():
    db = next(get_db())
    mutant_count = db.query(DNASequence).filter(DNASequence.is_mutant == 1).count()
    human_count = db.query(DNASequence).filter(DNASequence.is_mutant == 0).count()
    ratio = round(mutant_count / human_count, 2) if human_count > 0 else 0.0

    return jsonify(
        {
            "count_mutant_dna": mutant_count,
            "count_human_dna": human_count,
            "ratio": ratio,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
