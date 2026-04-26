"""
Reading Schedule Data
Parsed from ReadingSchedule-REGandLEAP.pdf (GVCC Three-Column Plan)
Format: SCHEDULE[(month, day)] = [reading1, reading2, reading3]
"""

SCHEDULE = {}

# ──────────────────────────────────────────────────────────────
# JANUARY  (OT: Genesis–Exodus, Psalms: 1–17, NT: Matthew–Mark)
# ──────────────────────────────────────────────────────────────
_jan = [
    (1,  ["Genesis 1-2",      "Psalms 1",       "Matthew 1-2"]),
    (2,  ["Genesis 3-4",      "Psalms 2",       "Matthew 3-4"]),
    (3,  ["Genesis 5-6",      "Psalms 3",       "Matthew 5-6"]),
    (4,  ["Genesis 7-8",      "Psalms 4",       "Matthew 7-8"]),
    (5,  ["Genesis 9-10",     "Psalms 5",       "Matthew 9-10"]),
    (6,  ["Genesis 11",       "Psalms 6",       "Matthew 11"]),
    (7,  ["Genesis 12",       "Psalms 7",       "Matthew 12"]),
    (8,  ["Genesis 13-14",    "Psalms 8",       "Matthew 13"]),
    (9,  ["Genesis 15",       "Psalms 9",       "Matthew 14-15"]),
    (10, ["Genesis 16",       "Psalms 10",      "Matthew 16-17"]),
    (11, ["Genesis 17",       "Psalms 11",      "Matthew 18-19"]),
    (12, ["Genesis 18",       "Psalms 12",      "Matthew 20-21"]),
    (13, ["Genesis 19",       "Psalms 13",      "Matthew 22"]),
    (14, ["Genesis 20",       "Psalms 14",      "Matthew 23"]),
    (15, ["Genesis 21",       "Psalms 15",      "Matthew 24"]),
    (16, ["Genesis 22",       "Psalms 16",      "Matthew 25"]),
    (17, ["Genesis 23",       "Psalms 17",      "Matthew 26"]),
    (18, ["Genesis 24",       "Psalms 18",      "Matthew 27-28"]),
    (19, ["Genesis 25",       "Psalms 19",      "Mark 1"]),
    (20, ["Genesis 26",       "Psalms 20",      "Mark 2-3"]),
    (21, ["Genesis 27-28",    "Psalms 21",      "Mark 4"]),
    (22, ["Genesis 29",       "Psalms 22",      "Mark 5-6"]),
    (23, ["Genesis 30",       "Psalms 23",      "Mark 7-8"]),
    (24, ["Genesis 31",       "Psalms 24",      "Mark 9-10"]),
    (25, ["Genesis 32",       "Psalms 25",      "Mark 11-12"]),
    (26, ["Genesis 33",       "Psalms 26",      "Mark 13-14"]),
    (27, ["Genesis 34",       "Psalms 27",      "Mark 15-16"]),
    (28, ["Genesis 35",       "Psalms 28",      "Romans 1"]),
    (29, ["Genesis 36",       "Psalms 29",      "Romans 2"]),
    (30, ["Genesis 37",       "Psalms 30",      "Romans 3-4"]),
    (31, ["Genesis 38",       "Psalms 31",      "Romans 5-6"]),
]
for d, r in _jan:
    SCHEDULE[(1, d)] = r

# ──────────────────────────────────────────────────────────────
# FEBRUARY  (OT: Genesis–Exodus, Psalms: 32–38, NT: Romans)
# ──────────────────────────────────────────────────────────────
_feb = [
    (1,  ["Genesis 39",       "Psalms 32",      "Romans 7-8"]),
    (2,  ["Genesis 40",       "Psalms 33",      "Romans 9-10"]),
    (3,  ["Genesis 41",       "Psalms 34",      "Romans 11-12"]),
    (4,  ["Genesis 42",       "Psalms 35",      "Romans 13-14"]),
    (5,  ["Genesis 43",       "Psalms 36",      "Romans 15-16"]),
    (6,  ["Genesis 44",       "Psalms 37",      "1 Corinthians 1-2"]),
    (7,  ["Genesis 45-46",    "Psalms 38",      "1 Corinthians 3-4"]),
    (8,  ["Genesis 47-48",    "Psalms 39",      "1 Corinthians 5-6"]),
    (9,  ["Genesis 49-50",    "Psalms 40",      "1 Corinthians 7"]),
    (10, ["Exodus 1-2",       "Psalms 41",      "1 Corinthians 8-9"]),
    (11, ["Exodus 3-4",       "Psalms 42-43",   "1 Corinthians 10-11"]),
    (12, ["Exodus 5",         "Psalms 44",      "1 Corinthians 12-14"]),
    (13, ["Exodus 6-7",       "Psalms 45",      "1 Corinthians 15"]),
    (14, ["Exodus 8",         "Psalms 46",      "1 Corinthians 16"]),
    (15, ["Exodus 9",         "Psalms 47-48",   "2 Corinthians 1-2"]),
    (16, ["Exodus 10-11",     "Psalms 49",      "2 Corinthians 3-4"]),
    (17, ["Exodus 12",        "Psalms 50",      "2 Corinthians 5-6"]),
    (18, ["Exodus 13-14",     "Psalms 51-52",   "2 Corinthians 7-8"]),
    (19, ["Exodus 15",        "Psalms 53-54",   "2 Corinthians 9-10"]),
    (20, ["Exodus 16-17",     "Psalms 55",      "2 Corinthians 11-12"]),
    (21, ["Exodus 18-19",     "Psalms 56",      "2 Corinthians 13"]),
    (22, ["Exodus 20",        "Psalms 57",      "Galatians 1-2"]),
    (23, ["Exodus 21",        "Psalms 58",      "Galatians 3-4"]),
    (24, ["Exodus 22",        "Psalms 59-60",   "Galatians 5-6"]),
    (25, ["Exodus 23",        "Psalms 61-62",   "Ephesians 1-2"]),
    (26, ["Exodus 24-25",     "Psalms 63",      "Ephesians 3-4"]),
    (27, ["Exodus 26",        "Psalms 64",      "Ephesians 5-6"]),
    (28, ["Exodus 27",        "Psalms 65",      "Philippians 1-2"]),
    (29, ["Exodus 28-29",     "Psalms 66",      "Philippians 3-4"]),  # leap year
]
for d, r in _feb:
    SCHEDULE[(2, d)] = r

