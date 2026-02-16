#!/usr/bin/env python3
"""
SQL Coach - Google gTech Ads Interview Prep
Interactive CLI tool with colored output, hints, and progress tracking.

Commands:
  run <sql>     - Execute SQL and see results
  hint          - Get a hint (progressive reveal)
  next          - Show next part of the solution
  answer        - Show full solution
  explain       - Explain your last query's execution
  schema        - Show database schema
  tables        - List all tables
  lesson        - Go to specific lesson (e.g., "lesson 1.2")
  progress      - Show your progress
  skip          - Skip to next lesson
  reset         - Reset current lesson progress
  help          - Show all commands
  quit          - Exit the coach
"""

import sqlite3
import os
import sys
import json
import re
from datetime import datetime

# ============================================================================
# ANSI COLOR CODES
# ============================================================================

class Colors:
    # Basic colors
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"

    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Bright foreground
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"

# Shorthand
C = Colors

# ============================================================================
# CURRICULUM - All lessons with hints and solutions
# ============================================================================

CURRICULUM = {
    "phases": [
        {
            "id": 1,
            "title": "Foundations",
            "description": "SELECT, FROM, WHERE, ORDER BY, LIMIT - the building blocks",
            "lessons": [
                {
                    "id": "1.1",
                    "title": "SELECT & FROM - Your Starting Point",
                    "concept": """Every SQL query starts here. SELECT defines WHAT you want to see.
FROM defines WHERE the data lives.

{cyan}Key syntax:{reset}
  SELECT column1, column2 FROM table_name;
  SELECT * FROM table_name;  -- all columns

{yellow}BigQuery Tip:{reset} SELECT * costs money! Always select only columns you need.

{green}Google Ads Context:{reset} You'll pull from performance tables like campaigns,
ad_groups, ad_performance_daily constantly.""",
                    "challenge": "Show me all campaign names and their bidding strategies from the campaigns table.",
                    "hints": [
                        "You need SELECT and FROM - two keywords",
                        "The columns you want are: campaign_name, bidding_strategy",
                        "The table is: campaigns"
                    ],
                    "solution_steps": [
                        "SELECT",
                        "SELECT campaign_name, bidding_strategy",
                        "SELECT campaign_name, bidding_strategy FROM campaigns;"
                    ],
                    "answer": "SELECT campaign_name, bidding_strategy FROM campaigns;",
                    "follow_up": "Try: Show only SEARCH type campaigns (you'll need WHERE)"
                },
                {
                    "id": "1.2",
                    "title": "WHERE - Filtering Rows",
                    "concept": """WHERE filters individual rows BEFORE any grouping happens.

{cyan}Common operators:{reset}
  =, !=, <, >, <=, >=
  BETWEEN, IN, LIKE
  IS NULL, IS NOT NULL
  AND, OR, NOT

{red}Interview Trap:{reset} You CANNOT use column aliases from SELECT in WHERE!
  {dim}-- WRONG: SELECT cost_micros/1000000 AS cost_usd WHERE cost_usd > 10{reset}
  {green}-- RIGHT: SELECT cost_micros/1000000 AS cost_usd WHERE cost_micros > 10000000{reset}

{yellow}Why?{reset} WHERE executes BEFORE SELECT in the query execution order.""",
                    "challenge": "Find all ad performance rows where device is 'MOBILE' and impressions are greater than 20000.",
                    "hints": [
                        "Start with SELECT * FROM ad_performance_daily",
                        "Add WHERE with two conditions",
                        "Use AND to combine: device = 'MOBILE' AND impressions > 20000",
                        "String values need quotes: 'MOBILE'"
                    ],
                    "solution_steps": [
                        "SELECT * FROM ad_performance_daily",
                        "SELECT * FROM ad_performance_daily WHERE device = 'MOBILE'",
                        "SELECT * FROM ad_performance_daily WHERE device = 'MOBILE' AND impressions > 20000;"
                    ],
                    "answer": "SELECT * FROM ad_performance_daily WHERE device = 'MOBILE' AND impressions > 20000;",
                    "follow_up": "Try: Find search terms with clicks but ZERO conversions (wasted spend)"
                },
                {
                    "id": "1.3",
                    "title": "ORDER BY & LIMIT",
                    "concept": """ORDER BY sorts results. LIMIT restricts row count.

{cyan}Syntax:{reset}
  ORDER BY column ASC   -- ascending (default)
  ORDER BY column DESC  -- descending
  LIMIT 10              -- first 10 rows

{green}Interview Pattern:{reset} "Find the top N..." = ORDER BY + LIMIT

{yellow}BigQuery Tip:{reset} Always use LIMIT when exploring large tables - saves cost!

{magenta}Key Insight:{reset} ORDER BY runs AFTER SELECT, so you CAN use aliases here!
  SELECT cost_micros/1000000 AS cost_usd ... ORDER BY cost_usd DESC  {green}-- WORKS!{reset}""",
                    "challenge": "Show the top 5 ad performance rows by clicks (highest first). Include date, campaign_id, clicks, and cost_micros.",
                    "hints": [
                        "SELECT specific columns, not *",
                        "ORDER BY clicks DESC for highest first",
                        "Add LIMIT 5 at the end"
                    ],
                    "solution_steps": [
                        "SELECT date, campaign_id, clicks, cost_micros",
                        "SELECT date, campaign_id, clicks, cost_micros FROM ad_performance_daily",
                        "SELECT date, campaign_id, clicks, cost_micros FROM ad_performance_daily ORDER BY clicks DESC",
                        "SELECT date, campaign_id, clicks, cost_micros FROM ad_performance_daily ORDER BY clicks DESC LIMIT 5;"
                    ],
                    "answer": "SELECT date, campaign_id, clicks, cost_micros FROM ad_performance_daily ORDER BY clicks DESC LIMIT 5;",
                    "follow_up": "Try converting cost_micros to dollars (divide by 1000000) and alias it"
                },
                {
                    "id": "1.4",
                    "title": "Execution Order - The Key Insight",
                    "concept": """SQL does NOT execute top-to-bottom. Understanding this prevents bugs!

{cyan}Logical Execution Order:{reset}
  1. FROM / JOIN    {dim}← tables loaded first{reset}
  2. WHERE          {dim}← filter individual rows{reset}
  3. GROUP BY       {dim}← group remaining rows{reset}
  4. HAVING         {dim}← filter groups{reset}
  5. SELECT         {dim}← compute columns + aliases{reset}
  6. DISTINCT       {dim}← remove duplicates{reset}
  7. ORDER BY       {dim}← sort (CAN use aliases){reset}
  8. LIMIT          {dim}← restrict rows{reset}

{yellow}Mnemonic:{reset} "From Where Groups Have Selected Distinct Ordered Limits"

{green}This explains:{reset}
  • Aliases don't work in WHERE (SELECT hasn't run yet)
  • Aliases DO work in ORDER BY (runs after SELECT)
  • HAVING exists separately from WHERE (needs aggregated values)""",
                    "challenge": "Calculate cost in USD (cost_micros / 1000000) as cost_usd, then ORDER BY cost_usd descending. Limit to 5 rows.",
                    "hints": [
                        "Create an alias: cost_micros / 1000000.0 AS cost_usd",
                        "You can use the alias in ORDER BY",
                        "Include date and campaign_id for context"
                    ],
                    "solution_steps": [
                        "SELECT date, campaign_id, cost_micros / 1000000.0 AS cost_usd",
                        "SELECT date, campaign_id, cost_micros / 1000000.0 AS cost_usd FROM ad_performance_daily",
                        "SELECT date, campaign_id, cost_micros / 1000000.0 AS cost_usd FROM ad_performance_daily ORDER BY cost_usd DESC",
                        "SELECT date, campaign_id, cost_micros / 1000000.0 AS cost_usd FROM ad_performance_daily ORDER BY cost_usd DESC LIMIT 5;"
                    ],
                    "answer": "SELECT date, campaign_id, cost_micros / 1000000.0 AS cost_usd FROM ad_performance_daily ORDER BY cost_usd DESC LIMIT 5;",
                    "follow_up": "Notice you CAN use cost_usd in ORDER BY. Try using it in WHERE and see why it fails."
                }
            ]
        },
        {
            "id": 2,
            "title": "Aggregation & GROUP BY",
            "description": "COUNT, SUM, AVG, GROUP BY, HAVING - analyzing data at scale",
            "lessons": [
                {
                    "id": "2.1",
                    "title": "Aggregate Functions",
                    "concept": """Aggregates collapse multiple rows into a single value.

{cyan}Core Functions:{reset}
  COUNT(*)      -- count all rows (including NULLs)
  COUNT(col)    -- count non-NULL values
  SUM(col)      -- total
  AVG(col)      -- average
  MIN(col)      -- smallest
  MAX(col)      -- largest

{red}NULL Trap:{reset} AVG ignores NULLs!
  If you have [10, NULL, 20], AVG = 15 (not 10)

{green}Google Ads Use:{reset}
  "What's total spend?" → SUM(cost_micros)
  "Average CTR?" → AVG(clicks * 100.0 / impressions)""",
                    "challenge": "Calculate the total impressions, total clicks, and total cost in USD across ALL rows in ad_performance_daily.",
                    "hints": [
                        "Use SUM() for each metric",
                        "No GROUP BY needed - you want one total across everything",
                        "Divide cost_micros by 1000000.0 for USD",
                        "Use AS to create readable column names"
                    ],
                    "solution_steps": [
                        "SELECT SUM(impressions)",
                        "SELECT SUM(impressions) AS total_impressions, SUM(clicks) AS total_clicks",
                        "SELECT SUM(impressions) AS total_impressions, SUM(clicks) AS total_clicks, SUM(cost_micros) / 1000000.0 AS total_cost_usd",
                        "SELECT SUM(impressions) AS total_impressions, SUM(clicks) AS total_clicks, SUM(cost_micros) / 1000000.0 AS total_cost_usd FROM ad_performance_daily;"
                    ],
                    "answer": "SELECT SUM(impressions) AS total_impressions, SUM(clicks) AS total_clicks, SUM(cost_micros) / 1000000.0 AS total_cost_usd FROM ad_performance_daily;",
                    "follow_up": "Add AVG(clicks) as avg_clicks to see average per row"
                },
                {
                    "id": "2.2",
                    "title": "GROUP BY - Aggregating by Category",
                    "concept": """GROUP BY splits rows into buckets, then aggregates within each.

{cyan}The Golden Rule:{reset}
Every column in SELECT must either be:
  1. In the GROUP BY clause, OR
  2. Inside an aggregate function

{red}WRONG:{reset}
  SELECT campaign_id, ad_group_id, SUM(clicks)
  FROM ... GROUP BY campaign_id
  {dim}-- ad_group_id isn't grouped or aggregated!{reset}

{green}RIGHT:{reset}
  SELECT campaign_id, SUM(clicks)
  FROM ... GROUP BY campaign_id

{yellow}Ad Tech Pattern:{reset}
  GROUP BY campaign_id  -- metrics per campaign
  GROUP BY device       -- mobile vs desktop
  GROUP BY date         -- daily trends""",
                    "challenge": "For each campaign_id, show the total impressions, total clicks, and total cost in USD.",
                    "hints": [
                        "SELECT campaign_id and your aggregates",
                        "Use SUM() for each metric",
                        "GROUP BY campaign_id at the end"
                    ],
                    "solution_steps": [
                        "SELECT campaign_id",
                        "SELECT campaign_id, SUM(impressions) AS total_impressions",
                        "SELECT campaign_id, SUM(impressions) AS total_impressions, SUM(clicks) AS total_clicks, SUM(cost_micros) / 1000000.0 AS total_cost_usd",
                        "SELECT campaign_id, SUM(impressions) AS total_impressions, SUM(clicks) AS total_clicks, SUM(cost_micros) / 1000000.0 AS total_cost_usd FROM ad_performance_daily",
                        "SELECT campaign_id, SUM(impressions) AS total_impressions, SUM(clicks) AS total_clicks, SUM(cost_micros) / 1000000.0 AS total_cost_usd FROM ad_performance_daily GROUP BY campaign_id;"
                    ],
                    "answer": "SELECT campaign_id, SUM(impressions) AS total_impressions, SUM(clicks) AS total_clicks, SUM(cost_micros) / 1000000.0 AS total_cost_usd FROM ad_performance_daily GROUP BY campaign_id;",
                    "follow_up": "Try grouping by campaign_id AND device to see breakdown by device"
                },
                {
                    "id": "2.3",
                    "title": "HAVING - Filtering After Aggregation",
                    "concept": """HAVING filters GROUPS. WHERE filters ROWS.

{cyan}The Difference:{reset}
  WHERE  = "only look at rows where..."      {dim}(before grouping){reset}
  HAVING = "only show groups where..."       {dim}(after grouping){reset}

{green}Classic Interview Question:{reset}
"Show campaigns that spent more than $10K total"

  {red}WHERE cost_micros > 10000000000{reset}
  {dim}← filters individual ROWS over $10K each{reset}

  {green}HAVING SUM(cost_micros) > 10000000000{reset}
  {dim}← filters GROUPS whose TOTAL is over $10K{reset}

{yellow}Key Insight:{reset} HAVING can use aggregate functions, WHERE cannot.""",
                    "challenge": "Show campaigns where total clicks exceed 2000. Display campaign_id, total clicks, and total cost in USD.",
                    "hints": [
                        "First write a GROUP BY query for campaign metrics",
                        "Add HAVING after GROUP BY",
                        "HAVING SUM(clicks) > 2000"
                    ],
                    "solution_steps": [
                        "SELECT campaign_id, SUM(clicks) AS total_clicks, SUM(cost_micros) / 1000000.0 AS total_cost_usd FROM ad_performance_daily GROUP BY campaign_id",
                        "SELECT campaign_id, SUM(clicks) AS total_clicks, SUM(cost_micros) / 1000000.0 AS total_cost_usd FROM ad_performance_daily GROUP BY campaign_id HAVING SUM(clicks) > 2000;"
                    ],
                    "answer": "SELECT campaign_id, SUM(clicks) AS total_clicks, SUM(cost_micros) / 1000000.0 AS total_cost_usd FROM ad_performance_daily GROUP BY campaign_id HAVING SUM(clicks) > 2000;",
                    "follow_up": "Add WHERE device = 'MOBILE' to filter rows BEFORE grouping, keep HAVING"
                }
            ]
        },
        {
            "id": 3,
            "title": "JOINs",
            "description": "INNER, LEFT, multi-table - combining data across tables",
            "lessons": [
                {
                    "id": "3.1",
                    "title": "INNER JOIN - Matching Rows Only",
                    "concept": """INNER JOIN returns only rows that match in BOTH tables.

{cyan}Syntax:{reset}
  SELECT a.col, b.col
  FROM table_a a
  INNER JOIN table_b b ON a.key = b.key

{green}Google Ads Use:{reset}
Join campaigns to ad_performance_daily to get campaign names alongside metrics.

{red}Pitfall:{reset} If join key has duplicates, you get row multiplication!
  {dim}1 campaign row + 5 performance rows = 5 result rows{reset}
  This is expected, but be aware of it.

{yellow}Pro Tip:{reset} Always use table aliases (c, p, ag) - cleaner and required
when column names overlap.""",
                    "challenge": "Join campaigns to ad_performance_daily to show campaign_name, date, clicks, and cost_micros for each performance row.",
                    "hints": [
                        "Start with FROM ad_performance_daily p",
                        "JOIN campaigns c ON matching campaign_id",
                        "Select: c.campaign_name, p.date, p.clicks, p.cost_micros"
                    ],
                    "solution_steps": [
                        "SELECT c.campaign_name, p.date, p.clicks, p.cost_micros",
                        "SELECT c.campaign_name, p.date, p.clicks, p.cost_micros FROM ad_performance_daily p",
                        "SELECT c.campaign_name, p.date, p.clicks, p.cost_micros FROM ad_performance_daily p INNER JOIN campaigns c ON p.campaign_id = c.campaign_id;"
                    ],
                    "answer": "SELECT c.campaign_name, p.date, p.clicks, p.cost_micros FROM ad_performance_daily p INNER JOIN campaigns c ON p.campaign_id = c.campaign_id;",
                    "follow_up": "Add GROUP BY c.campaign_name and aggregate to see totals per campaign name"
                },
                {
                    "id": "3.2",
                    "title": "LEFT JOIN - Keep All Left Rows",
                    "concept": """LEFT JOIN keeps ALL rows from the left table.
If no match exists in right table, right columns are NULL.

{green}Why It Matters:{reset}
"Show me ALL campaigns, even those with no performance data."

Campaign 4 (YouTube_Awareness) is PAUSED - may have no performance rows.
  INNER JOIN would drop it
  LEFT JOIN keeps it with NULLs for performance columns

{red}CLASSIC TRAP:{reset} Filtering right table in WHERE turns LEFT into INNER!

  {red}WRONG{reset} (drops non-matching rows):
  SELECT * FROM campaigns c
  LEFT JOIN ad_performance_daily p ON c.campaign_id = p.campaign_id
  WHERE p.device = 'MOBILE'

  {green}RIGHT{reset} (filter in ON clause):
  SELECT * FROM campaigns c
  LEFT JOIN ad_performance_daily p ON c.campaign_id = p.campaign_id
    AND p.device = 'MOBILE'""",
                    "challenge": "Show ALL campaigns (including those with no performance data) with their total clicks. Use COALESCE to show 0 instead of NULL.",
                    "hints": [
                        "Start FROM campaigns (left table keeps all rows)",
                        "LEFT JOIN ad_performance_daily",
                        "Use COALESCE(SUM(p.clicks), 0) to replace NULL with 0",
                        "GROUP BY c.campaign_name"
                    ],
                    "solution_steps": [
                        "SELECT c.campaign_name FROM campaigns c",
                        "SELECT c.campaign_name FROM campaigns c LEFT JOIN ad_performance_daily p ON c.campaign_id = p.campaign_id",
                        "SELECT c.campaign_name, COALESCE(SUM(p.clicks), 0) AS total_clicks FROM campaigns c LEFT JOIN ad_performance_daily p ON c.campaign_id = p.campaign_id",
                        "SELECT c.campaign_name, COALESCE(SUM(p.clicks), 0) AS total_clicks FROM campaigns c LEFT JOIN ad_performance_daily p ON c.campaign_id = p.campaign_id GROUP BY c.campaign_name;"
                    ],
                    "answer": "SELECT c.campaign_name, COALESCE(SUM(p.clicks), 0) AS total_clicks FROM campaigns c LEFT JOIN ad_performance_daily p ON c.campaign_id = p.campaign_id GROUP BY c.campaign_name;",
                    "follow_up": "Which campaigns show 0? Why does LEFT JOIN matter vs INNER?"
                },
                {
                    "id": "3.3",
                    "title": "Multi-Table JOINs",
                    "concept": """Chain joins to connect 3+ tables. Very common in interviews!

{cyan}Pattern:{reset}
Start from fact table (ad_performance_daily), join dimension tables.

  SELECT c.campaign_name, ag.ad_group_name, SUM(p.clicks)
  FROM ad_performance_daily p
  JOIN campaigns c ON p.campaign_id = c.campaign_id
  JOIN ad_groups ag ON p.ad_group_id = ag.ad_group_id
  GROUP BY c.campaign_name, ag.ad_group_name

{yellow}Pro Tips:{reset}
  • Always use table aliases - cleaner and often required
  • Think about grain: what's each row in your result?
  • JOIN order usually doesn't matter for results (optimizer handles it)""",
                    "challenge": "Write a 3-table join: Show campaign_name, ad_group_name, total impressions, total clicks, and total conversions for each ad group.",
                    "hints": [
                        "FROM ad_performance_daily p (fact table)",
                        "JOIN campaigns c ON campaign_id",
                        "JOIN ad_groups ag ON ad_group_id",
                        "GROUP BY c.campaign_name, ag.ad_group_name",
                        "SUM the metrics"
                    ],
                    "solution_steps": [
                        "SELECT c.campaign_name, ag.ad_group_name",
                        "SELECT c.campaign_name, ag.ad_group_name, SUM(p.impressions) AS total_impr, SUM(p.clicks) AS total_clicks, SUM(p.conversions) AS total_conv",
                        "SELECT c.campaign_name, ag.ad_group_name, SUM(p.impressions) AS total_impr, SUM(p.clicks) AS total_clicks, SUM(p.conversions) AS total_conv FROM ad_performance_daily p",
                        "SELECT c.campaign_name, ag.ad_group_name, SUM(p.impressions) AS total_impr, SUM(p.clicks) AS total_clicks, SUM(p.conversions) AS total_conv FROM ad_performance_daily p JOIN campaigns c ON p.campaign_id = c.campaign_id JOIN ad_groups ag ON p.ad_group_id = ag.ad_group_id",
                        "SELECT c.campaign_name, ag.ad_group_name, SUM(p.impressions) AS total_impr, SUM(p.clicks) AS total_clicks, SUM(p.conversions) AS total_conv FROM ad_performance_daily p JOIN campaigns c ON p.campaign_id = c.campaign_id JOIN ad_groups ag ON p.ad_group_id = ag.ad_group_id GROUP BY c.campaign_name, ag.ad_group_name;"
                    ],
                    "answer": "SELECT c.campaign_name, ag.ad_group_name, SUM(p.impressions) AS total_impr, SUM(p.clicks) AS total_clicks, SUM(p.conversions) AS total_conv FROM ad_performance_daily p JOIN campaigns c ON p.campaign_id = c.campaign_id JOIN ad_groups ag ON p.ad_group_id = ag.ad_group_id GROUP BY c.campaign_name, ag.ad_group_name;",
                    "follow_up": "Add CTR column: SUM(clicks) * 100.0 / SUM(impressions) AS ctr"
                }
            ]
        },
        {
            "id": 4,
            "title": "Window Functions & CTEs",
            "description": "ROW_NUMBER, RANK, LAG/LEAD, WITH clauses - advanced patterns",
            "lessons": [
                {
                    "id": "4.1",
                    "title": "Window Functions - The TSC III Separator",
                    "concept": """Window functions compute values across related rows WITHOUT collapsing them.

{cyan}Syntax:{reset}
  function() OVER (PARTITION BY col ORDER BY col)

{cyan}Key Functions:{reset}
  ROW_NUMBER() -- unique sequential (1,2,3,4), arbitrary tie-breaking
  RANK()       -- ties share rank, gaps after (1,2,2,4)
  DENSE_RANK() -- ties share rank, no gaps (1,2,2,3)

{yellow}PARTITION BY{reset} = like GROUP BY but keeps all rows
{yellow}ORDER BY{reset} = defines ranking order within each partition

{green}Google Ads Use:{reset}
  "Rank campaigns by spend"
  "Find top ad group per campaign"
  "Number rows for deduplication" """,
                    "challenge": "For each row in ad_performance_daily, rank by clicks within each campaign_id (highest first). Show campaign_id, date, device, clicks, and rank.",
                    "hints": [
                        "Use RANK() OVER (...)",
                        "PARTITION BY campaign_id",
                        "ORDER BY clicks DESC",
                        "Give the rank an alias like click_rank"
                    ],
                    "solution_steps": [
                        "SELECT campaign_id, date, device, clicks",
                        "SELECT campaign_id, date, device, clicks, RANK() OVER (...) AS click_rank",
                        "SELECT campaign_id, date, device, clicks, RANK() OVER (PARTITION BY campaign_id ORDER BY clicks DESC) AS click_rank",
                        "SELECT campaign_id, date, device, clicks, RANK() OVER (PARTITION BY campaign_id ORDER BY clicks DESC) AS click_rank FROM ad_performance_daily;"
                    ],
                    "answer": "SELECT campaign_id, date, device, clicks, RANK() OVER (PARTITION BY campaign_id ORDER BY clicks DESC) AS click_rank FROM ad_performance_daily;",
                    "follow_up": "Change RANK to ROW_NUMBER and DENSE_RANK - observe how ties differ"
                },
                {
                    "id": "4.2",
                    "title": "LAG/LEAD & Running Totals",
                    "concept": """Compare rows to previous/next rows in sequence.

{cyan}Functions:{reset}
  LAG(col, n)  -- previous nth row's value
  LEAD(col, n) -- next nth row's value

{green}Google Ads Use:{reset} "Compare today's clicks to yesterday's"

{cyan}Running Totals:{reset}
  SUM() OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)

{yellow}Frame Clauses:{reset}
  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW = cumulative sum
  ROWS BETWEEN 6 PRECEDING AND CURRENT ROW = 7-day rolling window""",
                    "challenge": "For campaign_id = 1, show date, daily total clicks, and previous day's clicks using LAG. First aggregate by date, then apply LAG.",
                    "hints": [
                        "Use a CTE or subquery to first get daily totals",
                        "Filter WHERE campaign_id = 1",
                        "GROUP BY date to get daily totals",
                        "Then apply LAG(daily_clicks, 1) OVER (ORDER BY date)"
                    ],
                    "solution_steps": [
                        "First get daily totals: SELECT date, SUM(clicks) AS daily_clicks FROM ad_performance_daily WHERE campaign_id = 1 GROUP BY date",
                        "Wrap in CTE: WITH daily AS (SELECT date, SUM(clicks) AS daily_clicks FROM ad_performance_daily WHERE campaign_id = 1 GROUP BY date)",
                        "Add LAG: WITH daily AS (...) SELECT date, daily_clicks, LAG(daily_clicks, 1) OVER (ORDER BY date) AS prev_day_clicks FROM daily",
                        "WITH daily AS (SELECT date, SUM(clicks) AS daily_clicks FROM ad_performance_daily WHERE campaign_id = 1 GROUP BY date) SELECT date, daily_clicks, LAG(daily_clicks, 1) OVER (ORDER BY date) AS prev_day_clicks FROM daily ORDER BY date;"
                    ],
                    "answer": "WITH daily AS (SELECT date, SUM(clicks) AS daily_clicks FROM ad_performance_daily WHERE campaign_id = 1 GROUP BY date) SELECT date, daily_clicks, LAG(daily_clicks, 1) OVER (ORDER BY date) AS prev_day_clicks FROM daily ORDER BY date;",
                    "follow_up": "Add day-over-day change: daily_clicks - LAG(...)"
                },
                {
                    "id": "4.3",
                    "title": "CTEs - Clean, Readable Queries",
                    "concept": """CTE (Common Table Expression) = WITH clause. Named temporary result set.

{cyan}Syntax:{reset}
  WITH my_cte AS (
    SELECT ... FROM ... WHERE ...
  )
  SELECT * FROM my_cte;

{green}Why Use CTEs:{reset}
  1. Readability - break complex queries into named steps
  2. Reuse - reference the CTE multiple times
  3. Interview gold - shows organized thinking

{cyan}Chaining CTEs:{reset}
  WITH step1 AS (...),
       step2 AS (SELECT ... FROM step1)
  SELECT * FROM step2;

{yellow}Pro Tip:{reset} In interviews, START with CTEs. Shows structured thinking.""",
                    "challenge": "Use a CTE to calculate total spend and conversions per campaign, then calculate cost per conversion (CPA). Join to campaigns for the name.",
                    "hints": [
                        "Create CTE: WITH campaign_metrics AS (SELECT campaign_id, SUM(cost_micros)/1000000.0 AS total_cost_usd, SUM(conversions) AS total_conversions FROM ad_performance_daily GROUP BY campaign_id)",
                        "In main query, JOIN to campaigns",
                        "Calculate CPA: total_cost_usd / total_conversions",
                        "Use CASE WHEN to avoid divide by zero"
                    ],
                    "solution_steps": [
                        "WITH campaign_metrics AS (SELECT campaign_id, SUM(cost_micros) / 1000000.0 AS total_cost_usd, SUM(conversions) AS total_conversions FROM ad_performance_daily GROUP BY campaign_id)",
                        "WITH campaign_metrics AS (...) SELECT c.campaign_name, cm.total_cost_usd, cm.total_conversions FROM campaign_metrics cm JOIN campaigns c ON cm.campaign_id = c.campaign_id",
                        "WITH campaign_metrics AS (SELECT campaign_id, SUM(cost_micros) / 1000000.0 AS total_cost_usd, SUM(conversions) AS total_conversions FROM ad_performance_daily GROUP BY campaign_id) SELECT c.campaign_name, cm.total_cost_usd, cm.total_conversions, CASE WHEN cm.total_conversions > 0 THEN ROUND(cm.total_cost_usd / cm.total_conversions, 2) ELSE NULL END AS cpa FROM campaign_metrics cm JOIN campaigns c ON cm.campaign_id = c.campaign_id ORDER BY cpa;"
                    ],
                    "answer": "WITH campaign_metrics AS (SELECT campaign_id, SUM(cost_micros) / 1000000.0 AS total_cost_usd, SUM(conversions) AS total_conversions FROM ad_performance_daily GROUP BY campaign_id) SELECT c.campaign_name, cm.total_cost_usd, cm.total_conversions, CASE WHEN cm.total_conversions > 0 THEN ROUND(cm.total_cost_usd / cm.total_conversions, 2) ELSE NULL END AS cpa FROM campaign_metrics cm JOIN campaigns c ON cm.campaign_id = c.campaign_id ORDER BY cpa;",
                    "follow_up": "Add a second CTE for search term waste (terms with 0 conversions)"
                }
            ]
        }
    ]
}

