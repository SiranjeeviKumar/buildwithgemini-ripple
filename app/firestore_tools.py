# app/firestore_tools.py
"""Firestore integration tools for Ripple decision benchmark profiles."""

import json
from typing import Optional
from google.cloud import firestore

# IMPORTANT: Hardcoded Project ID string per platform deployment requirement.
# Do NOT use google.auth.default() or GOOGLE_CLOUD_PROJECT env var.
PROJECT_ID = "qwiklabs-gcp-03-3773bdab8c6e"
COLLECTION_NAME = "decision_benchmarks"


def _get_firestore_client() -> firestore.Client:
    """Returns a Firestore client initialized with hardcoded project ID string."""
    return firestore.Client(project=PROJECT_ID)


def get_decision_benchmark(scenario_id: str) -> str:
    """Reads a decision benchmark scenario profile from Firestore by scenario ID.

    Args:
        scenario_id: The unique identifier for the scenario benchmark (e.g. 'dog-in-walkup', 'used-luxury-car', 'coding-bootcamp-pivot').

    Returns:
        JSON string containing the scenario benchmark data or error message.
    """
    try:
        db = _get_firestore_client()
        doc_ref = db.collection(COLLECTION_NAME).document(scenario_id)
        doc = doc_ref.get()

        if not doc.exists:
            return f"No decision benchmark found with ID '{scenario_id}'."

        return json.dumps(doc.to_dict(), indent=2)
    except Exception as e:
        return f"Error retrieving benchmark scenario from Firestore: {str(e)}"


def list_decision_benchmarks(category: str = "") -> str:
    """Lists available decision benchmark scenarios stored in Firestore.

    Args:
        category: Optional category string to filter scenarios (e.g. 'Pets & Housing', 'Vehicles & Transit', 'Career & Education').

    Returns:
        JSON string listing the matching decision benchmark profiles.
    """
    try:
        db = _get_firestore_client()
        collection_ref = db.collection(COLLECTION_NAME)

        if category:
            query = collection_ref.where("category", "==", category)
            docs = query.stream()
        else:
            docs = collection_ref.stream()

        results = [doc.to_dict() for doc in docs]
        if not results:
            return f"No decision benchmarks found for category '{category}'." if category else "No decision benchmarks stored in Firestore."

        return json.dumps(results, indent=2)
    except Exception as e:
        return f"Error listing benchmark scenarios from Firestore: {str(e)}"


def save_decision_benchmark(
    scenario_id: str,
    title: str,
    category: str,
    annual_tco_min: float,
    annual_tco_max: float,
    primary_friction: str,
    time_commitment_hrs_wk: int,
    common_pitfalls: str,
    recommended_alternatives: str,
) -> str:
    """Creates or updates a decision benchmark scenario profile in Firestore.

    Args:
        scenario_id: Unique identifier for the scenario (e.g., 'tiny-home-living').
        title: Descriptive title for the benchmark decision scenario.
        category: Decision domain category (e.g. 'Housing', 'Transportation', 'Career').
        annual_tco_min: Estimated minimum annual total cost of ownership in USD.
        annual_tco_max: Estimated maximum annual total cost of ownership in USD.
        primary_friction: Main friction point or physical constraint.
        time_commitment_hrs_wk: Estimated weekly time commitment in hours.
        common_pitfalls: Comma-separated list of common hidden risks or pitfalls.
        recommended_alternatives: Comma-separated list of lower-friction alternative choices.

    Returns:
        Confirmation message upon saving document to Firestore.
    """
    try:
        db = _get_firestore_client()
        doc_ref = db.collection(COLLECTION_NAME).document(scenario_id)

        pitfalls_list = [p.strip() for p in common_pitfalls.split(",") if p.strip()]
        alternatives_list = [a.strip() for a in recommended_alternatives.split(",") if a.strip()]

        payload = {
            "id": scenario_id,
            "title": title,
            "category": category,
            "annual_tco_min": annual_tco_min,
            "annual_tco_max": annual_tco_max,
            "primary_friction": primary_friction,
            "time_commitment_hrs_wk": time_commitment_hrs_wk,
            "common_pitfalls": pitfalls_list,
            "recommended_alternatives": alternatives_list,
        }

        doc_ref.set(payload)
        return f"Successfully saved benchmark scenario '{scenario_id}' ('{title}') to Firestore."
    except Exception as e:
        return f"Error saving benchmark scenario to Firestore: {str(e)}"
