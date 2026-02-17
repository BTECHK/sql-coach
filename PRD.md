# SQL Coach - Product Requirements Document

**Version:** 1.0
**Author:** BTECHK
**Date:** February 2025
**Status:** Released

---

## 1. Overview

### 1.1 Problem Statement

Technical interview candidates preparing for Google gTech Ads roles struggle to practice SQL effectively because generic SQL tutorials don't cover ad tech-specific data patterns, and existing resources don't simulate the interview experience where candidates must ask clarifying questions before diving into code.

**Customer Quote Evidence:**
> "I know SQL basics, but I freeze up in interviews when I see unfamiliar table structures. I wish I could practice with realistic ad data and learn to think through problems the way interviewers expect."
> — Technical interview candidate

### 1.2 Opportunity

Google gTech Ads Technical Solutions Consultant roles require strong SQL skills with specific patterns: micros-based currency, campaign hierarchies, device segmentation, and window functions for ranking/comparison. The interview process explicitly tests for structured problem-solving, not just correct answers. No existing tool combines realistic ad tech data with interview-style progressive hints.

### 1.3 Solution Summary

SQL Coach is an interactive CLI tool that teaches SQL through 13 structured lessons using Google Ads-style data. It provides interview-style progressive hints (clarifying questions → approach → conceptual hints → code hints) that train users to think like interviewers expect, plus automatic progress tracking.

### 1.4 Success Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Primary: Lesson completion rate | 80%+ users complete Phase 1-2 | Progress.json tracking |
| Secondary: Hint dependency | <3 hints average per lesson | Hint count tracking |
| Guardrail: Time to first query | <2 minutes per lesson | User observation |

---

## 2. Target Users

### 2.1 Primary User Persona

**Name:** Interview Prepper
**Segment:** Technical candidates preparing for Google gTech Ads or similar ad tech roles

**Demographics:**
- 2-5 years technical experience
- Familiar with SQL basics but not ad tech patterns
- Preparing for interviews within 1-4 weeks

**Jobs to be Done:**

| Job Type | Job Statement | Priority |
|----------|---------------|----------|
| Functional | Practice SQL with realistic ad tech data structures | P0 |
| Functional | Learn to ask clarifying questions before writing queries | P0 |
| Emotional | Feel confident walking into technical interviews | P0 |
| Social | Demonstrate structured problem-solving to interviewers | P1 |

**Pain Points (from research):**
1. Generic SQL tutorials don't cover ad tech patterns - "LeetCode SQL problems are nothing like what I see in ad tech interviews"
2. No practice with interview format - "I know the SQL but I don't know how to approach the problem out loud"

**Current Alternatives:**
- LeetCode/HackerRank - Why it fails: Generic problems, no ad tech context, no interview-style thinking
- YouTube tutorials - Why it fails: Passive learning, can't practice interactively
- Google BigQuery documentation - Why it fails: Reference material, not structured learning

**Success Criteria (in their words):**
> "I want to walk into the interview knowing I've seen these exact types of problems and practiced thinking through them the right way."

### 2.2 Anti-Personas (Who This Is NOT For)

- **Complete SQL beginners** - Why: Assumes basic SELECT/FROM knowledge
- **Experienced ad tech analysts** - Why: Content is introductory to intermediate
- **Non-interview contexts** - Why: Hint system is specifically designed for interview prep

---

## 3. User Stories & Requirements

### 3.1 Epic Overview

| Epic | Description | Priority | JTBD Mapping |
|------|-------------|----------|--------------|
| Epic 1: Structured Curriculum | 13 lessons across 4 phases with progressive difficulty | P0 | Practice SQL with realistic data |
| Epic 2: Interview-Style Hints | Progressive hint system mimicking interview dialogue | P0 | Learn to ask clarifying questions |
| Epic 3: Progress Tracking | Save/resume progress across sessions | P1 | Complete curriculum over multiple sessions |
| Epic 4: Query Execution | Run SQL against realistic ad data | P0 | Practice with realistic data |

### 3.2 Detailed User Stories

**Epic 1: Structured Curriculum**

| ID | User Story | Acceptance Criteria | Priority |
|----|------------|---------------------|----------|
| US-001 | As a learner, I want lessons organized by topic so I can build skills progressively | - 4 phases: Foundations, Aggregation, JOINs, Window Functions<br>- Each phase builds on previous | P0 |
| US-002 | As a learner, I want each lesson to explain concepts before challenging me | - Concept section with syntax examples<br>- Google Ads context provided<br>- Interview tips included | P0 |
| US-003 | As a learner, I want realistic challenges that mirror interview questions | - Challenges use ad tech terminology<br>- Multiple tables involved<br>- Real-world scenarios | P0 |

