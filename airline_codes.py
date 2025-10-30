# airline_codes.py
"""airline_codes to map IATA airline codes to full airline names"""

AIRLINE_NAMES = {
    "QF": "Qantas",
    "VA": "Virgin Australia",
    "JQ": "Jetstar",
    "BA": "British Airways",
    "SQ": "Singapore Airlines",
    "EK": "Emirates",
    "QR": "Qatar Airways",
    "CX": "Cathay Pacific",
    "TG": "Thai Airways",
    "MH": "Malaysia Airlines",
    "GA": "Garuda Indonesia",
    "AA": "American Airlines",
    "UA": "United Airlines",
    "DL": "Delta Air Lines",
    "AF": "Air France",
    "LH": "Lufthansa",
    "KL": "KLM",
    
}

def get_airline_name(code):
    """if given an IATA airline code, return the full airline name"""
    return AIRLINE_NAMES.get(code, f"未知航司 ({code})")
