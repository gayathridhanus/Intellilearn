def recommend_topics(concept_config, mastery, threshold=0.65):
    items = []
    for item in concept_config:
        name = item["name"]
        score = mastery.get(name, 0.50)
        prerequisite = item.get("prerequisite")
        prerequisite_score = mastery.get(prerequisite, 0.50) if prerequisite else 1.0
        if score < threshold and prerequisite_score >= 0.50:
            reason = "Needs more practice" if score < 0.50 else "Revise to strengthen mastery"
            if prerequisite:
                reason += f"; prerequisite {prerequisite} is sufficiently familiar"
            items.append({"concept": name, "mastery": score,
                          "difficulty": item["difficulty"], "reason": reason})
    return sorted(items, key=lambda x: x["mastery"])