**Epic 2: Interview-Style Hints**

| ID | User Story | Acceptance Criteria | Priority |
|----|------------|---------------------|----------|
| US-004 | As a learner, I want hints that teach me to ask clarifying questions | - First hints are questions to ask interviewer<br>- Approach guidance before code | P0 |
| US-005 | As a learner, I want progressive hints so I don't see the answer immediately | - Minimum 4 hint levels<br>- Code hints only after conceptual hints | P0 |
| US-006 | As a learner, I want step-by-step solution building | - Solutions shown incrementally<br>- Can see full answer when ready | P1 |

**Epic 3: Progress Tracking**

| ID | User Story | Acceptance Criteria | Priority |
|----|------------|---------------------|----------|
| US-007 | As a learner, I want my progress saved automatically | - Progress persists across sessions<br>- Can resume where I left off | P1 |
| US-008 | As a learner, I want to see my overall progress | - Progress bar showing completion<br>- List of completed lessons | P1 |
| US-009 | As a learner, I want to jump to any lesson | - `lesson X.Y` command works<br>- Can skip ahead or review | P2 |

**Epic 4: Query Execution**

| ID | User Story | Acceptance Criteria | Priority |
|----|------------|---------------------|----------|
| US-010 | As a learner, I want to run SQL and see results immediately | - Queries execute against real database<br>- Results displayed in formatted table | P0 |
| US-011 | As a learner, I want to understand query execution order | - `explain` command shows execution order<br>- Helps debug WHERE vs HAVING issues | P1 |

### 3.3 Feature Requirements Matrix

| Feature | User Story | Must Have | Should Have | Nice to Have |
|---------|------------|-----------|-------------|--------------|
| 13-lesson curriculum | US-001 | X | | |
| Concept explanations | US-002 | X | | |
| Progressive hints | US-004, US-005 | X | | |
| SQL execution | US-010 | X | | |
| Progress persistence | US-007 | | X | |
| Execution order explain | US-011 | | X | |
| Lesson navigation | US-009 | | | X |

---

## 4. Functional Requirements

### 4.1 Core Functionality

**Curriculum System**

| Requirement ID | Requirement | Rationale | Priority |
|----------------|-------------|-----------|----------|
| FR-001 | Display lesson concept with formatted text and examples | Users need context before attempting challenges | P0 |
| FR-002 | Present challenge clearly separated from concept | Clear delineation between learning and practice | P0 |
| FR-003 | Support phase/lesson hierarchy (e.g., 3.2 = Phase 3, Lesson 2) | Organized progression | P0 |

**Hint System**

| Requirement ID | Requirement | Rationale | Priority |
|----------------|-------------|-----------|----------|
| FR-004 | Provide hints in order: clarifying questions → approach → conceptual → code | Mimics interview dialogue | P0 |
| FR-005 | Track hint usage per lesson | Measure learning efficiency | P1 |
| FR-006 | Provide step-by-step solution reveal via `next` command | Allows incremental learning | P1 |

**Query Execution**

| Requirement ID | Requirement | Rationale | Priority |
|----------------|-------------|-----------|----------|
| FR-007 | Execute SQL against SQLite database | Real query practice | P0 |
| FR-008 | Display results in formatted ASCII table | Readable output | P0 |
| FR-009 | Detect correct answers and auto-advance | Positive reinforcement | P1 |
| FR-010 | Show helpful error messages on SQL errors | Learning from mistakes | P0 |

### 4.2 User Flows

**Flow 1: Complete a Lesson**
```
Step 1: User starts SQL Coach
   → User sees: Banner, progress bar, current lesson concept
   → System does: Loads progress.json, displays lesson

Step 2: User reads concept and challenge
   → User sees: Formatted concept with examples, challenge prompt
   → System does: Waits for input

Step 3: User attempts query (or requests hint)
   → User sees: Query results or hint
   → System does: Executes SQL or displays next hint

Step 4: User gets correct answer
   → User sees: Success message, follow-up suggestion
   → System does: Marks lesson complete, saves progress

Step 5: User advances to next lesson
   → User sees: Next lesson content
   → System does: Updates current_lesson, resets hint counter

Success State: Lesson marked complete in progress.json
Error States: SQL syntax error (show message), no more hints (suggest answer)
```

### 4.3 Edge Cases & Error Handling

| Scenario | Expected Behavior | Priority |
|----------|-------------------|----------|
| SQL syntax error | Display error message, allow retry | P0 |
| All hints exhausted | Suggest using `answer` command | P0 |
| Database file missing | Auto-run setup_db.py | P1 |
| Invalid lesson ID | Show error, list valid IDs | P2 |

---

## 5. Non-Functional Requirements

### 5.1 Performance