# ============================================================================
# DATABASE CONNECTION
# ============================================================================

DB_PATH = os.path.join(os.path.dirname(__file__), "google_ads.db")
PROGRESS_PATH = os.path.join(os.path.dirname(__file__), "progress.json")

def get_db_connection():
    """Get database connection, creating DB if needed."""
    if not os.path.exists(DB_PATH):
        print(f"{C.YELLOW}Database not found. Running setup...{C.RESET}")
        import setup_db
        setup_db.setup_database()
    return sqlite3.connect(DB_PATH)

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def clear_screen():
    """Clear terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Print the app banner."""
    print(f"""
{C.BRIGHT_BLUE}╔══════════════════════════════════════════════════════════════════╗
║{C.RESET}{C.BOLD}  SQL COACH{C.RESET}{C.BRIGHT_BLUE}  │  {C.BRIGHT_WHITE}Google gTech Ads Interview Prep{C.BRIGHT_BLUE}              ║
╚══════════════════════════════════════════════════════════════════╝{C.RESET}
""")

def print_divider(char="─", color=C.BRIGHT_BLACK):
    """Print a divider line."""
    print(f"{color}{char * 70}{C.RESET}")

def print_box(title, content, color=C.CYAN):
    """Print content in a colored box."""
    print(f"""
{color}╔══════════════════════════════════════════════════════════════════╗
║  {C.BOLD}{title:<64}{C.RESET}{color} ║
╚══════════════════════════════════════════════════════════════════╝{C.RESET}
""")
    # Format content with color codes
    formatted = content.format(
        cyan=C.CYAN, green=C.GREEN, yellow=C.YELLOW, red=C.RED,
        magenta=C.MAGENTA, blue=C.BLUE, dim=C.DIM, bold=C.BOLD,
        reset=C.RESET
    )
    print(formatted)
    print()