# ──────────────────────────────────────────────────────────────
# MARCH  (from PDF page 2 — verbatim)
# ──────────────────────────────────────────────────────────────
_mar = [
    (1,  ["Exodus 26-27",     "Psalms 39",      "Romans 2-3"]),
    (2,  ["Exodus 28-29",     "Psalms 40",      "Romans 4-6"]),
    (3,  ["Exodus 30",        "Psalms 41",      "Romans 7-8"]),
    (4,  ["Exodus 31-32",     "Psalms 42-43",   "Romans 9-10"]),
    (5,  ["Exodus 33-34",     "Psalms 44",      "Romans 11-12"]),
    (6,  ["Exodus 35",        "Psalms 45",      "Romans 13-14"]),
    (7,  ["Exodus 36-37",     "Psalms 46",      "Romans 15-16"]),
    (8,  ["Exodus 38",        "Psalms 47-48",   "1 Corinthians 1-2"]),
    (9,  ["Exodus 39",        "Psalms 49",      "1 Corinthians 3-4"]),
    (10, ["Exodus 40",        "Psalms 50",      "1 Corinthians 5-6"]),
    (11, ["Leviticus 1-2",    "Psalms 51-52",   "1 Corinthians 7"]),
    (12, ["Leviticus 3-4",    "Psalms 53-54",   "1 Corinthians 8-9"]),
    (13, ["Leviticus 5",      "Psalms 55",      "1 Corinthians 10-11"]),
    (14, ["Leviticus 6",      "Psalms 56",      "1 Corinthians 12-14"]),
    (15, ["Leviticus 7",      "Psalms 57",      "1 Corinthians 15"]),
    (16, ["Leviticus 8-9",    "Psalms 58",      "1 Corinthians 16"]),
    (17, ["Leviticus 10",     "Psalms 59-60",   "2 Corinthians 1-2"]),
    (18, ["Leviticus 11-12",  "Psalms 61-62",   "2 Corinthians 3"]),
    (19, ["Leviticus 13",     "Psalms 63",      "2 Corinthians 4-5"]),
    (20, ["Leviticus 14",     "Psalms 64",      "2 Corinthians 6-7"]),
    (21, ["Leviticus 15",     "Psalms 65-66",   "2 Corinthians 8-9"]),
    (22, ["Leviticus 16",     "Psalms 67-68",   "2 Corinthians 10"]),
    (23, ["Leviticus 17",     "Psalms 69",      "2 Corinthians 11-12"]),
    (24, ["Leviticus 18-19",  "Psalms 70-71",   "2 Corinthians 13"]),
    (25, ["Leviticus 20",     "Psalms 72",      "Galatians 1-2"]),
    (26, ["Leviticus 21",     "Psalms 73",      "Galatians 3-4"]),
    (27, ["Leviticus 22",     "Psalms 74",      "Galatians 5-6"]),
    (28, ["Leviticus 23",     "Psalms 75-76",   "Ephesians 1-2"]),
    (29, ["Leviticus 24",     "Psalms 77",      "Ephesians 3"]),
    (30, ["Leviticus 25",     "Psalms 78",      "Ephesians 4"]),
    (31, ["Leviticus 26",     "Psalms 79",      "Ephesians 5"]),
]
for d, r in _mar:
    SCHEDULE[(3, d)] = r

