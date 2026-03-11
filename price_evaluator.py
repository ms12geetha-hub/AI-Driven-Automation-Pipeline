def compare_prices(vendor_results):
    """
    Adds price score and ranking based on invoice amount
    """
    # Filter vendors with valid amount
    valid_vendors = [
        v for v in vendor_results
        if v["extracted_data"].get("amount")
    ]

    # Convert amount to numeric
    for v in valid_vendors:
        amt = v["extracted_data"]["amount"]
        amt = amt.replace("₹", "").replace(",", "").strip()
        v["numeric_amount"] = float(amt)

    # Sort by lowest price
    valid_vendors.sort(key=lambda x: x["numeric_amount"])

    # Assign price rank & score
    for rank, vendor in enumerate(valid_vendors, start=1):
        vendor["price_rank"] = rank
        vendor["price_score"] = max(0, 100 - (rank - 1) * 10)

    return vendor_results
