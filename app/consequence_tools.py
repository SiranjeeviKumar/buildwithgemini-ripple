# app/consequence_tools.py
"""Multi-Tier Consequence & Ripple Calculation Tools for Ripple - Foresight Angle."""

import json


def friction_calculator(
    decision_domain: str,
    physical_constraints: str,
    weekly_frequency: int,
    intensity_rating_1_to_10: int = 7,
) -> str:
    """Maps micro-annoyances, physical friction, and daily operational burden.

    Args:
        decision_domain: The decision area (e.g., 'Pet Ownership', 'Vehicle Purchase', 'Housing Move', 'Career Change').
        physical_constraints: Known physical or environmental constraints (e.g., '4th floor walkup, no elevator', '2-hour highway commute').
        weekly_frequency: How many times per week the physical task or friction occurs (e.g., 14 for dog walks, 10 for commutes).
        intensity_rating_1_to_10: Perceived physical/mental intensity of each friction event on a scale of 1 to 10.

    Returns:
        JSON string detailing daily, weekly, and annual friction metrics and annoyance scores.
    """
    try:
        annual_occurrences = weekly_frequency * 52
        annual_friction_score = annual_occurrences * intensity_rating_1_to_10

        if annual_friction_score > 3500:
            friction_tier = "CRITICAL FRICTION: Extreme daily lifestyle exhaustion risk."
        elif annual_friction_score > 1800:
            friction_tier = "HIGH FRICTION: Significant ongoing lifestyle compromise."
        elif annual_friction_score > 800:
            friction_tier = "MODERATE FRICTION: Manageable annoyance requiring routine discipline."
        else:
            friction_tier = "LOW FRICTION: Minimal operational burden."

        result = {
            "decision_domain": decision_domain,
            "physical_constraints": physical_constraints,
            "weekly_frequency": weekly_frequency,
            "annual_occurrences": annual_occurrences,
            "intensity_score_per_event": intensity_rating_1_to_10,
            "annual_friction_points": annual_friction_score,
            "friction_tier": friction_tier,
            "micro_annoyance_scenarios": [
                f"Navigating '{physical_constraints}' under bad weather or illness ({annual_occurrences} times/yr).",
                f"Emergency or late-night interruptions (est. 12-24 unexpected occurrences/yr).",
                f"Compounding physical fatigue over 52 weeks without break.",
            ],
        }

        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error computing friction breakdown: {str(e)}"


