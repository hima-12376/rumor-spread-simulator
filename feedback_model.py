def compute_validity(upvotes, downvotes):

    total = upvotes + downvotes

    if total == 0:
        return 0.5  # Neutral if no votes

    validity = upvotes / total
    return validity