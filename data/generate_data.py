import pandas as pd
import json
import random
from faker import Faker

fake = Faker("en_IN")
random.seed(42)

areas      = ["Koramangala", "Indiranagar", "Whitefield", "Jayanagar", "HSR Layout"]
styles     = ["Casual", "Ethnic", "Streetwear", "Formal"]
categories = ["Tops", "Bottoms", "Footwear", "Ethnic Wear", "Accessories"]
colors     = ["Black", "White", "Navy", "Olive", "Maroon", "Beige", "Mustard", "Pastel", "Blue"]
brands     = ["Roadster", "HRX", "W", "Biba", "Puma", "Campus", "Van Heusen"]
budgets    = ["Low", "Mid", "High"]
sizes      = ["XS", "S", "M", "L", "XL"]
occasions  = ["College", "Festive", "Casual Outing", "Work", "Party"]
color_prefs = ["Black", "White", "Navy", "Pastel", "Blue", "Olive", "Maroon", "Mustard"]

# --- Users (now with color_pref + occasion) ---
users = []
for i in range(1, 26):
    users.append({
        "user_id":           f"U{i:03}",
        "name":              fake.name(),
        "age":               random.randint(16, 35),
        "area":              random.choice(areas),
        "school":            f"{random.choice(areas)} College",
        "budget":            random.choice(budgets),
        "style_pref":        random.choice(styles),
        "gender":            random.choice(["Male", "Female"]),
        "social_influence":  random.choice(["High", "Medium", "Low"]),
        "purchase_frequency":random.choice(["Weekly", "Monthly", "Rarely"]),
        "preferred_brands":  random.choice(brands),
        "size":              random.choice(sizes),
        "color_pref":        random.choice(color_prefs),   # NEW
        "occasion":          random.choice(occasions),     # NEW
    })

pd.DataFrame(users).to_csv("data/users.csv", index=False)

# --- Products ---
products = []
pid = 1
for cat in categories:
    for _ in range(10):
        price_map = {
            "Low":  random.randint(199, 499),
            "Mid":  random.randint(500, 1499),
            "High": random.randint(1500, 4999)
        }
        tier  = random.choice(budgets)
        color = random.choice(colors)
        style = random.choice(styles)
        brand = random.choice(brands)
        size  = random.choice(sizes)
        products.append({
            "product_id":  f"P{pid:03}",
            "name":        f"{brand} {color} {cat[:-1] if cat.endswith('s') else cat}",
            "category":    cat,
            "color":       color,
            "style":       style,
            "price":       price_map[tier],
            "budget_tier": tier,
            "brand":       brand,
            "size":        size,
        })
        pid += 1

pd.DataFrame(products).to_csv("data/products.csv", index=False)

# --- Sales Trends ---
product_names = [p["name"] for p in products]
trends = []
for area in areas:
    for _ in range(15):
        trends.append({
            "area":         area,
            "product_name": random.choice(product_names),
            "color":        random.choice(colors),
            "category":     random.choice(categories),
            "units_sold":   random.randint(10, 200),
            "month":        "April 2025"
        })

pd.DataFrame(trends).to_csv("data/sales_trends.csv", index=False)

# --- Social Connections ---
user_ids = [u["user_id"] for u in users]
social = {}
for u in user_ids:
    friends = random.sample([x for x in user_ids if x != u], k=random.randint(3, 6))
    social[u] = friends

with open("data/social_connections.json", "w") as f:
    json.dump(social, f, indent=2)

# --- Events Calendar ---
events = [
    {"name": "Diwali",              "days_away": 18, "relevant_categories": ["Ethnic Wear", "Accessories", "Footwear"]},
    {"name": "College Fest",        "days_away": 6,  "relevant_categories": ["Streetwear", "Tops", "Footwear"]},
    {"name": "End of Season Sale",  "days_away": 3,  "relevant_categories": ["Tops", "Bottoms", "Footwear"]},
    {"name": "Freshers Party",      "days_away": 12, "relevant_categories": ["Formal", "Accessories"]},
    {"name": "Republic Day",        "days_away": 25, "relevant_categories": ["Ethnic Wear", "Tops"]},
]

with open("data/events_calendar.json", "w") as f:
    json.dump(events, f, indent=2)

# --- Purchase History (with category for sequence analysis) ---
purchase_history = []
for u in users:
    past = random.sample(products, k=random.randint(3, 6))
    for p in past:
        purchase_history.append({
            "user_id":      u["user_id"],
            "product_id":   p["product_id"],
            "product_name": p["name"],
            "category":     p["category"],
            "price":        p["price"],
            "date_purchased": fake.date_between(
                start_date="-6m", end_date="today"
            ).strftime("%Y-%m-%d"),
        })

pd.DataFrame(purchase_history).to_csv("data/purchase_history.csv", index=False)

print("All datasets generated successfully.")
print(f"  users.csv            — {len(users)} users (now includes color_pref + occasion)")
print(f"  products.csv         — {len(products)} products")
print(f"  sales_trends.csv     — {len(trends)} trend records")
print(f"  social_connections   — {len(social)} users mapped")
print(f"  events_calendar      — {len(events)} events")
print(f"  purchase_history.csv — {len(purchase_history)} records")