from sentence_transformers import SentenceTransformer
import numpy as np
import pickle
import os

model = SentenceTransformer("all-MiniLM-L6-v2")

FILE = "memory_store.pkl"

if os.path.exists(FILE):
    with open(FILE, "rb") as f:
        incident_vectors, incident_texts = pickle.load(f)
else:
    incident_vectors, incident_texts = [], []

def store_incident(text):
    vec = model.encode(text)
    incident_vectors.append(vec)
    incident_texts.append(text)
    with open(FILE, "wb") as f:
        pickle.dump((incident_vectors, incident_texts), f)

def find_similar(text):
    if not incident_vectors:
        return None

    vec = model.encode(text)
    scores = [np.dot(vec, v) for v in incident_vectors]
    best = int(np.argmax(scores))
    return incident_texts[best]