def tco_financial_stress_test(
    upfront_cost: float,
    monthly_cost: float,
    annual_inflation_pct: float = 5.5,
    investment_return_pct: float = 11.0,
    local_benchmark_multiplier: float = 1.0,
    currency_code: str = "INR",
) -> str:
    """Computes exact 1-year and 5-year compounding Total Cost of Ownership (TCO), inflation, and opportunity cost of capital.

    Args:
        upfront_cost: One-time initial expense (INR ₹ or foreign currency).
        monthly_cost: Initial base monthly recurring expense (INR ₹ or foreign currency).
        annual_inflation_pct: Annual inflation rate in India (default 5.5%).
        investment_return_pct: Expected annual return rate if capital were invested in Indian Equity Mutual Funds / Nifty index (default 11.0%).
        local_benchmark_multiplier: Cost multiplier based on city tier (e.g., 1.35 for Bengaluru/Mumbai Tier 1, 1.0 baseline).
        currency_code: Currency symbol/code (default 'INR' / '₹').

    Returns:
        JSON string containing 1-year TCO, 5-year compounding TCO, lost opportunity cost, and total financial stress score in INR (₹).
    """
    try:
        adj_upfront = upfront_cost * local_benchmark_multiplier
        adj_monthly = monthly_cost * local_benchmark_multiplier

        # 1-Year Calculation
        year1_recurring = adj_monthly * 12
        year1_total_tco = adj_upfront + year1_recurring

        # 5-Year Compounding Calculation with Inflation
        total_5yr_recurring = 0.0
        curr_monthly = adj_monthly
        monthly_costs_by_year = []

        for yr in range(1, 6):
            yr_total = curr_monthly * 12
            monthly_costs_by_year.append(round(yr_total, 2))
            total_5yr_recurring += yr_total
            curr_monthly *= (1.0 + (annual_inflation_pct / 100.0))

        total_5yr_tco = adj_upfront + total_5yr_recurring

        # Opportunity Cost Calculation (Compound growth of upfront + monthly investments over 5 years)
        r = investment_return_pct / 100.0
        upfront_opp_cost = adj_upfront * ((1 + r) ** 5)
        monthly_opp_cost = 0.0

        for yr in range(5):
            annual_inv = adj_monthly * 12
            monthly_opp_cost += annual_inv * ((1 + r) ** (5 - yr))

        total_opportunity_cost = upfront_opp_cost + monthly_opp_cost
        wealth_deficit_vs_investing = total_opportunity_cost - total_5yr_tco

        # Helper formatting for INR Lakhs
        tco_lakhs = total_5yr_tco / 100000.0
        deficit_lakhs = wealth_deficit_vs_investing / 100000.0

        result = {
            "currency": currency_code,
            "upfront_adjusted_inr": round(adj_upfront, 2),
            "monthly_adjusted_base_inr": round(adj_monthly, 2),
            "local_benchmark_multiplier": local_benchmark_multiplier,
            "year_1_total_tco_inr": round(year1_total_tco, 2),
            "year_5_compounding_tco_inr": round(total_5yr_tco, 2),
            "year_5_compounding_tco_formatted": f"₹{total_5yr_tco:,.2f} ({tco_lakhs:.2f} Lakhs)",
            "year_by_year_recurring_breakdown_inr": monthly_costs_by_year,
            "lost_opportunity_cost_if_invested_inr": round(total_opportunity_cost, 2),
            "5yr_wealth_deficit_vs_investing_inr": round(wealth_deficit_vs_investing, 2),
            "5yr_wealth_deficit_formatted": f"₹{wealth_deficit_vs_investing:,.2f} ({deficit_lakhs:.2f} Lakhs)",
            "financial_stress_summary": (
                f"Committing to this decision costs ₹{total_5yr_tco:,.2f} ({tco_lakhs:.2f} Lakhs) over 5 years and "
                f"forfeits an estimated ₹{wealth_deficit_vs_investing:,.2f} ({deficit_lakhs:.2f} Lakhs) in compound mutual fund growth."
            ),
        }

        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error computing financial stress test: {str(e)}"


