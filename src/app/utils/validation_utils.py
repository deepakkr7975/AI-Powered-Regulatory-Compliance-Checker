
def validate_row(row):
    """
    Ensure row has all required fields.
    """
    required = ["Clause ID", "Contract Clause", "Regulation", "Risk Level", "AI Analysis"]
    for field in required:
        if not row.get(field):
            return False
    return True

def validate_results(results, start_id, clauses):
    """
    Re-run or fallback if validation fails.
    """
    validated = []
    for i, cl in enumerate(clauses):
        base = {
            "Clause ID": i + start_id,
            "Contract Clause": cl,
            "Regulation": "Unknown",
            "Risk Level": "Unknown",
            "AI Analysis": "Failed validation.",
        }
        try:
            res = results[i]
            validated.append(res if validate_row(res) else base)
        except:
            validated.append(base)
    return validated
