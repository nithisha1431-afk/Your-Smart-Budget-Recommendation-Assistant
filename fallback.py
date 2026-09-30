from app.services.catalog import (
    home_catalog,
    party_catalog,
    jewelry_catalog,
    link,
)


def build_items(catalog, budget):
    result = []
    total = 0

    for name, category, price, platform in catalog:

        if total + price <= budget:

            result.append(
                {
                    "name": name,
                    "category": category,
                    "estimated_price": price,
                    "platform": platform,
                    "url": link(platform, name),
                    "reason": (
                        "Demo catalog option selected "
                        "within the requested budget."
                    ),
                }
            )

            total += price

        if len(result) >= 4:
            break

    return result


def fallback(planner, data):
    budget = float(data["budget"])

    catalogs = {
        "home": home_catalog(),
        "party": party_catalog(),
        "jewelry": jewelry_catalog(),
    }

    recommendations = build_items(
        catalogs[planner],
        budget
    )

    total = sum(
        item["estimated_price"]
        for item in recommendations
    )

    allocations = {
        "home": {
            "furniture": budget * 0.45,
            "lighting": budget * 0.20,
            "decor": budget * 0.20,
            "reserve": budget * 0.15,
        },

        "party": {
            "catering": budget * 0.45,
            "decoration": budget * 0.20,
            "venue": budget * 0.25,
            "reserve": budget * 0.10,
        },

        "jewelry": {
            "jewelry": budget * 0.80,
            "reserve": budget * 0.20,
        },
    }

    return {
        "planner": planner,
        "budget": budget,
        "total_estimate": total,
        "remaining_budget": max(
            0,
            budget - total
        ),
        "summary": (
            f"Demo {planner} plan generated "
            "within the requested budget."
        ),
        "allocations": allocations[planner],
        "recommendations": recommendations,
        "source": "fallback-demo",
        "warning": (
            "Gemini is not configured. "
            "Simulated catalog recommendations "
            "are being used."
        ),
        "request": data,
    }