def print_success_box(message):
    """Print a success message box."""
    print(f"""
{C.GREEN}╔══════════════════════════════════════════════════════════════════╗
║  {C.BOLD}SUCCESS{C.RESET}{C.GREEN}                                                         ║
╚══════════════════════════════════════════════════════════════════╝{C.RESET}

{message}
""")

def print_error_box(message):
    """Print an error message box."""
    print(f"""
{C.RED}╔══════════════════════════════════════════════════════════════════╗
║  {C.BOLD}ERROR{C.RESET}{C.RED}                                                           ║
╚══════════════════════════════════════════════════════════════════╝{C.RESET}

{message}
""")

def print_hint_box(hint_num, total_hints, hint_text):
    """Print a hint in a styled box."""
    print(f"""
{C.YELLOW}╔══════════════════════════════════════════════════════════════════╗
║  {C.BOLD}HINT {hint_num} of {total_hints}{C.RESET}{C.YELLOW}                                                       ║
╚══════════════════════════════════════════════════════════════════╝{C.RESET}

{hint_text}

{C.DIM}──────────────────────────────────────────────────────────────────
→ Try again, type 'hint' for next hint, or 'answer' for solution
──────────────────────────────────────────────────────────────────{C.RESET}
""")

def print_next_step_box(step_num, total_steps, step_text):
    """Print a solution step."""
    print(f"""
{C.MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║  {C.BOLD}STEP {step_num} of {total_steps}{C.RESET}{C.MAGENTA}                                                       ║
╚══════════════════════════════════════════════════════════════════╝{C.RESET}

{C.BRIGHT_WHITE}{step_text}{C.RESET}

{C.DIM}──────────────────────────────────────────────────────────────────
→ Type 'next' for next step, or 'answer' for full solution
──────────────────────────────────────────────────────────────────{C.RESET}
""")

