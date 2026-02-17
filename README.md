# SQL Coach

An interactive CLI tool for practicing SQL with a focus on ad tech data patterns. Designed for learning SQL concepts through realistic business scenarios, featuring a structured curriculum, progressive hints, and automatic progress tracking.

## Why SQL Coach?

Most SQL practice tools use generic datasets and provide answers immediately. SQL Coach is different:

- **Ad Tech Context**: Practice with realistic advertising data (campaigns, ad groups, performance metrics, cost in micros)
- **Progressive Hints**: Learn to ask clarifying questions before coding—building strong problem-solving skills
- **Guided Learning**: Hints reveal in stages (questions → approach → concept → code) to build understanding
- **Structured Curriculum**: 13 lessons across 4 phases, building from basics to window functions

## Features

- **13 lessons** across 4 phases: Foundations, Aggregation, JOINs, Window Functions & CTEs
- **Progressive hints**: Clarifying questions, approach guidance, conceptual hints, then code hints
- **Step-by-step solutions**: See the solution build incrementally
- **Progress tracking**: Automatically saves your progress between sessions
- **Colored terminal UI**: Clear visual hierarchy with formatted output
- **Execution order explainer**: Understand why WHERE runs before SELECT

## Requirements

- Python 3.7 or higher
- Terminal with ANSI color support (most modern terminals)

No external dependencies required—uses only Python standard library.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/BTECHK/sql-coach.git
cd sql-coach

# Set up the database (creates google_ads.db)
python setup_db.py

# Start the coach
python sql_coach.py
```

## Commands

| Command | Description |
|---------|-------------|
| `run <sql>` | Execute SQL and see results |
| `<sql>` | Execute SQL directly (auto-detected) |
| `hint` | Get progressive hints (guided learning) |
| `next` | Show next step of the solution |
| `answer` | Show full solution |
| `explain` | Explain execution order of last query |
| `schema` | Show database schema |
| `tables` | List all tables |
| `lesson X.Y` | Jump to specific lesson (e.g., `lesson 2.1`) |
| `progress` | Show your overall progress |
| `skip` | Skip to next lesson |
| `reset` | Reset hints for current lesson |
| `clear` | Clear screen and redisplay lesson |
| `help` | Show all commands |
| `quit` | Exit (progress auto-saved) |

## Curriculum

### Phase 1: Foundations
| Lesson | Topic | Key Concepts |
|--------|-------|--------------|
| 1.1 | SELECT & FROM | Basic queries, column selection |
| 1.2 | WHERE | Filtering rows, operators, AND/OR |
| 1.3 | ORDER BY & LIMIT | Sorting, top-N queries |
| 1.4 | Execution Order | Why aliases work in ORDER BY but not WHERE |

### Phase 2: Aggregation
| Lesson | Topic | Key Concepts |
|--------|-------|--------------|
| 2.1 | Aggregate Functions | SUM, COUNT, AVG, MIN, MAX |
| 2.2 | GROUP BY | Aggregating by category |
| 2.3 | HAVING | Filtering groups vs filtering rows |

### Phase 3: JOINs
| Lesson | Topic | Key Concepts |
|--------|-------|--------------|
| 3.1 | INNER JOIN | Matching rows from both tables |
| 3.2 | LEFT JOIN | Keeping all rows from left table, COALESCE |
| 3.3 | Multi-Table JOINs | Chaining 3+ tables, correct join keys |

### Phase 4: Window Functions & CTEs
| Lesson | Topic | Key Concepts |
|--------|-------|--------------|
| 4.1 | Window Functions | ROW_NUMBER, RANK, DENSE_RANK, PARTITION BY |
| 4.2 | LAG/LEAD | Comparing to previous/next rows |
| 4.3 | CTEs | WITH clauses for readable queries |

## Database Schema

The practice database uses realistic advertising data:

```
campaigns (6 rows)
├── campaign_id (PK)
├── campaign_name
├── campaign_type (SEARCH, DISPLAY, VIDEO, SHOPPING, PMAX)
├── status (ENABLED, PAUSED)
├── daily_budget_micros
├── bidding_strategy
└── start_date

ad_groups (8 rows)
├── ad_group_id (PK)
├── campaign_id (FK → campaigns)
├── ad_group_name
├── status
└── cpc_bid_micros

ad_performance_daily (20 rows)
├── id (PK)
├── date
├── campaign_id (FK → campaigns)
├── ad_group_id (FK → ad_groups)
├── impressions
├── clicks
├── cost_micros
├── conversions
├── conversion_value
└── device (MOBILE, DESKTOP)

search_terms (12 rows)
├── id (PK)
├── date
├── campaign_id, ad_group_id (FKs)
├── search_term
├── impressions, clicks, cost_micros, conversions

conversions (12 rows)
├── conversion_id (PK)
├── date
├── campaign_id, ad_group_id (FKs)
├── conversion_action (PURCHASE, SIGN_UP, ADD_TO_CART)
├── conversion_value
└── attribution_model
```

**Note**: Cost columns are in micros (divide by 1,000,000 for USD).

## Example Session

```
sql> SELECT campaign_name, SUM(clicks) as total_clicks
     FROM campaigns c
     JOIN ad_performance_daily p ON c.campaign_id = p.campaign_id
     GROUP BY campaign_name;

Query executed successfully!
┌───────────────────┬──────────────┐
│ campaign_name     │ total_clicks │
├───────────────────┼──────────────┤
│ Brand_Search_US   │ 5230         │
│ Competitor_Search │ 950          │
│ Display_Remarketing│ 4690        │
└───────────────────┴──────────────┘
3 row(s) returned
```

## Learning Tips Included

Each lesson includes practical guidance:

- **Common traps**: "You CANNOT use column aliases from SELECT in WHERE!"
- **BigQuery tips**: "SELECT * costs money! Always select only columns you need."
- **Query patterns**: "Find the top N..." = ORDER BY + LIMIT
- **Execution order**: Understanding why HAVING exists separately from WHERE

## Documentation

- [PRD.md](PRD.md) - Full product requirements document

## Contributing

Contributions welcome! Areas for improvement:

- Additional lessons (subqueries, CASE statements, date functions)
- More practice challenges per lesson
- Alternative datasets (e-commerce, SaaS metrics)
- Web-based version

## License

PolyForm Noncommercial 1.0.0 - Free for personal and noncommercial use. Commercial use requires permission. See [LICENSE](LICENSE) for details.

## Author

Created by [BTECHK](https://github.com/BTECHK)
