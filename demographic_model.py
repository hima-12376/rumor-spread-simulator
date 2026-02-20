def predict_demographic(amp_score, validity):

    impact = amp_score * validity

    if impact > 0.5:
        return "Urban Users aged 30-50"
    elif impact > 0.25:
        return "Mixed Users aged 20-40"
    else:
        return "Young Users aged 18-25"