def print_answer_box(answer):
    """Print the full answer."""
    print(f"""
{C.GREEN}╔══════════════════════════════════════════════════════════════════╗
║  {C.BOLD}FULL SOLUTION{C.RESET}{C.GREEN}                                                     ║
╚══════════════════════════════════════════════════════════════════╝{C.RESET}

{C.BRIGHT_GREEN}{answer}{C.RESET}

{C.DIM}──────────────────────────────────────────────────────────────────
→ Type 'run <sql>' to try it, or 'skip' for next lesson
──────────────────────────────────────────────────────────────────{C.RESET}
""")

def print_table(columns, rows, max_col_width=20):
    """Print a formatted table with colors."""
    if not rows:
        print(f"{C.DIM}(No results){C.RESET}")
        return

    # Calculate column widths
    col_widths = []
    for i, col in enumerate(columns):
        max_width = len(str(col))
        for row in rows:
            if i < len(row):
                max_width = max(max_width, len(str(row[i])[:max_col_width]))
        col_widths.append(min(max_width, max_col_width))

    # Print header
    header_line = f"{C.BRIGHT_CYAN}│{C.RESET}"
    for i, col in enumerate(columns):
        header_line += f" {C.BOLD}{str(col)[:col_widths[i]].ljust(col_widths[i])}{C.RESET} {C.BRIGHT_CYAN}│{C.RESET}"

    separator = f"{C.BRIGHT_CYAN}├" + "┼".join(["─" * (w + 2) for w in col_widths]) + f"┤{C.RESET}"
    top_border = f"{C.BRIGHT_CYAN}┌" + "┬".join(["─" * (w + 2) for w in col_widths]) + f"┐{C.RESET}"
    bottom_border = f"{C.BRIGHT_CYAN}└" + "┴".join(["─" * (w + 2) for w in col_widths]) + f"┘{C.RESET}"

    print(top_border)
    print(header_line)
    print(separator)

    # Print rows
    for row_idx, row in enumerate(rows):
        row_color = C.WHITE if row_idx % 2 == 0 else C.BRIGHT_WHITE
        row_line = f"{C.BRIGHT_CYAN}│{C.RESET}"
        for i, col_width in enumerate(col_widths):
            val = str(row[i]) if i < len(row) else ""
            if val == "None":
                val = f"{C.DIM}NULL{C.RESET}"
                row_line += f" {val.ljust(col_width + len(C.DIM) + len(C.RESET))} {C.BRIGHT_CYAN}│{C.RESET}"
            else:
                row_line += f" {row_color}{val[:col_width].ljust(col_width)}{C.RESET} {C.BRIGHT_CYAN}│{C.RESET}"
        print(row_line)

    print(bottom_border)
    print(f"{C.DIM}{len(rows)} row(s) returned{C.RESET}")

