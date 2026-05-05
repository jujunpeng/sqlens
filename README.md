# sqlens

> CLI tool that parses and visualizes query execution plans from PostgreSQL and MySQL in a readable terminal format.

---

## Installation

```bash
pip install sqlens
```

Or install from source:

```bash
git clone https://github.com/yourname/sqlens.git && cd sqlens && pip install .
```

---

## Usage

Pipe a query directly into `sqlens` or pass a file containing an `EXPLAIN` output:

```bash
# PostgreSQL
psql -U user -d mydb -c "EXPLAIN ANALYZE SELECT * FROM orders WHERE status = 'pending';" | sqlens

# MySQL
mysql -u user -p mydb -e "EXPLAIN SELECT * FROM orders WHERE status = 'pending';" | sqlens --dialect mysql

# From a file
sqlens --file plan.txt --dialect postgres
```

**Example output:**

```
┌─ Seq Scan on orders  [cost=0.00..431.20 rows=1140 width=174]
│   Filter: (status = 'pending')
│   Rows Removed by Filter: 8860
│
└─ Planning Time: 0.8 ms  |  Execution Time: 3.2 ms
```

### Options

| Flag | Description |
|------|-------------|
| `--dialect` | Database dialect: `postgres` (default) or `mysql` |
| `--file` | Path to a saved EXPLAIN output file |
| `--format` | Output style: `tree` (default) or `json` |
| `--no-color` | Disable colored terminal output |

---

## Requirements

- Python 3.8+
- PostgreSQL 12+ or MySQL 8.0+

---

## License

MIT © 2024 [yourname](https://github.com/yourname)