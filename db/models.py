from sqlalchemy import Column, String, Integer
from .database import Base


class DNASequence(Base):
    __tablename__ = "dna_sequences"
    id = Column(Integer, primary_key=True, index=True)
    sequence = Column(String, unique=True, nullable=False)
    is_mutant = Column(Integer, nullable=False)  # 1 for mutant, 0 for non-mutant