def print_progress_bar(current, total, label="Progress"):
    """Print a colored progress bar."""
    percentage = int((current / total) * 100) if total > 0 else 0
    filled = int((current / total) * 20) if total > 0 else 0
    bar = "█" * filled + "░" * (20 - filled)

    color = C.RED if percentage < 33 else C.YELLOW if percentage < 66 else C.GREEN
    print(f"{label}: {color}{bar}{C.RESET} {percentage}% ({current}/{total})")

def print_schema():
    """Print the database schema with colors."""
    schema = """
{cyan}╔══════════════════════════════════════════════════════════════════╗
║  {bold}DATABASE SCHEMA{reset}{cyan}                                                  ║
╚══════════════════════════════════════════════════════════════════╝{reset}

{yellow}campaigns{reset}
  {green}campaign_id{reset}        INTEGER PRIMARY KEY
  campaign_name      TEXT
  campaign_type      TEXT (SEARCH, DISPLAY, VIDEO, SHOPPING, PMAX)
  status             TEXT (ENABLED, PAUSED)
  daily_budget_micros INTEGER (divide by 1,000,000 for USD)
  bidding_strategy   TEXT
  start_date         DATE

{yellow}ad_groups{reset}
  {green}ad_group_id{reset}        INTEGER PRIMARY KEY
  {blue}campaign_id{reset}        INTEGER → campaigns
  ad_group_name      TEXT
  status             TEXT
  cpc_bid_micros     INTEGER

{yellow}ad_performance_daily{reset}
  id                 INTEGER PRIMARY KEY
  date               DATE
  {blue}campaign_id{reset}        INTEGER → campaigns
  {blue}ad_group_id{reset}        INTEGER → ad_groups
  impressions        INTEGER
  clicks             INTEGER
  cost_micros        INTEGER
  conversions        REAL
  conversion_value   REAL
  device             TEXT (MOBILE, DESKTOP)

{yellow}search_terms{reset}
  id                 INTEGER PRIMARY KEY
  date               DATE
  {blue}campaign_id{reset}        INTEGER → campaigns
  {blue}ad_group_id{reset}        INTEGER → ad_groups
  search_term        TEXT
  impressions        INTEGER
  clicks             INTEGER
  cost_micros        INTEGER
  conversions        REAL

{yellow}conversions{reset}
  {green}conversion_id{reset}      INTEGER PRIMARY KEY
  date               DATE
  {blue}campaign_id{reset}        INTEGER → campaigns
  {blue}ad_group_id{reset}        INTEGER → ad_groups
  conversion_action  TEXT (PURCHASE, SIGN_UP, ADD_TO_CART)
  conversion_value   REAL
  attribution_model  TEXT

{dim}Legend: {green}PK = Primary Key{reset}, {blue}FK = Foreign Key{reset}
Cost columns are in micros (divide by 1,000,000 for USD){reset}
"""
    print(schema.format(
        cyan=C.CYAN, yellow=C.YELLOW, green=C.GREEN, blue=C.BLUE,
        bold=C.BOLD, dim=C.DIM, reset=C.RESET
    ))