# ──────────────────────────────────────────────────────────────
# APRIL  (from PDF page 2 — verbatim)
# ──────────────────────────────────────────────────────────────
_apr = [
    (1,  ["Leviticus 27",     "Psalms 80",      "Ephesians 6"]),
    (2,  ["Numbers 1",        "Psalms 81",      "Philippians 1-2"]),
    (3,  ["Numbers 2",        "Psalms 82",      "Philippians 3-4"]),
    (4,  ["Numbers 3",        "Psalms 83",      "Colossians 1-2"]),
    (5,  ["Numbers 4",        "Psalms 84",      "Colossians 3-4"]),
    (6,  ["Numbers 5",        "Psalms 85",      "1 Thessalonians 1-2"]),
    (7,  ["Numbers 6",        "Psalms 86",      "1 Thessalonians 3-4"]),
    (8,  ["Numbers 7",        "Psalms 87",      "1 Thessalonians 5"]),
    (9,  ["Numbers 8-9",      "Psalms 88",      "2 Thessalonians 1-3"]),
    (10, ["Numbers 10",       "Psalms 89",      "1 Timothy 1-2"]),
    (11, ["Numbers 11-12",    "Psalms 90",      "1 Timothy 3-4"]),
    (12, ["Numbers 13",       "Psalms 91-92",   "1 Timothy 5-6"]),
    (13, ["Numbers 14",       "Psalms 93",      "2 Timothy 1-2"]),
    (14, ["Numbers 15",       "Psalms 94",      "2 Timothy 3-4"]),
    (15, ["Numbers 16",       "Psalms 95",      "Titus 1-3"]),
    (16, ["Numbers 17-18",    "Psalms 96-97",   "Philemon"]),
    (17, ["Numbers 19",       "Psalms 98",      "Luke 1"]),
    (18, ["Numbers 20",       "Psalms 99-100",  "Luke 2"]),
    (19, ["Numbers 21",       "Psalms 101-102", "Luke 3"]),
    (20, ["Numbers 22",       "Psalms 103",     "Luke 4"]),
    (21, ["Numbers 23",       "Psalms 104",     "Luke 5"]),
    (22, ["Numbers 24",       "Psalms 105",     "Luke 6"]),
    (23, ["Numbers 25",       "Psalms 106",     "Luke 7"]),
    (24, ["Numbers 26",       "Psalms 107",     "Luke 8"]),
    (25, ["Numbers 27",       "Psalms 108",     "Luke 9"]),
    (26, ["Numbers 28",       "Psalms 109",     "Luke 10"]),
    (27, ["Numbers 29-30",    "Psalms 110",     "Luke 11"]),
    (28, ["Numbers 31",       "Psalms 111",     "Luke 12"]),
    (29, ["Numbers 32",       "Psalms 112-113", "Luke 13-14"]),
    (30, ["Numbers 33-34",    "Psalms 114-115", "Luke 15-16"]),
]
for d, r in _apr:
    SCHEDULE[(4, d)] = r

# ──────────────────────────────────────────────────────────────
# MAY  (from PDF page 2 — verbatim)
# ──────────────────────────────────────────────────────────────
_may = [
    (1,  ["Numbers 35-36",        "Psalms 116",            "Luke 17"]),
    (2,  ["Deuteronomy 1",        "Psalms 117-118",        "Luke 18"]),
    (3,  ["Deuteronomy 2",        "Psalms 119:1-24",       "Luke 19"]),
    (4,  ["Deuteronomy 3",        "Psalms 119:25-40",      "Luke 20"]),
    (5,  ["Deuteronomy 4",        "Psalms 119:41-64",      "Luke 21"]),
    (6,  ["Deuteronomy 5",        "Psalms 119:65-80",      "Luke 22"]),
    (7,  ["Deuteronomy 6",        "Psalms 119:81-104",     "Luke 23"]),
    (8,  ["Deuteronomy 7-8",      "Psalms 119:105-120",    "Luke 24"]),
    (9,  ["Deuteronomy 9",        "Psalms 119:121-136",    "Acts 1-2"]),
    (10, ["Deuteronomy 10",       "Psalms 119:137-160",    "Acts 3-4"]),
    (11, ["Deuteronomy 11",       "Psalms 119:161-176",    "Acts 5"]),
    (12, ["Deuteronomy 12",       "Psalms 120",            "Acts 6-7"]),
    (13, ["Deuteronomy 13-14",    "Psalms 121-122",        "Acts 8"]),
    (14, ["Deuteronomy 15-16",    "Psalms 123-124",        "Acts 9"]),
    (15, ["Deuteronomy 17-18",    "Psalms 125-126",        "Acts 10"]),
    (16, ["Deuteronomy 19-20",    "Psalms 127-128",        "Acts 11-12"]),
    (17, ["Deuteronomy 21",       "Psalms 129",            "Acts 13"]),
    (18, ["Deuteronomy 22",       "Psalms 130",            "Acts 14-15"]),
    (19, ["Deuteronomy 23-24",    "Psalms 131",            "Acts 16"]),
    (20, ["Deuteronomy 25",       "Psalms 132",            "Acts 17-18"]),
    (21, ["Deuteronomy 26-27",    "Psalms 133",            "Acts 19"]),
    (22, ["Deuteronomy 28",       "Psalms 134",            "Acts 20"]),
    (23, ["Deuteronomy 29",       "Psalms 135",            "Acts 21-22"]),
    (24, ["Deuteronomy 30",       "Psalms 136",            "Acts 23-24"]),
    (25, ["Deuteronomy 31",       "Psalms 137",            "Acts 25-26"]),
    (26, ["Deuteronomy 32",       "Psalms 138",            "Acts 27"]),
    (27, ["Deuteronomy 33-34",    "Psalms 139",            "Acts 28"]),
    (28, ["Joshua 1",             "Psalms 140-141",        "John 1"]),
    (29, ["Joshua 2",             "Psalms 142-143",        "John 2-3"]),
    (30, ["Joshua 3-4",           "Psalms 144",            "John 4"]),
    (31, ["Joshua 5",             "Psalms 145-146",        "John 5"]),
]
for d, r in _may:
    SCHEDULE[(5, d)] = r

