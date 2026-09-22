# scripts/seed_firestore.py
"""Seed Firestore database with decision benchmark scenario profiles for Ripple."""

from google.cloud import firestore

PROJECT_ID = "qwiklabs-gcp-03-3773bdab8c6e"
COLLECTION_NAME = "decision_benchmarks"

SEED_DATA = [
    {
        "id": "dog-in-walkup",
        "category": "Pets & Housing",
        "title": "Adopting a Large Dog in a Walkup Apartment",
        "annual_tco_min": 2500,
        "annual_tco_max": 4000,
        "primary_friction": "Navigating 4+ flights of stairs 8-12 times daily with a 75lb+ dog",
        "time_commitment_hrs_wk": 15,
        "common_pitfalls": [
            "Underestimating emergency vet bills ($3k-$8k)",
            "Mandatory dog walker expense ($100+/week for 50hr work weeks)",
            "Senior dog arthritis causing stair immobility"
        ],
        "recommended_alternatives": [
            "Adopt a small low-energy breed under 25 lbs",
            "Foster first to test daily schedule friction",
            "Postpone until moving to an elevator/ground-floor building"
        ]
    },
    {
        "id": "used-luxury-car",
        "category": "Vehicles & Transit",
        "title": "Buying a Used Out-of-Warranty European Luxury Car",
        "annual_tco_min": 4500,
        "annual_tco_max": 8000,
        "primary_friction": "Exponential component failure costs & specialized mechanic labor rates ($180+/hr)",
        "time_commitment_hrs_wk": 4,
        "common_pitfalls": [
            "Deferred maintenance by previous owner causing compound failures",
            "High insurance premiums for performance trims",
            "Parts availability delays (2-4 weeks out of service)"
        ],
        "recommended_alternatives": [
            "Buy a certified pre-owned (CPO) vehicle with extended warranty",
            "Opt for a reliable Japanese sporty sedan (Lexus/Acura)",
            "Lease new if premium luxury features are essential"
        ]
    },
    {
        "id": "coding-bootcamp-pivot",
        "category": "Career & Education",
        "title": "Quitting Full-Time Job for 16-Week Intensive Coding Bootcamp",
        "annual_tco_min": 25000,
        "annual_tco_max": 45000,
        "primary_friction": "Extended job search runway (6-12 months) during entry-level market contraction",
        "time_commitment_hrs_wk": 60,
        "common_pitfalls": [
            "Ignoring total income gap during study + job hunt (est. 10-14 months total income deficit)",
            "Relying solely on Income Share Agreements (ISAs) with high payback caps",
            "Lack of portfolio differentiation"
        ],
        "recommended_alternatives": [
            "Part-time night/weekend self-paced program while keeping main income",
            "Build open-source contributions & portfolio projects before quitting",
            "Internal transfer to tech-adjacent role at current employer"
        ]
    }
]


def seed_database():
    """Populates Firestore collection with initial benchmark scenarios."""
    db = firestore.Client(project=PROJECT_ID)
    collection_ref = db.collection(COLLECTION_NAME)

    print(f"Seeding Firestore project '{PROJECT_ID}' -> collection '{COLLECTION_NAME}'...")
    for item in SEED_DATA:
        doc_id = item["id"]
        doc_ref = collection_ref.document(doc_id)
        doc_ref.set(item)
        print(f"  ✓ Seeded document: {doc_id} ('{item['title']}')")

    print("Successfully seeded Firestore benchmark scenarios!")


if __name__ == "__main__":
    seed_database()