# ============================================================================
# PROGRESS TRACKING
# ============================================================================

def load_progress():
    """Load progress from file."""
    if os.path.exists(PROGRESS_PATH):
        with open(PROGRESS_PATH, 'r') as f:
            return json.load(f)
    return {
        "current_lesson": "1.1",
        "completed_lessons": [],
        "hint_counts": {},
        "started_at": datetime.now().isoformat()
    }

def save_progress(progress):
    """Save progress to file."""
    with open(PROGRESS_PATH, 'w') as f:
        json.dump(progress, f, indent=2)

def get_lesson_by_id(lesson_id):
    """Get a lesson by its ID (e.g., '1.2')."""
    for phase in CURRICULUM["phases"]:
        for lesson in phase["lessons"]:
            if lesson["id"] == lesson_id:
                return lesson, phase
    return None, None

def get_next_lesson_id(current_id):
    """Get the next lesson ID."""
    all_lessons = []
    for phase in CURRICULUM["phases"]:
        for lesson in phase["lessons"]:
            all_lessons.append(lesson["id"])

    try:
        idx = all_lessons.index(current_id)
        if idx + 1 < len(all_lessons):
            return all_lessons[idx + 1]
    except ValueError:
        pass
    return None

def get_total_lessons():
    """Get total number of lessons."""
    return sum(len(p["lessons"]) for p in CURRICULUM["phases"])