| Requirement | Target | Measurement |
|-------------|--------|-------------|
| Query execution time | < 100ms | SQLite local |
| Application startup | < 2 seconds | Manual test |
| Progress save | Instant (JSON write) | Manual test |

### 5.2 Compatibility

- Python 3.7+
- Windows, macOS, Linux
- Terminal with ANSI color support

### 5.3 Data Requirements

| Data Entity | Source | Storage | Retention |
|-------------|--------|---------|-----------|
| Lesson content | Embedded in code | sql_coach.py | Permanent |
| Practice data | Generated | google_ads.db | Regenerable |
| User progress | User-generated | progress.json | User-controlled |

---

## 6. Technical Architecture

### 6.1 Components

```
sql_coach.py          # Main application, curriculum, UI
setup_db.py           # Database initialization
google_ads.db         # SQLite database (generated)
progress.json         # User progress (generated)
```

### 6.2 Database Schema

| Table | Purpose | Row Count |
|-------|---------|-----------|
| campaigns | Campaign dimension table | 6 |
| ad_groups | Ad group dimension table | 8 |
| ad_performance_daily | Fact table with metrics | 20 |
| search_terms | Search term report | 12 |
| conversions | Conversion tracking | 12 |

### 6.3 Data Patterns Covered

- Micros-based currency (divide by 1,000,000)
- Campaign → Ad Group hierarchy
- Device segmentation (MOBILE, DESKTOP)
- Date-based performance data
- NULL handling in aggregations

---

## 7. UX/UI Requirements

### 7.1 Design Principles

1. **Clear visual hierarchy** - Colored boxes distinguish concepts, challenges, hints, results
2. **Progressive disclosure** - Don't overwhelm; reveal information as needed
3. **Immediate feedback** - Query results appear instantly

### 7.2 Key Screens/Views

| Screen | Purpose | Key Elements |
|--------|---------|--------------|
| Lesson view | Primary learning interface | Progress bar, concept box, challenge box, command prompt |
| Results view | Query output | Formatted ASCII table, row count |
| Hint view | Progressive help | Hint category, hint number, hint content |
| Success view | Positive reinforcement | Success box, follow-up suggestion |

### 7.3 Color Coding

| Element | Color | Purpose |
|---------|-------|---------|
| Concept boxes | Cyan | Information |
| Challenge boxes | Yellow | Action needed |
| Success messages | Green | Positive feedback |
| Errors | Red | Attention needed |
| Hints | Yellow/Magenta | Help content |

---

## 8. Curriculum Detail

### Phase 1: Foundations (Lessons 1.1-1.4)
- SELECT & FROM basics
- WHERE filtering
- ORDER BY & LIMIT
- Execution order understanding

### Phase 2: Aggregation (Lessons 2.1-2.3)
- SUM, COUNT, AVG functions
- GROUP BY mechanics
- HAVING vs WHERE

### Phase 3: JOINs (Lessons 3.1-3.3)
- INNER JOIN
- LEFT JOIN with COALESCE
- Multi-table JOINs

### Phase 4: Advanced (Lessons 4.1-4.3)
- Window functions (ROW_NUMBER, RANK, DENSE_RANK)
- LAG/LEAD for comparisons
- CTEs for readable queries

---

## 9. Success Criteria

### 9.1 Activation Metric
- **Event:** User completes first lesson (1.1)
- **Target:** 90% of users who start

### 9.2 Completion Metric
- **Event:** User completes all 13 lessons
- **Target:** 50% of activated users

### 9.3 Learning Efficiency
- **Metric:** Average hints per lesson
- **Target:** < 3 hints for lessons after Phase 1

---

## 10. Future Considerations

| Feature | Description | Priority |
|---------|-------------|----------|
| Additional lessons | Subqueries, CASE statements, date functions | P2 |
| Timed mode | Simulate interview time pressure | P3 |
| Custom datasets | Allow users to practice with their own data | P3 |
| Web version | Browser-based for easier access | P3 |

---

## 11. Appendices

### 11.1 Competitive Analysis

| Feature | SQL Coach | LeetCode | Mode Analytics |
|---------|-----------|----------|----------------|
| Ad tech context | ✓ | ✗ | ✗ |
| Interview-style hints | ✓ | ✗ | ✗ |
| Progressive curriculum | ✓ | ✓ | ✓ |
| Free | ✓ | Partial | Partial |
| Offline capable | ✓ | ✗ | ✗ |

### 11.2 Google Ads SQL Patterns Covered

- Micros to USD conversion
- Campaign/Ad Group hierarchy queries
- Device-level performance analysis
- Cost per conversion (CPA) calculations
- Period-over-period comparisons (LAG)
- Ranking within partitions