# ──────────────────────────────────────────────────────────────
# JUNE  (from PDF page 2 — verbatim)
# ──────────────────────────────────────────────────────────────
_jun = [
    (1,  ["Joshua 6",         "Psalms 147",     "John 6"]),
    (2,  ["Joshua 7-8",       "Psalms 148",     "John 7"]),
    (3,  ["Joshua 9",         "Psalms 149-150", "John 8"]),
    (4,  ["Joshua 10",        "Proverbs 1",     "John 9"]),
    (5,  ["Joshua 11-12",     "Proverbs 2",     "John 10"]),
    (6,  ["Joshua 13",        "Proverbs 3",     "John 11"]),
    (7,  ["Joshua 14",        "Proverbs 4",     "John 12"]),
    (8,  ["Joshua 15",        "Proverbs 5",     "John 13"]),
    (9,  ["Joshua 16-17",     "Proverbs 6",     "John 14"]),
    (10, ["Joshua 18",        "Proverbs 7",     "John 15-16"]),
    (11, ["Joshua 19",        "Proverbs 8",     "John 17"]),
    (12, ["Joshua 20-21",     "Proverbs 9",     "John 18"]),
    (13, ["Joshua 22",        "Proverbs 10",    "John 19"]),
    (14, ["Joshua 23",        "Proverbs 11",    "John 20-21"]),
    (15, ["Joshua 24",        "Proverbs 12",    "Revelation 1-2"]),
    (16, ["Judges 1-2",       "Proverbs 13",    "Revelation 3"]),
    (17, ["Judges 3",         "Proverbs 14",    "Revelation 4-5"]),
    (18, ["Judges 4-5",       "Proverbs 15",    "Revelation 6"]),
    (19, ["Judges 6",         "Proverbs 16",    "Revelation 7-8"]),
    (20, ["Judges 7",         "Proverbs 17",    "Revelation 9-10"]),
    (21, ["Judges 8",         "Proverbs 18",    "Revelation 11-12"]),
    (22, ["Judges 9",         "Proverbs 19",    "Revelation 13"]),
    (23, ["Judges 10",        "Proverbs 20",    "Revelation 14-15"]),
    (24, ["Judges 11-12",     "Proverbs 21",    "Revelation 16"]),
    (25, ["Judges 13-14",     "Proverbs 22",    "Revelation 17"]),
    (26, ["Judges 15",        "Proverbs 23",    "Revelation 18"]),
    (27, ["Judges 16",        "Proverbs 24",    "Revelation 19"]),
    (28, ["Judges 17",        "Proverbs 25",    "Revelation 20"]),
    (29, ["Judges 18",        "Proverbs 26",    "Revelation 21"]),
    (30, ["Judges 19",        "Proverbs 27",    "Revelation 22"]),
]
for d, r in _jun:
    SCHEDULE[(6, d)] = r

