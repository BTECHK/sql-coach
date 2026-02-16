"""
Setup SQLite database with Google Ads sample data for SQL practice.
Run this once to create the database.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "google_ads.db")

def setup_database():
    """Create and populate the Google Ads practice database."""

    # Remove existing database
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # ========================================
    # CREATE TABLES
    # ========================================

    cursor.execute("""
        CREATE TABLE campaigns (
            campaign_id INTEGER PRIMARY KEY,
            campaign_name TEXT NOT NULL,
            campaign_type TEXT NOT NULL,
            status TEXT NOT NULL,
            daily_budget_micros INTEGER,
            bidding_strategy TEXT,
            start_date DATE
        )
    """)

    cursor.execute("""
        CREATE TABLE ad_groups (
            ad_group_id INTEGER PRIMARY KEY,
            campaign_id INTEGER NOT NULL,
            ad_group_name TEXT NOT NULL,
            status TEXT NOT NULL,
            cpc_bid_micros INTEGER,
            FOREIGN KEY (campaign_id) REFERENCES campaigns(campaign_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE ad_performance_daily (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL,
            campaign_id INTEGER NOT NULL,
            ad_group_id INTEGER NOT NULL,
            impressions INTEGER,
            clicks INTEGER,
            cost_micros INTEGER,
            conversions REAL,
            conversion_value REAL,
            device TEXT,
            FOREIGN KEY (campaign_id) REFERENCES campaigns(campaign_id),
            FOREIGN KEY (ad_group_id) REFERENCES ad_groups(ad_group_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE search_terms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL,
            campaign_id INTEGER NOT NULL,
            ad_group_id INTEGER NOT NULL,
            search_term TEXT NOT NULL,
            impressions INTEGER,
            clicks INTEGER,
            cost_micros INTEGER,
            conversions REAL,
            FOREIGN KEY (campaign_id) REFERENCES campaigns(campaign_id),
            FOREIGN KEY (ad_group_id) REFERENCES ad_groups(ad_group_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE conversions (
            conversion_id INTEGER PRIMARY KEY,
            date DATE NOT NULL,
            campaign_id INTEGER NOT NULL,
            ad_group_id INTEGER NOT NULL,
            conversion_action TEXT NOT NULL,
            conversion_value REAL,
            attribution_model TEXT,
            FOREIGN KEY (campaign_id) REFERENCES campaigns(campaign_id),
            FOREIGN KEY (ad_group_id) REFERENCES ad_groups(ad_group_id)
        )
    """)

    # ========================================
    # INSERT SAMPLE DATA
    # ========================================

    # Campaigns
    campaigns_data = [
        (1, "Brand_Search_US", "SEARCH", "ENABLED", 50000000, "TARGET_CPA", "2025-01-01"),
        (2, "Competitor_Search", "SEARCH", "ENABLED", 30000000, "MAXIMIZE_CLICKS", "2025-01-15"),
        (3, "Display_Remarketing", "DISPLAY", "ENABLED", 20000000, "TARGET_ROAS", "2025-02-01"),
        (4, "YouTube_Awareness", "VIDEO", "PAUSED", 75000000, "TARGET_CPM", "2025-01-10"),
        (5, "Shopping_Feed", "SHOPPING", "ENABLED", 40000000, "MAXIMIZE_CONVERSIONS", "2025-03-01"),
        (6, "Performance_Max_Q1", "PMAX", "ENABLED", 60000000, "MAXIMIZE_CONVERSIONS", "2025-01-20"),
    ]
    cursor.executemany("INSERT INTO campaigns VALUES (?,?,?,?,?,?,?)", campaigns_data)

    # Ad Groups
    ad_groups_data = [
        (101, 1, "Brand_Exact", "ENABLED", 2500000),
        (102, 1, "Brand_Broad", "ENABLED", 1800000),
        (103, 2, "Competitor_Names", "ENABLED", 4500000),
        (104, 3, "Past_Visitors_30d", "ENABLED", 1200000),
        (105, 3, "Cart_Abandoners", "ENABLED", 2000000),
        (106, 5, "All_Products", "ENABLED", 1500000),
        (107, 4, "Awareness_18_34", "PAUSED", 0),
        (108, 6, "PMax_Signals", "ENABLED", 0),
    ]
    cursor.executemany("INSERT INTO ad_groups VALUES (?,?,?,?,?)", ad_groups_data)

    # Ad Performance Daily
    performance_data = [
        ("2025-01-15", 1, 101, 12000, 850, 1275000000, 42.0, 4200.00, "MOBILE"),
        ("2025-01-15", 1, 101, 8500, 620, 930000000, 35.0, 3500.00, "DESKTOP"),
        ("2025-01-15", 1, 102, 25000, 400, 720000000, 12.0, 1200.00, "MOBILE"),
        ("2025-01-15", 2, 103, 9000, 310, 1395000000, 5.0, 500.00, "DESKTOP"),
        ("2025-01-15", 3, 104, 45000, 900, 1080000000, 22.0, 3300.00, "MOBILE"),
        ("2025-01-15", 3, 105, 18000, 650, 1300000000, 38.0, 5700.00, "DESKTOP"),
        ("2025-01-16", 1, 101, 11500, 800, 1200000000, 40.0, 4000.00, "MOBILE"),
        ("2025-01-16", 1, 101, 9200, 680, 1020000000, 38.0, 3800.00, "DESKTOP"),
        ("2025-01-16", 1, 102, 23000, 380, 684000000, 10.0, 1000.00, "MOBILE"),
        ("2025-01-16", 2, 103, 8500, 290, 1305000000, 4.0, 400.00, "DESKTOP"),
        ("2025-01-16", 3, 104, 42000, 870, 1044000000, 20.0, 3000.00, "MOBILE"),
        ("2025-01-16", 3, 105, 19500, 700, 1400000000, 41.0, 6150.00, "DESKTOP"),
        ("2025-01-17", 1, 101, 13000, 910, 1365000000, 45.0, 4500.00, "MOBILE"),
        ("2025-01-17", 1, 101, 8000, 590, 885000000, 32.0, 3200.00, "DESKTOP"),
        ("2025-01-17", 2, 103, 10200, 350, 1575000000, 6.0, 600.00, "DESKTOP"),
        ("2025-01-17", 3, 104, 48000, 950, 1140000000, 25.0, 3750.00, "MOBILE"),
        ("2025-01-17", 3, 105, 17000, 620, 1240000000, 35.0, 5250.00, "DESKTOP"),
        ("2025-01-17", 5, 106, 32000, 1200, 1800000000, 55.0, 8250.00, "MOBILE"),
        ("2025-01-17", 5, 106, 28000, 980, 1470000000, 48.0, 7200.00, "DESKTOP"),
        ("2025-01-17", 6, 108, 55000, 1800, 2700000000, 72.0, 10800.00, "MOBILE"),
    ]
    cursor.executemany(
        "INSERT INTO ad_performance_daily (date, campaign_id, ad_group_id, impressions, clicks, cost_micros, conversions, conversion_value, device) VALUES (?,?,?,?,?,?,?,?,?)",
        performance_data
    )

    # Search Terms
    search_terms_data = [
        ("2025-01-15", 1, 101, "buy acme widgets", 3000, 250, 375000000, 18.0),
        ("2025-01-15", 1, 101, "acme store near me", 2200, 180, 270000000, 12.0),
        ("2025-01-15", 1, 102, "cheap widgets online", 8000, 120, 216000000, 2.0),
        ("2025-01-15", 2, 103, "betterwidgets reviews", 4500, 155, 697500000, 3.0),
        ("2025-01-15", 2, 103, "widgetco vs acme", 3200, 100, 450000000, 1.0),
        ("2025-01-16", 1, 101, "acme widgets coupon", 2800, 200, 300000000, 15.0),
        ("2025-01-16", 1, 102, "free widgets download", 5000, 90, 162000000, 0.0),
        ("2025-01-16", 2, 103, "betterwidgets pricing", 4000, 140, 630000000, 2.0),
        ("2025-01-17", 1, 101, "buy acme widgets", 3200, 270, 405000000, 20.0),
        ("2025-01-17", 2, 103, "widgetco alternatives", 3800, 130, 585000000, 0.0),
        ("2025-01-17", 5, 106, "acme blue widget large", 8000, 400, 600000000, 22.0),
        ("2025-01-17", 5, 106, "widget gift set", 6000, 300, 450000000, 15.0),
    ]
    cursor.executemany(
        "INSERT INTO search_terms (date, campaign_id, ad_group_id, search_term, impressions, clicks, cost_micros, conversions) VALUES (?,?,?,?,?,?,?,?)",
        search_terms_data
    )

    # Conversions
    conversions_data = [
        (1001, "2025-01-15", 1, 101, "PURCHASE", 120.00, "DATA_DRIVEN"),
        (1002, "2025-01-15", 1, 101, "PURCHASE", 85.50, "DATA_DRIVEN"),
        (1003, "2025-01-15", 1, 101, "SIGN_UP", 0.00, "LAST_CLICK"),
        (1004, "2025-01-15", 3, 105, "PURCHASE", 250.00, "DATA_DRIVEN"),
        (1005, "2025-01-15", 3, 105, "ADD_TO_CART", 0.00, "LAST_CLICK"),
        (1006, "2025-01-16", 1, 101, "PURCHASE", 95.00, "DATA_DRIVEN"),
        (1007, "2025-01-16", 3, 104, "PURCHASE", 175.00, "DATA_DRIVEN"),
        (1008, "2025-01-16", 3, 105, "PURCHASE", 310.00, "DATA_DRIVEN"),
        (1009, "2025-01-17", 5, 106, "PURCHASE", 65.00, "DATA_DRIVEN"),
        (1010, "2025-01-17", 5, 106, "PURCHASE", 142.00, "DATA_DRIVEN"),
        (1011, "2025-01-17", 6, 108, "PURCHASE", 200.00, "DATA_DRIVEN"),
        (1012, "2025-01-17", 6, 108, "SIGN_UP", 0.00, "LAST_CLICK"),
    ]
    cursor.executemany("INSERT INTO conversions VALUES (?,?,?,?,?,?,?)", conversions_data)

    conn.commit()
    conn.close()

    print(f"Database created successfully at: {DB_PATH}")
    print("\nTables created:")
    print("  - campaigns (6 rows)")
    print("  - ad_groups (8 rows)")
    print("  - ad_performance_daily (20 rows)")
    print("  - search_terms (12 rows)")
    print("  - conversions (12 rows)")

if __name__ == "__main__":
    setup_database()
