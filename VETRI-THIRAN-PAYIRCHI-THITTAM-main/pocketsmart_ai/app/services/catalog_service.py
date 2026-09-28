from urllib.parse import quote_plus

PLATFORM_BASE = {
    "Amazon": "https://www.amazon.in/s?k=",
    "Flipkart": "https://www.flipkart.com/search?q=",
    "IKEA": "https://www.ikea.com/in/en/search/?q=",
    "Swiggy": "https://www.swiggy.com/search?query=",
    "Zomato": "https://www.zomato.com/search?q=",
    "OYO": "https://www.oyorooms.com/search?location=",
}

HOME_CATALOG = [
    ("LED Ceiling Light", "Lighting", 1299, "Amazon", "modern bright ceiling light"),
    ("Study/Work Lamp", "Lighting", 899, "IKEA", "desk lamp modern"),
    ("3-Seater Sofa", "Furniture", 18999, "IKEA", "3 seater sofa"),
    ("Compact Dining Table", "Furniture", 7499, "Flipkart", "4 seater dining table"),
    ("Wall Art Set", "Decor", 1299, "Amazon", "modern wall art set"),
    ("Artificial Indoor Plant", "Decor", 699, "IKEA", "indoor plant decor"),
    ("Ceiling Fan", "Appliances", 2499, "Flipkart", "energy efficient ceiling fan"),
    ("Storage Cabinet", "Storage", 5999, "IKEA", "storage cabinet"),
    ("Area Rug", "Decor", 2499, "Amazon", "modern area rug"),
    ("Curtain Set", "Decor", 1499, "Flipkart", "living room curtains"),
]

PARTY_CATALOG = [
    ("Veg Buffet Package", "Catering", 450, "Swiggy", "veg catering buffet"),
    ("Party Snack Combo", "Catering", 250, "Zomato", "party snack combo"),
    ("Birthday Decoration Kit", "Decoration", 1499, "Amazon", "birthday decoration kit"),
    ("LED Fairy Light Set", "Decoration", 599, "Flipkart", "party fairy lights"),
    ("Banquet Hall Search", "Venue", 12000, "OYO", "banquet hall event venue"),
    ("Cake + Dessert Package", "Catering", 1800, "Zomato", "birthday cake dessert"),
]

JEWELRY_CATALOG = [
    ("Minimal Gold-Tone Necklace Set", "Necklace", 899, "Amazon", "minimal gold necklace set"),
    ("Pearl Drop Earrings", "Earrings", 699, "Flipkart", "pearl drop earrings"),
    ("Statement Jhumka Earrings", "Earrings", 999, "Amazon", "statement jhumka earrings"),
    ("Silver-Tone Bracelet", "Bracelet", 749, "Flipkart", "silver tone bracelet"),
    ("Kundan Choker Set", "Necklace", 1599, "Amazon", "kundan choker necklace"),
    ("Simple Stud Earrings", "Earrings", 399, "Flipkart", "simple stud earrings"),
]


def search_url(platform: str, query: str) -> str:
    return PLATFORM_BASE.get(platform, PLATFORM_BASE["Amazon"]) + quote_plus(query)


def catalog_for(planner_type: str):
    return {"home": HOME_CATALOG, "party": PARTY_CATALOG, "jewelry": JEWELRY_CATALOG}[planner_type]


def get_budgeted_catalog(planner_type: str, budget: float, limit: int = 8):
    items = []
    for name, category, price, platform, query in catalog_for(planner_type):
        if price <= budget:
            items.append({
                "name": name,
                "category": category,
                "price": float(price),
                "platform": platform,
                "url": search_url(platform, query),
            })
    return items[:limit]