# ──────────────────────────────────────────────────────────────
# JULY  (OT: Judges–Samuel, Wisdom lit, NT: Hebrews–James)
# ──────────────────────────────────────────────────────────────
_jul = [
    (1,  ["Judges 20",        "Proverbs 28",    "Hebrews 1-2"]),
    (2,  ["Judges 21",        "Proverbs 29",    "Hebrews 3-4"]),
    (3,  ["Ruth 1",           "Proverbs 30",    "Hebrews 5-6"]),
    (4,  ["Ruth 2-3",         "Proverbs 31",    "Hebrews 7-8"]),
    (5,  ["Ruth 4",           "Ecclesiastes 1", "Hebrews 9-10"]),
    (6,  ["1 Samuel 1",       "Ecclesiastes 2", "Hebrews 11"]),
    (7,  ["1 Samuel 2",       "Ecclesiastes 3", "Hebrews 12-13"]),
    (8,  ["1 Samuel 3",       "Ecclesiastes 4", "James 1"]),
    (9,  ["1 Samuel 4-5",     "Ecclesiastes 5", "James 2-3"]),
    (10, ["1 Samuel 6-7",     "Ecclesiastes 6", "James 4-5"]),
    (11, ["1 Samuel 8",       "Ecclesiastes 7", "1 Peter 1-2"]),
    (12, ["1 Samuel 9",       "Ecclesiastes 8", "1 Peter 3-5"]),
    (13, ["1 Samuel 10",      "Ecclesiastes 9", "2 Peter 1-3"]),
    (14, ["1 Samuel 11-12",   "Ecclesiastes 10","1 John 1-2"]),
    (15, ["1 Samuel 13",      "Ecclesiastes 11","1 John 3-4"]),
    (16, ["1 Samuel 14",      "Ecclesiastes 12","1 John 5"]),
    (17, ["1 Samuel 15",      "Song of Sol. 1", "2 John"]),
    (18, ["1 Samuel 16",      "Song of Sol. 2", "3 John"]),
    (19, ["1 Samuel 17",      "Song of Sol. 3", "Jude"]),
    (20, ["1 Samuel 18",      "Song of Sol. 4", "Romans 1-2"]),
    (21, ["1 Samuel 19-20",   "Song of Sol. 5", "Romans 3-4"]),
    (22, ["1 Samuel 21",      "Song of Sol. 6", "Romans 5-6"]),
    (23, ["1 Samuel 22",      "Song of Sol. 7", "Romans 7-8"]),
    (24, ["1 Samuel 23",      "Song of Sol. 8", "Romans 9-10"]),
    (25, ["1 Samuel 24-25",   "Isaiah 1",       "Romans 11-12"]),
    (26, ["1 Samuel 26-27",   "Isaiah 2",       "Romans 13-14"]),
    (27, ["1 Samuel 28-29",   "Isaiah 3-4",     "Romans 15-16"]),
    (28, ["1 Samuel 30-31",   "Isaiah 5",       "1 Corinthians 1-2"]),
    (29, ["2 Samuel 1-2",     "Isaiah 6",       "1 Corinthians 3-4"]),
    (30, ["2 Samuel 3-4",     "Isaiah 7",       "1 Corinthians 5-6"]),
    (31, ["2 Samuel 5",       "Isaiah 8",       "1 Corinthians 7"]),
]
for d, r in _jul:
    SCHEDULE[(7, d)] = r

# ──────────────────────────────────────────────────────────────
# AUGUST  (OT: Samuel–Kings, Isaiah, NT: 1 Cor–Romans)
# ──────────────────────────────────────────────────────────────
_aug = [
    (1,  ["2 Samuel 6",       "Isaiah 9",       "1 Corinthians 8-9"]),
    (2,  ["2 Samuel 7",       "Isaiah 10",      "1 Corinthians 10-11"]),
    (3,  ["2 Samuel 8-9",     "Isaiah 11-12",   "1 Corinthians 12-14"]),
    (4,  ["2 Samuel 10",      "Isaiah 13",      "1 Corinthians 15"]),
    (5,  ["2 Samuel 11-12",   "Isaiah 14",      "1 Corinthians 16"]),
    (6,  ["2 Samuel 13",      "Isaiah 15",      "2 Corinthians 1-2"]),
    (7,  ["2 Samuel 14",      "Isaiah 16",      "2 Corinthians 3-4"]),
    (8,  ["2 Samuel 15",      "Isaiah 17-18",   "2 Corinthians 5-6"]),
    (9,  ["2 Samuel 16",      "Isaiah 19-20",   "2 Corinthians 7-8"]),
    (10, ["2 Samuel 17",      "Isaiah 21-22",   "2 Corinthians 9-10"]),
    (11, ["2 Samuel 18",      "Isaiah 23",      "2 Corinthians 11-12"]),
    (12, ["2 Samuel 19",      "Isaiah 24",      "2 Corinthians 13"]),
    (13, ["2 Samuel 20",      "Isaiah 25-26",   "Galatians 1-2"]),
    (14, ["2 Samuel 21",      "Isaiah 27",      "Galatians 3-4"]),
    (15, ["2 Samuel 22",      "Isaiah 28",      "Galatians 5-6"]),
    (16, ["2 Samuel 23",      "Isaiah 29",      "Ephesians 1-2"]),
    (17, ["2 Samuel 24",      "Isaiah 30",      "Ephesians 3-4"]),
    (18, ["1 Kings 1",        "Isaiah 31-32",   "Ephesians 5-6"]),
    (19, ["1 Kings 2",        "Isaiah 33-34",   "Philippians 1-2"]),
    (20, ["1 Kings 3",        "Isaiah 35",      "Philippians 3-4"]),
    (21, ["1 Kings 4",        "Isaiah 36",      "Colossians 1-2"]),
    (22, ["1 Kings 5",        "Isaiah 37",      "Colossians 3-4"]),
    (23, ["1 Kings 6",        "Isaiah 38",      "1 Thessalonians 1-3"]),
    (24, ["1 Kings 7",        "Isaiah 39",      "1 Thessalonians 4-5"]),
    (25, ["1 Kings 8",        "Isaiah 40",      "2 Thessalonians 1-3"]),
    (26, ["1 Kings 9",        "Isaiah 41",      "1 Timothy 1-2"]),
    (27, ["1 Kings 10",       "Isaiah 42",      "1 Timothy 3-4"]),
    (28, ["1 Kings 11",       "Isaiah 43",      "1 Timothy 5-6"]),
    (29, ["1 Kings 12",       "Isaiah 44",      "2 Timothy 1-2"]),
    (30, ["1 Kings 13",       "Isaiah 45",      "2 Timothy 3-4"]),
    (31, ["1 Kings 14",       "Isaiah 46-47",   "Titus 1-3"]),
]
for d, r in _aug:
    SCHEDULE[(8, d)] = r