def compliance_legal_check(
    decision_type: str,
    housing_or_location_type: str,
) -> str:
    """Surfaces potential Indian regulatory/legal risks, RWA rules, RTO registration, GST tariffs, lease security deposit norms, and tax implications.

    Args:
        decision_type: Type of decision (e.g., 'Pet Adoption', 'Used Vehicle', 'Home Renovation', 'Career Transition').
        housing_or_location_type: Housing environment (e.g., 'Gated Society Apartment', 'Independent House', '11-month Rental Walkup').

    Returns:
        JSON string listing potential legal, compliance, RWA, RTO, GST, and rental agreement flags.
    """
    try:
        flags = []
        decision_lower = decision_type.lower()
        housing_lower = housing_or_location_type.lower()

        if "pet" in decision_lower or "dog" in decision_lower:
            flags.extend([
                "RWA (Resident Welfare Association) Guidelines: Verification of pet policies, elevator usage rules, and designated leash areas.",
                "BBMP / Municipal Corporation pet licensing & mandatory annual rabies vaccination requirements.",
                "Rental Security Deposit Impact: Potential non-refundable cleaning deductions from the 3-10 month security deposit.",
                "Stairwell & Balkony Safety: Mesh netting requirements for high-rise balconies.",
            ])

        if "vehicle" in decision_lower or "car" in decision_lower:
            flags.extend([
                "RTO Registration & Road Tax: 8%-18% state RTO road tax based on ex-showroom price and vehicle fuel type (Petrol/Diesel/EV).",
                "Gated Society Covered Parking Allocation: Stacker/basement parking slot availability or monthly open parking surcharge.",
                "Insurance & Third-Party Liability: Mandatory Bumper-to-Bumper zero-depreciation insurance renewal + FASTag mandatory recharge.",
                "15-year (Petrol) / 10-year (Diesel) vehicle scrap & re-registration rules in Delhi NCR and major metros.",
            ])

        if "career" in decision_lower or "job" in decision_lower or "bootcamp" in decision_lower:
            flags.extend([
                "Notice Period Compensation & Buyout Surcharge: 1-3 month notice period shortfall penalty if changing roles.",
                "Health Insurance Continuity: Out-of-pocket health insurance / top-up coverage cost during unemployment gap.",
                "Tax Slabs & EPF Transfer: Income tax slab realignment, EPF account transfer, and 18% GST on vocational training programs.",
            ])

        if "society" in housing_lower or "rental" in housing_lower or "apartment" in housing_lower:
            flags.extend([
                "11-Month Rental Agreement Norms: 10% annual rent escalation clause + 3 to 10 months upfront refundable security deposit.",
                "Monthly Society Maintenance Charges: Fixed ₹2,000 - ₹8,000/month maintenance fee covering power backup, security, and lift maintenance.",
                "Water Supply Dependencies: Borewell vs Municipal Cauvery/Narmada water supply and emergency tanker surcharge during summer.",
            ])

        if not flags:
            flags.append("Standard Indian municipal, RWA, RTO, and IT-act compliance guidelines apply.")

        result = {
            "decision_type": decision_type,
            "housing_or_location_type": housing_or_location_type,
            "identified_compliance_and_legal_flags": flags,
            "risk_assessment": "Moderate regulatory & society scrutiny required prior to binding commitment.",
        }

        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error conducting compliance legal check: {str(e)}"


def relationship_social_ripple(
    time_commitment_hrs_wk: int,
    travel_flexibility_impact: str,
    partner_co_dependency: bool = True,
) -> str:
    """Evaluates impact on partner bandwidth, social life, spontaneous travel flexibility, and relational friction.

    Args:
        time_commitment_hrs_wk: Total weekly hours dedicated to managing/servicing this decision.
        travel_flexibility_impact: Description of travel constraint (e.g., 'Requires pet sitter or boarding ($80/night)', 'No long trips').
        partner_co_dependency: Whether a partner or roommate will share daily operational burden.

    Returns:
        JSON string evaluating social life impact, travel friction, partner bandwidth stress, and relational ripple score.
    """
    try:
        annual_hours_diverted = time_commitment_hrs_wk * 52

        if time_commitment_hrs_wk >= 15:
            social_impact_level = "HIGH RIPPLE: Significant restriction on spontaneous weekend activities and travel."
        elif time_commitment_hrs_wk >= 8:
            social_impact_level = "MODERATE RIPPLE: Requires advance scheduling and calendar coordination."
        else:
            social_impact_level = "LOW RIPPLE: Minor impact on discretionary leisure time."

        partner_friction_note = (
            "Partner/roommate will absorb ~30-50% of overflow friction, potentially leading to chore resentment."
            if partner_co_dependency
            else "Sole responsibility; no partner delegation possible."
        )

        result = {
            "weekly_time_commitment_hrs": time_commitment_hrs_wk,
            "annual_hours_diverted_from_leisure": annual_hours_diverted,
            "travel_flexibility_impact": travel_flexibility_impact,
            "partner_co_dependency": partner_co_dependency,
            "partner_bandwidth_impact": partner_friction_note,
            "social_ripple_classification": social_impact_level,
            "key_social_tradeoffs": [
                f"Loss of {annual_hours_diverted} hours per year previously available for hobbies, rest, or social events.",
                f"Spontaneous weekend getaways now cost extra or require 7+ days advance planning.",
                "Compounding fatigue reducing evening social energy.",
            ],
        }

        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error evaluating relationship social ripple: {str(e)}"
