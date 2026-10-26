def detect_threats(predictions):
    print("\nThreat Alerts:\n")

    for i, val in enumerate(predictions):
        if val == 1:
            print(f"⚠️ Threat detected at index {i}")