# ──────────────────────────────────────────────────────────────
# SEPTEMBER  (from PDF page 1 — verbatim)
# ──────────────────────────────────────────────────────────────
_sep = [
    (1,  ["1 Kings 15",       "Isaiah 65",      "Romans 7-8"]),
    (2,  ["1 Kings 16",       "Isaiah 66",      "Romans 9-10"]),
    (3,  ["1 Kings 17",       "Jeremiah 1-2",   "Romans 11"]),
    (4,  ["1 Kings 18",       "Jeremiah 3",     "Romans 12-13"]),
    (5,  ["1 Kings 19",       "Jeremiah 4",     "Romans 14-15"]),
    (6,  ["1 Kings 20",       "Jeremiah 5",     "Romans 16"]),
    (7,  ["1 Kings 21",       "Jeremiah 6",     "1 Corinthians 1-2"]),
    (8,  ["1 Kings 22",       "Jeremiah 7",     "1 Corinthians 3"]),
    (9,  ["2 Kings 1-2",      "Jeremiah 8-9",   "1 Corinthians 4"]),
    (10, ["2 Kings 3",        "Jeremiah 10",    "1 Corinthians 5-6"]),
    (11, ["2 Kings 4",        "Jeremiah 11",    "1 Corinthians 7"]),
    (12, ["2 Kings 5",        "Jeremiah 12-14", "1 Corinthians 8-9"]),
    (13, ["2 Kings 6",        "Jeremiah 14",    "1 Corinthians 10-11"]),
    (14, ["2 Kings 7",        "Jeremiah 15",    "1 Corinthians 12-14"]),
    (15, ["2 Kings 8",        "Jeremiah 16",    "1 Corinthians 15"]),
    (16, ["2 Kings 9",        "Jeremiah 17",    "1 Corinthians 16"]),
    (17, ["2 Kings 10",       "Jeremiah 18-19", "2 Corinthians 1-2"]),
    (18, ["2 Kings 11-12",    "Jeremiah 20-21", "2 Corinthians 3"]),
    (19, ["2 Kings 13",       "Jeremiah 22",    "2 Corinthians 4-5"]),
    (20, ["2 Kings 14",       "Jeremiah 23",    "2 Corinthians 6-7"]),
    (21, ["2 Kings 15",       "Jeremiah 24",    "2 Corinthians 8-10"]),
    (22, ["2 Kings 16",       "Jeremiah 25",    "2 Corinthians 11-12"]),
    (23, ["2 Kings 17",       "Jeremiah 26-27", "2 Corinthians 13"]),
    (24, ["2 Kings 18-19",    "Jeremiah 28",    "Galatians 1"]),
    (25, ["2 Kings 20",       "Jeremiah 29-30", "Galatians 2"]),
    (26, ["2 Kings 21",       "Jeremiah 31",    "Galatians 3-4"]),
    (27, ["2 Kings 22",       "Jeremiah 32",    "Galatians 5-6"]),
    (28, ["2 Kings 23",       "Jeremiah 33",    "Ephesians 1-2"]),
    (29, ["2 Kings 24-25",    "Jeremiah 34",    "Ephesians 3"]),
    (30, ["1 Chronicles 1-2", "Jeremiah 35-36", "Ephesians 4-5"]),
]
for d, r in _sep:
    SCHEDULE[(9, d)] = r

