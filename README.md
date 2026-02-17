# SQL Coach

An interactive CLI tool for practicing SQL with a focus on Google Ads data patterns. Features a structured curriculum, progressive hints, and automatic progress tracking.

## Features

- **13 lessons** across 4 phases: Foundations, Aggregation, JOINs, Window Functions & CTEs
- **Interview-style hints**: Clarifying questions, approach guidance, conceptual hints, then code hints
- **Step-by-step solutions**: See the solution build incrementally
- **Progress tracking**: Automatically saves your progress
- **Google Ads context**: Practice with realistic ad tech data (campaigns, ad groups, performance metrics)

## Quick Start

```bash
# Set up the database
python setup_db.py

# Start the coach
python sql_coach.py
```

## Commands

| Command | Description |
|---------|-------------|
| `run <sql>` | Execute SQL and see results |
| `hint` | Get progressive hints (interview-style) |
| `next` | Show next step of the solution |
| `answer` | Show full solution |
| `explain` | Explain execution order of last query |
| `schema` | Show database schema |
| `tables` | List all tables |
| `lesson X.Y` | Jump to specific lesson |
| `progress` | Show your progress |
| `skip` | Skip to next lesson |
| `help` | Show all commands |

## Curriculum

### Phase 1: Foundations
- SELECT & FROM
- WHERE (filtering rows)
- ORDER BY & LIMIT
- Execution order

### Phase 2: Aggregation
- Aggregate functions (SUM, COUNT, AVG)
- GROUP BY
- HAVING vs WHERE

### Phase 3: JOINs
- INNER JOIN
- LEFT JOIN
- Multi-table JOINs

### Phase 4: Window Functions & CTEs
- ROW_NUMBER, RANK, DENSE_RANK
- LAG/LEAD
- Common Table Expressions (WITH clause)

## Database Schema

The practice database simulates Google Ads data:

- **campaigns** - Campaign settings (name, type, budget, bidding strategy)
- **ad_groups** - Ad groups within campaigns
- **ad_performance_daily** - Daily metrics (impressions, clicks, cost, conversions)
- **search_terms** - Search term report data
- **conversions** - Conversion tracking data

## License

MIT License - see [LICENSE](LICENSE) for details.