# ============================================================================
# SQL EXECUTION
# ============================================================================

def execute_sql(sql):
    """Execute SQL and return results."""
    conn = get_db_connection()
    try:
        cursor = conn.execute(sql)
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        rows = cursor.fetchall()
        conn.close()
        return columns, rows, None
    except Exception as e:
        conn.close()
        return None, None, str(e)

def explain_execution_order(sql):
    """Explain the execution order of a SQL query."""
    sql_lower = sql.lower()

    steps = []

    # Determine which clauses are present
    has_cte = "with " in sql_lower
    has_from = "from " in sql_lower
    has_join = "join " in sql_lower
    has_where = "where " in sql_lower
    has_group = "group by" in sql_lower
    has_having = "having " in sql_lower
    has_select = "select " in sql_lower
    has_distinct = "distinct" in sql_lower
    has_order = "order by" in sql_lower
    has_limit = "limit " in sql_lower

    step_num = 1

    if has_cte:
        steps.append(f"{step_num}. {C.CYAN}WITH (CTE){C.RESET}         ← Build temporary result sets first")
        step_num += 1

    if has_from:
        steps.append(f"{step_num}. {C.CYAN}FROM{C.RESET}               ← Load table(s)")
        step_num += 1

    if has_join:
        steps.append(f"{step_num}. {C.CYAN}JOIN{C.RESET}               ← Combine with other tables")
        step_num += 1

    if has_where:
        steps.append(f"{step_num}. {C.YELLOW}WHERE{C.RESET}              ← Filter individual rows")
        step_num += 1

    if has_group:
        steps.append(f"{step_num}. {C.MAGENTA}GROUP BY{C.RESET}           ← Collapse rows into groups")
        step_num += 1

    if has_having:
        steps.append(f"{step_num}. {C.MAGENTA}HAVING{C.RESET}             ← Filter groups")
        step_num += 1

    if has_select:
        steps.append(f"{step_num}. {C.GREEN}SELECT{C.RESET}             ← Compute output columns + aliases")
        step_num += 1

    if has_distinct:
        steps.append(f"{step_num}. {C.GREEN}DISTINCT{C.RESET}           ← Remove duplicates")
        step_num += 1

    if has_order:
        steps.append(f"{step_num}. {C.BLUE}ORDER BY{C.RESET}           ← Sort results (can use aliases)")
        step_num += 1

    if has_limit:
        steps.append(f"{step_num}. {C.BLUE}LIMIT{C.RESET}              ← Restrict row count")
        step_num += 1

    print(f"""
{C.CYAN}╔══════════════════════════════════════════════════════════════════╗
║  {C.BOLD}QUERY EXECUTION ORDER{C.RESET}{C.CYAN}                                           ║
╚══════════════════════════════════════════════════════════════════╝{C.RESET}

{C.DIM}Your query executes in this order:{C.RESET}

""")
    for step in steps:
        print(f"  {step}")
    print()

# ============================================================================
# MAIN APPLICATION
# ============================================================================

