# app/location_tools.py
"""Public API Location Lookup Tool for Ripple - Foresight Angle."""

import json
import os
import urllib.request


def fetch_location_info(zipcode: str) -> str:
    """Fetches location data (city, state, coordinates) for an Indian PIN code (6-digit) or US ZIP code (5-digit) using the Zippopotam.us public API.

    Args:
        zipcode: 6-digit Indian PIN code (e.g. '560001', '400001', '110001') or 5-digit US ZIP code string.

    Returns:
        JSON string containing resolved city, state, coordinates, and city tier benchmark factor.
    """
    try:
        clean_code = zipcode.strip()
        api_key = os.environ.get("ZIP_API_KEY", os.environ.get("PUBLIC_API_KEY", ""))

        # Determine if Indian PIN code (6 digits) or US ZIP code (5 digits)
        if len(clean_code) == 6 and clean_code.isdigit():
            country = "IN"
            url = f"https://api.zippopotam.us/in/{clean_code}"
        else:
            country = "US"
            url = f"https://api.zippopotam.us/us/{clean_code[:5]}"

        req = urllib.request.Request(url, headers={"User-Agent": "RippleAgent/1.0"})
        if api_key:
            req.add_header("Authorization", f"Bearer {api_key}")

        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                places = data.get("places", [])
                if not places:
                    return f"No location found for postal code {clean_code}."

                primary_place = places[0]
                city = primary_place.get("place name", "")
                state = primary_place.get("state", "")
                state_abbr = primary_place.get("state abbreviation", "")
                lat = primary_place.get("latitude", "")
                lon = primary_place.get("longitude", "")

                # Benchmark multiplier heuristics for Indian Tier 1 Metros & US High-Cost states
                indian_tier1_cities = {"Bengaluru", "Bangalore", "Mumbai", "Delhi", "New Delhi", "Gurgaon", "Gurugram", "Noida", "Hyderabad", "Pune", "Chennai"}
                high_cost_states = {"NY", "CA", "MA", "WA", "DC", "HI"}

                if country == "IN":
                    is_high_cost = any(t1.lower() in city.lower() or t1.lower() in state.lower() for t1 in indian_tier1_cities)
                    tier_name = "India Tier 1 Metro (High Cost)" if is_high_cost else "India Tier 2/3 City"
                    city_tier_multiplier = 1.35 if is_high_cost else 1.0
                else:
                    is_high_cost = state_abbr in high_cost_states
                    tier_name = "US Tier 1 High-Cost Metro" if is_high_cost else "US Standard Cost Metro"
                    city_tier_multiplier = 1.35 if is_high_cost else 1.0

                result = {
                    "postal_code": clean_code,
                    "country": country,
                    "city": city,
                    "state": state,
                    "latitude": lat,
                    "longitude": lon,
                    "location_cost_multiplier": city_tier_multiplier,
                    "city_tier_category": tier_name,
                }
                return json.dumps(result, indent=2)

        return f"Unable to fetch location data for postal code {clean_code}."
    except Exception as e:
        return f"Error querying location API for postal code {zipcode}: {str(e)}"
