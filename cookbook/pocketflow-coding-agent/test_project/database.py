"""Simple CSV-based database loader."""

import csv
import os

_tables = {}

def load_csv(name, filepath):
    """Load a CSV file as a named table."""
    rows = []
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Auto-convert numeric fields
            converted = {}
            for k, v in row.items():
                if v == "":
                    converted[k] = None
                else:
                    try:
                        converted[k] = int(v)
                    except ValueError:
                        try:
                            converted[k] = float(v)
                        except ValueError:
                            converted[k] = v
            rows.append(converted)
    _tables[name] = rows
    return rows

def get_table(name):
    """Return loaded table by name."""
    if name not in _tables:
        raise ValueError(f"Table \'{name}\' not loaded. Call load_csv first.")
    return [dict(r) for r in _tables[name]]

def init_db(data_dir=None):
    """Load all CSV files from data_dir (defaults to script directory)."""
    if data_dir is None:
        data_dir = os.path.dirname(os.path.abspath(__file__))
    for fname in os.listdir(data_dir):
        if fname.endswith(".csv"):
            table_name = fname[:-4]
            load_csv(table_name, os.path.join(data_dir, fname))
    return list(_tables.keys())

def reset():
    """Clear all loaded tables."""
    _tables.clear()
