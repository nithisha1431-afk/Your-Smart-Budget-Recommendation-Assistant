from urllib.parse import quote


PLATFORMS = {
    "Amazon": "https://www.amazon.in/s?k=",
    "Flipkart": "https://www.flipkart.com/search?q=",
    "IKEA": "https://www.ikea.com/in/en/search/?q=",
    "Swiggy": "https://www.swiggy.com/search?query=",
    "Zomato": "https://www.zomato.com/search?q=",
    "OYO": "https://www.oyorooms.com/search?location=",
}


def link(platform: str, query: str) -> str:
    base = PLATFORMS.get(
        platform,
        "https://www.google.com/search?q="
    )

    return base + quote(query)


def home_catalog():
    return [
        (
            "LED Ceiling Light",
            "Lighting",
            1299,
            "Amazon"
        ),
        (
            "5-Blade Ceiling Fan",
            "Electrical",
            2499,
            "Flipkart"
        ),
        (
            "Minimal Wall Art Set",
            "Decor",
            899,
            "IKEA"
        ),
        (
            "Compact Study Table",
            "Furniture",
            3499,
            "Amazon"
        ),
        (
            "Modern Dining Table",
            "Furniture",
            7999,
            "IKEA"
        ),
        (
            "Decorative Indoor Plant",
            "Decor",
            699,
            "Amazon"
        ),
    ]


def party_catalog():
    return [
        (
            "Vegetarian Catering Package",
            "Catering",
            250,
            "Swiggy"
        ),
        (
            "Party Snacks Combo",
            "Food",
            180,
            "Zomato"
        ),
        (
            "Decoration Starter Kit",
            "Decoration",
            2499,
            "Amazon"
        ),
        (
            "Simple Event Venue",
            "Venue",
            7000,
            "OYO"
        ),
        (
            "Cake and Dessert Package",
            "Food",
            1800,
            "Zomato"
        ),
    ]


def jewelry_catalog():
    return [
        (
            "Minimal Gold-Tone Necklace",
            "Necklace",
            899,
            "Amazon"
        ),
        (
            "Pearl Drop Earrings",
            "Earrings",
            699,
            "Flipkart"
        ),
        (
            "Elegant Bracelet",
            "Bracelet",
            799,
            "Amazon"
        ),
        (
            "Traditional Jhumka Set",
            "Earrings",
            1099,
            "Flipkart"
        ),
        (
            "Stone Pendant Set",
            "Necklace",
            1299,
            "Amazon"
        ),
    ]