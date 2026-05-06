CUSTOMERS = [
    {"id": 1, "name": "Alice Johnson",  "email": "alice@example.com",  "location": "New York, NY",      "joined": "2024-01-15", "orders": 5, "total_spent": 649.95},
    {"id": 2, "name": "Bob Martinez",   "email": "bob@example.com",    "location": "Los Angeles, CA",   "joined": "2024-02-20", "orders": 3, "total_spent": 289.97},
    {"id": 3, "name": "Carol White",    "email": "carol@example.com",  "location": "Chicago, IL",       "joined": "2024-03-05", "orders": 7, "total_spent": 1124.93},
    {"id": 4, "name": "David Kim",      "email": "david@example.com",  "location": "Seattle, WA",       "joined": "2024-04-10", "orders": 2, "total_spent": 199.98},
    {"id": 5, "name": "Emma Davis",     "email": "emma@example.com",   "location": "Austin, TX",        "joined": "2024-05-22", "orders": 4, "total_spent": 524.96},
    {"id": 6, "name": "Frank Lee",      "email": "frank@example.com",  "location": "Boston, MA",        "joined": "2024-06-30", "orders": 1, "total_spent":  79.99},
    {"id": 7, "name": "Grace Chen",     "email": "grace@example.com",  "location": "San Francisco, CA", "joined": "2024-07-14", "orders": 6, "total_spent": 899.94},
    {"id": 8, "name": "Henry Brown",    "email": "henry@example.com",  "location": "Miami, FL",         "joined": "2024-08-01", "orders": 3, "total_spent": 374.97},
]

ORDERS = [
    {"id": "ORD-001", "customer": "Alice Johnson", "product": "Wireless Headphones",      "amount": 149.99, "status": "Delivered", "date": "2025-04-12"},
    {"id": "ORD-002", "customer": "Bob Martinez",  "product": "Mechanical Keyboard",      "amount":  89.99, "status": "Shipped",   "date": "2025-04-15"},
    {"id": "ORD-003", "customer": "Carol White",   "product": "4K Webcam",                "amount": 199.99, "status": "Delivered", "date": "2025-04-10"},
    {"id": "ORD-004", "customer": "David Kim",     "product": "Laptop Stand",             "amount":  49.99, "status": "Pending",   "date": "2025-04-20"},
    {"id": "ORD-005", "customer": "Emma Davis",    "product": "USB-C Hub",                "amount":  69.99, "status": "Delivered", "date": "2025-04-08"},
    {"id": "ORD-006", "customer": "Frank Lee",     "product": "Wireless Mouse",           "amount":  39.99, "status": "Shipped",   "date": "2025-04-18"},
    {"id": "ORD-007", "customer": "Grace Chen",    "product": "Noise Cancelling Earbuds", "amount": 179.99, "status": "Pending",   "date": "2025-04-22"},
    {"id": "ORD-008", "customer": "Alice Johnson", "product": "Mechanical Keyboard",      "amount":  89.99, "status": "Delivered", "date": "2025-03-28"},
    {"id": "ORD-009", "customer": "Carol White",   "product": "Monitor Light Bar",        "amount":  59.99, "status": "Delivered", "date": "2025-03-25"},
    {"id": "ORD-010", "customer": "Henry Brown",   "product": "USB-C Hub",                "amount":  69.99, "status": "Cancelled", "date": "2025-04-05"},
    {"id": "ORD-011", "customer": "Bob Martinez",  "product": "Laptop Stand",             "amount":  49.99, "status": "Delivered", "date": "2025-03-20"},
    {"id": "ORD-012", "customer": "Grace Chen",    "product": "Wireless Headphones",      "amount": 149.99, "status": "Shipped",   "date": "2025-04-17"},
    {"id": "ORD-013", "customer": "Emma Davis",    "product": "4K Webcam",                "amount": 199.99, "status": "Pending",   "date": "2025-04-21"},
    {"id": "ORD-014", "customer": "Carol White",   "product": "USB-C Hub",                "amount":  69.99, "status": "Delivered", "date": "2025-04-01"},
    {"id": "ORD-015", "customer": "David Kim",     "product": "Wireless Mouse",           "amount":  39.99, "status": "Shipped",   "date": "2025-04-19"},
    {"id": "ORD-016", "customer": "Alice Johnson", "product": "Monitor Light Bar",        "amount":  59.99, "status": "Delivered", "date": "2025-03-15"},
    {"id": "ORD-017", "customer": "Henry Brown",   "product": "Mechanical Keyboard",      "amount":  89.99, "status": "Delivered", "date": "2025-04-02"},
    {"id": "ORD-018", "customer": "Grace Chen",    "product": "Laptop Stand",             "amount":  49.99, "status": "Delivered", "date": "2025-03-30"},
]

PRODUCTS = [
    {"id": 1, "name": "Wireless Headphones",      "price": 149.99, "stock": 42, "category": "Audio"},
    {"id": 2, "name": "Mechanical Keyboard",       "price":  89.99, "stock": 28, "category": "Peripherals"},
    {"id": 3, "name": "4K Webcam",                 "price": 199.99, "stock": 15, "category": "Video"},
    {"id": 4, "name": "Laptop Stand",              "price":  49.99, "stock": 63, "category": "Accessories"},
    {"id": 5, "name": "USB-C Hub",                 "price":  69.99, "stock": 37, "category": "Accessories"},
    {"id": 6, "name": "Wireless Mouse",            "price":  39.99, "stock": 54, "category": "Peripherals"},
    {"id": 7, "name": "Noise Cancelling Earbuds",  "price": 179.99, "stock": 22, "category": "Audio"},
    {"id": 8, "name": "Monitor Light Bar",         "price":  59.99, "stock": 31, "category": "Accessories"},
]