# ──────────────────────────────────────────────────────────────
# OCTOBER  (from PDF page 1 — verbatim)
# ──────────────────────────────────────────────────────────────
_oct = [
    (1,  ["1 Chronicles 3",   "Jeremiah 37-38", "Ephesians 6"]),
    (2,  ["1 Chronicles 4",   "Jeremiah 39",    "Philippians 1-2"]),
    (3,  ["1 Chronicles 5",   "Jeremiah 40-41", "Philippians 3-4"]),
    (4,  ["1 Chronicles 6",   "Jeremiah 42-43", "Colossians 1"]),
    (5,  ["1 Chronicles 7",   "Jeremiah 44",    "Colossians 2"]),
    (6,  ["1 Chronicles 8",   "Jeremiah 45-46", "Colossians 3"]),
    (7,  ["1 Chronicles 9",   "Jeremiah 47",    "1 Thessalonians 1-3"]),
    (8,  ["1 Chronicles 10",  "Jeremiah 48",    "1 Thessalonians 4-5"]),
    (9,  ["1 Chronicles 11",  "Jeremiah 49",    "2 Thessalonians 1"]),
    (10, ["1 Chronicles 12",  "Jeremiah 50",    "2 Thessalonians 2-3"]),
    (11, ["1 Chronicles 13",  "Jeremiah 51",    "1 Timothy 1-2"]),
    (12, ["1 Chronicles 14",  "Jeremiah 52",    "1 Timothy 3-4"]),
    (13, ["1 Chronicles 15",  "Lamentations 1", "1 Timothy 5-6"]),
    (14, ["1 Chronicles 16",  "Lamentations 2", "2 Timothy 1-2"]),
    (15, ["1 Chronicles 17",  "Lamentations 3", "2 Timothy 3-4"]),
    (16, ["1 Chronicles 18",  "Lamentations 4", "Titus 1-3"]),
    (17, ["1 Chronicles 19",  "Lamentations 5", "Philemon"]),
    (18, ["1 Chronicles 20",  "Ezekiel 1",      "Luke 1"]),
    (19, ["1 Chronicles 21",  "Ezekiel 2",      "Luke 2"]),
    (20, ["1 Chronicles 22",  "Ezekiel 3",      "Luke 3"]),
    (21, ["1 Chronicles 23",  "Ezekiel 4-5",    "Luke 4"]),
    (22, ["1 Chronicles 24",  "Ezekiel 6-7",    "Luke 5"]),
    (23, ["1 Chronicles 25",  "Ezekiel 8",      "Luke 6"]),
    (24, ["1 Chronicles 26",  "Ezekiel 9",      "Luke 7"]),
    (25, ["1 Chronicles 27",  "Ezekiel 10",     "Luke 8"]),
    (26, ["1 Chronicles 28",  "Ezekiel 11",     "Luke 9"]),
    (27, ["1 Chronicles 29",  "Ezekiel 12",     "Luke 10"]),
    (28, ["2 Chronicles 1",   "Ezekiel 13",     "Luke 11"]),
    (29, ["2 Chronicles 2",   "Ezekiel 14",     "Luke 12"]),
    (30, ["2 Chronicles 3",   "Ezekiel 15",     "Luke 13"]),
    (31, ["2 Chronicles 4",   "Ezekiel 16",     "Luke 14"]),
]
for d, r in _oct:
    SCHEDULE[(10, d)] = r

# ──────────────────────────────────────────────────────────────
# NOVEMBER  (from PDF page 1 — verbatim)
# ──────────────────────────────────────────────────────────────
_nov = [
    (1,  ["2 Chronicles 5",   "Ezekiel 17",     "Luke 15"]),
    (2,  ["2 Chronicles 6",   "Ezekiel 18",     "Luke 16"]),
    (3,  ["2 Chronicles 7",   "Ezekiel 19",     "Luke 17"]),
    (4,  ["2 Chronicles 8",   "Ezekiel 20",     "Luke 18"]),
    (5,  ["2 Chronicles 9",   "Ezekiel 21-22",  "Luke 19"]),
    (6,  ["2 Chronicles 10",  "Ezekiel 23",     "Luke 20"]),
    (7,  ["2 Chronicles 11",  "Ezekiel 24",     "Luke 21"]),
    (8,  ["2 Chronicles 12",  "Ezekiel 25-26",  "Luke 22"]),
    (9,  ["2 Chronicles 13",  "Ezekiel 27",     "Luke 23"]),
    (10, ["2 Chronicles 14",  "Ezekiel 28-29",  "Luke 24"]),
    (11, ["2 Chronicles 15",  "Ezekiel 30-31",  "Acts 1-2"]),
    (12, ["2 Chronicles 16",  "Ezekiel 32",     "Acts 3-4"]),
    (13, ["2 Chronicles 17",  "Ezekiel 33-34",  "Acts 5"]),
    (14, ["2 Chronicles 18",  "Ezekiel 35",     "Acts 6-7"]),
    (15, ["2 Chronicles 19",  "Ezekiel 36",     "Acts 8"]),
    (16, ["2 Chronicles 20",  "Ezekiel 37-38",  "Acts 9"]),
    (17, ["2 Chronicles 21",  "Ezekiel 39",     "Acts 10"]),
    (18, ["2 Chronicles 22",  "Ezekiel 40",     "Acts 11-12"]),
    (19, ["2 Chronicles 23",  "Ezekiel 41-42",  "Acts 13"]),
    (20, ["2 Chronicles 24",  "Ezekiel 43",     "Acts 14-15"]),
    (21, ["2 Chronicles 25",  "Ezekiel 44-45",  "Acts 16"]),
    (22, ["2 Chronicles 26",  "Ezekiel 46",     "Acts 17-18"]),
    (23, ["2 Chronicles 27",  "Ezekiel 47-48",  "Acts 19"]),
    (24, ["2 Chronicles 28",  "Daniel 1-2",     "Acts 20"]),
    (25, ["2 Chronicles 29",  "Daniel 3-4",     "Acts 21-22"]),
    (26, ["2 Chronicles 30",  "Daniel 5-6",     "Acts 23-24"]),
    (27, ["2 Chronicles 31",  "Daniel 7-8",     "Acts 25"]),
    (28, ["2 Chronicles 32",  "Daniel 9-10",    "Acts 26"]),
    (29, ["2 Chronicles 33",  "Daniel 11-12",   "Acts 27"]),
    (30, ["2 Chronicles 34",  "Hosea 1-2",      "Acts 28"]),
]
for d, r in _nov:
    SCHEDULE[(11, d)] = r

