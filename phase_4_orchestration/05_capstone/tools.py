import math
from langchain_core.tools import tool
from typing import List, Dict, Tuple

# --- 1. MOCK DATABASE ---
# Generic healthcare provider data
NURSE_DB = [
    {"id": "n1", "name": "Sarah Jones", "location": "Brooklyn", "skills": ["ICU", "Wound Care"], "rating": 4.8, "is_preferred": True},
    {"id": "n2", "name": "Mike Ross", "location": "Manhattan", "skills": ["Pediatrics"], "rating": 4.2, "is_preferred": False},
    {"id": "n3", "name": "Jessica Pearson", "location": "Queens", "skills": ["ICU"], "rating": 4.9, "is_preferred": True},
    {"id": "n4", "name": "Gregory House", "location": "Bronx", "skills": ["Diagnostics", "ICU"], "rating": 3.5, "is_preferred": False},
]

LOCATIONS: Dict[str, Tuple[float, float]] = {
    "Brooklyn": (40.6782, -73.9442),
    "Manhattan": (40.7831, -73.9712),
    "Queens": (40.7282, -73.7949),
    "Bronx": (40.8448, -73.8648)
}

# --- 2. CONFIGURATION ---
# Standard weighted scoring logic
SCORING_WEIGHTS = {
    "distance": 0.50,
    "rating": 0.30,
    "preference": 0.20
}

# --- 3. HELPER FUNCTIONS ---

def haversine_distance(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """Calculates great-circle distance in miles."""
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 3958.8 
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def normalize(value: float, min_val: float, max_val: float) -> float:
    """Standard Min-Max Normalization: Scales value to 0.0 - 1.0 range."""
    if max_val == min_val:
        return 0.0
    return (value - min_val) / (max_val - min_val)

# --- 4. THE TOOL ---

@tool
def find_available_nurse(location: str, required_skill: str):
    """
    Finds and ranks nurses using a multi-factor weighted scoring algorithm.
    Factors: Distance (50%), Rating (30%), Provider Preference (20%).
    """
    target_coords = LOCATIONS.get(location)
    if not target_coords:
        return {"status": "error", "message": "Unknown location."}
        
    candidates = []
    
    # Step A: Filter by Skill & Calculate Raw Metrics
    for nurse in NURSE_DB:
        if any(required_skill.lower() in s.lower() for s in nurse["skills"]):
            nurse_coords = LOCATIONS.get(nurse["location"])
            dist = haversine_distance(target_coords, nurse_coords)
            
            candidates.append({
                **nurse,
                "raw_distance": dist,
                "score": 0.0
            })
    
    if not candidates:
        return {"status": "error", "message": "No matching nurses found."}

    # Step B: Normalize Metrics
    distances = [c["raw_distance"] for c in candidates]
    ratings = [c["rating"] for c in candidates]
    
    min_dist, max_dist = min(distances), max(distances)
    min_rate, max_rate = min(ratings), max(ratings)

    # Step C: Calculate Weighted Score
    ranked_results = []
    for c in candidates:
        # Normalize Distance (Inverted: Closer is better)
        norm_dist = normalize(c["raw_distance"], min_dist, max_dist)
        score_dist = 1.0 - norm_dist 
        
        # Normalize Rating
        score_rate = normalize(c["rating"], min_rate, max_rate)
        
        # Preference Bonus
        score_pref = 1.0 if c["is_preferred"] else 0.0
        
        # Weighted Sum
        final_score = (score_dist * SCORING_WEIGHTS["distance"]) + \
                      (score_rate * SCORING_WEIGHTS["rating"]) + \
                      (score_pref * SCORING_WEIGHTS["preference"])
        
        c["final_score"] = round(final_score, 2)
        c["raw_distance"] = round(c["raw_distance"], 2)
        ranked_results.append(c)

    # Step D: Sort Descending
    ranked_results.sort(key=lambda x: x["final_score"], reverse=True)
    winner = ranked_results[0]
    
    return {
        "status": "success",
        "nurse": winner["name"],
        "metrics": {
            "score": winner["final_score"],
            "distance_miles": winner["raw_distance"],
            "rating": winner["rating"]
        }
    }