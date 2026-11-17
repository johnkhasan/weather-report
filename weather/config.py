"""Project-wide settings: cities, date range and reference period."""

CITIES = {
    "Tashkent": (41.31, 69.28),
    "Milan": (45.46, 9.19),
    "Oslo": (59.91, 10.75),
}

START_DATE = "1950-01-01"
END_DATE = "2025-12-31"

# 1961–1990 is the standard WMO reference period for climate normals
BASELINE_YEARS = (1961, 1990)