class SQLCoach:
    def __init__(self):
        self.progress = load_progress()
        self.current_hint = 0
        self.current_step = 0
        self.last_query = None

    def show_current_lesson(self):
        """Display the current lesson."""
        lesson, phase = get_lesson_by_id(self.progress["current_lesson"])
        if not lesson:
            print_error_box("Lesson not found!")
            return

        # Reset hint/step counters for new lesson
        self.current_hint = 0
        self.current_step = 0

        # Progress bar
        completed = len(self.progress["completed_lessons"])
        total = get_total_lessons()
        print()
        print_progress_bar(completed, total, f"{C.BOLD}Overall Progress{C.RESET}")
        print()

        # Phase and lesson header
        print(f"{C.BRIGHT_MAGENTA}Phase {phase['id']}: {phase['title']}{C.RESET}")
        print(f"{C.BOLD}{C.BRIGHT_WHITE}Lesson {lesson['id']}: {lesson['title']}{C.RESET}")
        print_divider()

        # Concept
        print_box("CONCEPT", lesson["concept"], C.CYAN)

        # Challenge
        print(f"""{C.YELLOW}╔══════════════════════════════════════════════════════════════════╗
║  {C.BOLD}YOUR CHALLENGE{C.RESET}{C.YELLOW}                                                    ║
╚══════════════════════════════════════════════════════════════════╝{C.RESET}

{lesson['challenge']}

{C.DIM}──────────────────────────────────────────────────────────────────
Commands: run <sql> │ hint │ next │ answer │ schema │ help
──────────────────────────────────────────────────────────────────{C.RESET}
""")

    def handle_command(self, cmd):
        """Process user command."""
        cmd = cmd.strip()

        if not cmd:
            return True

        cmd_lower = cmd.lower()
        lesson, phase = get_lesson_by_id(self.progress["current_lesson"])

        # Run SQL
        if cmd_lower.startswith("run "):
            sql = cmd[4:].strip()
            self.last_query = sql
            columns, rows, error = execute_sql(sql)

            if error:
                print_error_box(f"SQL Error:\n{error}")
            else:
                print(f"\n{C.GREEN}Query executed successfully!{C.RESET}\n")
                print_table(columns, rows)

                # Check if matches answer (loosely)
                if lesson and self.normalize_sql(sql) == self.normalize_sql(lesson["answer"]):
                    print_success_box(f"Perfect! That matches the expected solution!\n\n{C.YELLOW}Follow-up:{C.RESET} {lesson.get('follow_up', 'Try the next lesson!')}")
            return True

        # Hint
        if cmd_lower == "hint" or cmd_lower == "stuck" or cmd_lower == "help me":
            if not lesson:
                return True
            hints = lesson.get("hints", [])
            if self.current_hint < len(hints):
                print_hint_box(self.current_hint + 1, len(hints), hints[self.current_hint])
                self.current_hint += 1
            else:
                print(f"{C.YELLOW}No more hints! Type 'answer' to see the solution.{C.RESET}")
            return True

        # Next step
        if cmd_lower == "next":
            if not lesson:
                return True
            steps = lesson.get("solution_steps", [])
            if self.current_step < len(steps):
                print_next_step_box(self.current_step + 1, len(steps), steps[self.current_step])
                self.current_step += 1
            else:
                print(f"{C.YELLOW}No more steps! Here's the full solution:{C.RESET}")
                print_answer_box(lesson["answer"])
            return True

        # Full answer
        if cmd_lower == "answer" or cmd_lower == "solution":
            if lesson:
                print_answer_box(lesson["answer"])
            return True

        # Explain execution
        if cmd_lower == "explain":
            if self.last_query:
                explain_execution_order(self.last_query)
            else:
                print(f"{C.YELLOW}Run a query first, then type 'explain' to see execution order.{C.RESET}")
            return True

        # Schema
        if cmd_lower == "schema":
            print_schema()
            return True

        # Tables list
        if cmd_lower == "tables":
            print(f"\n{C.CYAN}Available Tables:{C.RESET}")
            print(f"  {C.YELLOW}campaigns{C.RESET}            - 6 rows")
            print(f"  {C.YELLOW}ad_groups{C.RESET}            - 8 rows")
            print(f"  {C.YELLOW}ad_performance_daily{C.RESET} - 20 rows")
            print(f"  {C.YELLOW}search_terms{C.RESET}         - 12 rows")
            print(f"  {C.YELLOW}conversions{C.RESET}          - 12 rows")
            print(f"\n{C.DIM}Type 'schema' for full details{C.RESET}\n")
            return True

        # Skip lesson
        if cmd_lower == "skip":
            if lesson:
                if lesson["id"] not in self.progress["completed_lessons"]:
                    self.progress["completed_lessons"].append(lesson["id"])
                next_id = get_next_lesson_id(lesson["id"])
                if next_id:
                    self.progress["current_lesson"] = next_id
                    save_progress(self.progress)
                    clear_screen()
                    print_banner()
                    self.show_current_lesson()
                else:
                    print_success_box("Congratulations! You've completed all lessons!")
            return True

        # Go to specific lesson
        if cmd_lower.startswith("lesson "):
            lesson_id = cmd[7:].strip()
            test_lesson, _ = get_lesson_by_id(lesson_id)
            if test_lesson:
                self.progress["current_lesson"] = lesson_id
                save_progress(self.progress)
                clear_screen()
                print_banner()
                self.show_current_lesson()
            else:
                print_error_box(f"Lesson '{lesson_id}' not found. Use format like '1.2' or '3.1'")
            return True

        # Progress
        if cmd_lower == "progress":
            completed = len(self.progress["completed_lessons"])
            total = get_total_lessons()
            print(f"\n{C.BOLD}Your Progress:{C.RESET}\n")
            print_progress_bar(completed, total)
            print(f"\n{C.DIM}Completed lessons: {', '.join(self.progress['completed_lessons']) or 'None yet'}{C.RESET}")
            print(f"{C.DIM}Current lesson: {self.progress['current_lesson']}{C.RESET}\n")
            return True

        # Reset
        if cmd_lower == "reset":
            self.current_hint = 0
            self.current_step = 0
            print(f"{C.GREEN}Lesson progress reset. Hints and steps start from beginning.{C.RESET}")
            return True

        # Help
        if cmd_lower == "help" or cmd_lower == "?":
            print(f"""
{C.CYAN}╔══════════════════════════════════════════════════════════════════╗
║  {C.BOLD}COMMANDS{C.RESET}{C.CYAN}                                                          ║
╚══════════════════════════════════════════════════════════════════╝{C.RESET}

  {C.GREEN}run <sql>{C.RESET}     Execute SQL query and see results
  {C.YELLOW}hint{C.RESET}          Get a hint (progressive, multiple available)
  {C.YELLOW}next{C.RESET}          Show next part of solution step-by-step
  {C.YELLOW}answer{C.RESET}        Show the full solution
  {C.CYAN}explain{C.RESET}       Explain execution order of last query
  {C.CYAN}schema{C.RESET}        Show database schema
  {C.CYAN}tables{C.RESET}        List all tables
  {C.MAGENTA}lesson X.Y{C.RESET}    Jump to specific lesson (e.g., lesson 2.1)
  {C.MAGENTA}progress{C.RESET}      Show your overall progress
  {C.MAGENTA}skip{C.RESET}          Skip to next lesson
  {C.DIM}reset{C.RESET}         Reset hint/step counters for current lesson
  {C.DIM}clear{C.RESET}         Clear screen and show current lesson
  {C.RED}quit{C.RESET}          Exit the coach
""")
            return True

        # Clear
        if cmd_lower == "clear" or cmd_lower == "cls":
            clear_screen()
            print_banner()
            self.show_current_lesson()
            return True

        # Quit
        if cmd_lower in ["quit", "exit", "q"]:
            save_progress(self.progress)
            print(f"\n{C.GREEN}Progress saved! See you next time.{C.RESET}\n")
            return False

        # Unknown command - try as SQL
        if any(kw in cmd_lower for kw in ["select", "with", "insert", "update", "delete"]):
            self.last_query = cmd
            columns, rows, error = execute_sql(cmd)
            if error:
                print_error_box(f"SQL Error:\n{error}")
            else:
                print(f"\n{C.GREEN}Query executed!{C.RESET}\n")
                print_table(columns, rows)
        else:
            print(f"{C.YELLOW}Unknown command. Type 'help' for available commands.{C.RESET}")

        return True

    def normalize_sql(self, sql):
        """Normalize SQL for comparison."""
        return re.sub(r'\s+', ' ', sql.lower().strip().rstrip(';'))

    def run(self):
        """Main loop."""
        clear_screen()
        print_banner()

        print(f"""
{C.BRIGHT_WHITE}Welcome to SQL Coach!{C.RESET}

This tool will help you master SQL for your Google gTech Ads interview.
Work through lessons, get hints when stuck, and see solutions step-by-step.

{C.DIM}Type 'help' anytime to see all commands.{C.RESET}
""")

        self.show_current_lesson()

        while True:
            try:
                cmd = input(f"\n{C.BRIGHT_BLUE}sql>{C.RESET} ")
                if not self.handle_command(cmd):
                    break
            except KeyboardInterrupt:
                print(f"\n\n{C.GREEN}Progress saved! Goodbye.{C.RESET}\n")
                save_progress(self.progress)
                break
            except EOFError:
                break

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Enable ANSI colors on Windows
    if os.name == 'nt':
        os.system('color')
        # Also try to enable ANSI via Windows API
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except:
            pass

    coach = SQLCoach()
    coach.run()