# ──────────────────────────────────────────────────────────────
# DECEMBER  (from PDF page 1 — verbatim)
# ──────────────────────────────────────────────────────────────
_dec = [
    (1,  ["2 Chronicles 35",  "Hosea 3-5",      "John 1"]),
    (2,  ["2 Chronicles 36",  "Hosea 6-8",      "John 2"]),
    (3,  ["Ezra 1",           "Hosea 9-10",     "John 3"]),
    (4,  ["Ezra 2",           "Hosea 11",       "John 4"]),
    (5,  ["Ezra 3",           "Hosea 12-14",    "John 5"]),
    (6,  ["Ezra 4",           "Joel 1-2",       "John 6"]),
    (7,  ["Ezra 5",           "Joel 3",         "John 7"]),
    (8,  ["Ezra 6",           "Amos 1-3",       "John 8"]),
    (9,  ["Ezra 7",           "Amos 4-5",       "John 9"]),
    (10, ["Ezra 8",           "Amos 6-7",       "John 10"]),
    (11, ["Ezra 9",           "Amos 8-9",       "John 11"]),
    (12, ["Ezra 10",          "Obadiah",        "John 12"]),
    (13, ["Nehemiah 1",       "Jonah 1-2",      "John 13"]),
    (14, ["Nehemiah 2",       "Jonah 3-4",      "John 14-15"]),
    (15, ["Nehemiah 3",       "Micah 1-2",      "John 16"]),
    (16, ["Nehemiah 4",       "Micah 3-4",      "John 17"]),
    (17, ["Nehemiah 5",       "Micah 5-7",      "John 18"]),
    (18, ["Nehemiah 6",       "Nahum 1-3",      "John 19"]),
    (19, ["Nehemiah 7",       "Habakkuk 1-3",   "John 20"]),
    (20, ["Nehemiah 8",       "Zephaniah 1-3",  "John 21"]),
    (21, ["Nehemiah 9",       "Haggai 1-2",     "Revelation 1-2"]),
    (22, ["Nehemiah 10",      "Zechariah 1",    "Revelation 3-4"]),
    (23, ["Nehemiah 11",      "Zechariah 2-3",  "Revelation 5-6"]),
    (24, ["Nehemiah 12",      "Zechariah 4-5",  "Revelation 7-8"]),
    (25, ["Nehemiah 13",      "Zechariah 6-7",  "Revelation 9-10"]),
    (26, ["Esther 1",         "Zechariah 8",    "Revelation 11-12"]),
    (27, ["Esther 2",         "Zechariah 9-11", "Revelation 13-14"]),
    (28, ["Esther 3-4",       "Zechariah 12-13","Revelation 15-16"]),
    (29, ["Esther 5-6",       "Zechariah 14",   "Revelation 17-18"]),
    (30, ["Esther 7-8",       "Malachi 1-2",    "Revelation 19-20"]),
    (31, ["Esther 9-10",      "Malachi 3-4",    "Revelation 21-22"]),
]
for d, r in _dec:
    SCHEDULE[(12, d)] = r


def get_readings(month: int, day: int) -> list[str]:
    """Return the three readings for a given month/day, or [] if not found."""
    return SCHEDULE.get((month, day), [])


def get_today_readings() -> list[str]:
    from datetime import date
    today = date.today()
    return get_readings(today.month, today.day)


# Common Bible cross-references (seed data for suggestions)
CROSS_REFERENCES = {
    "John 3:16":      ["Romans 5:8", "1 John 4:9", "Ephesians 2:4-5"],
    "Romans 8:28":    ["Genesis 50:20", "Jeremiah 29:11", "Philippians 4:13"],
    "Psalms 23:1":    ["John 10:11", "Ezekiel 34:11", "Isaiah 40:11"],
    "Galatians 3:28": ["Colossians 3:11", "Romans 10:12", "1 Corinthians 12:13"],
    "Ephesians 2:8":  ["Romans 3:23-24", "Titus 3:5", "Acts 15:11"],
    "Philippians 4:13":["2 Corinthians 12:9", "Isaiah 40:31", "John 15:5"],
    "Proverbs 3:5":   ["Psalms 37:5", "Isaiah 26:3", "Matthew 6:33"],
    "Isaiah 40:31":   ["Psalms 27:14", "Galatians 6:9", "Philippians 4:13"],
    "Matthew 6:33":   ["Proverbs 3:5-6", "Luke 12:31", "Psalms 37:4"],
    "Leviticus 19:18":["Matthew 22:39", "Romans 13:9", "Galatians 5:14"],
}
