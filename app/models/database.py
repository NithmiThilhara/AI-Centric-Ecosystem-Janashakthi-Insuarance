import sqlite3
from contextlib import contextmanager


def get_db(db_path):
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    return db


@contextmanager
def db_connection(db_path):
    db = get_db(db_path)
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db(db_path):
    with db_connection(db_path) as db:
        db.executescript('''
            CREATE TABLE IF NOT EXISTS customers (
                id          TEXT PRIMARY KEY,
                nic         TEXT UNIQUE NOT NULL,
                full_name   TEXT NOT NULL,
                phone       TEXT,
                email       TEXT,
                address     TEXT,
                date_of_birth TEXT,
                created_at  TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS policies (
                id             TEXT PRIMARY KEY,
                policy_number  TEXT UNIQUE NOT NULL,
                customer_id    TEXT NOT NULL,
                plan           TEXT NOT NULL,
                branch         TEXT NOT NULL,
                status         TEXT DEFAULT "Active",
                premium_mode   TEXT DEFAULT "Monthly",
                sum_assured    REAL,
                start_date     TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            );

            CREATE TABLE IF NOT EXISTS service_requests (
                id                TEXT PRIMARY KEY,
                customer_id       TEXT,
                policy_number     TEXT,
                service_type      TEXT NOT NULL,
                status            TEXT DEFAULT "Pending",
                ai_notes          TEXT,
                underwriter_notes TEXT,
                created_at        TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at        TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            );

            CREATE TABLE IF NOT EXISTS documents (
                id          TEXT PRIMARY KEY,
                request_id  TEXT NOT NULL,
                doc_type    TEXT NOT NULL,
                file_path   TEXT NOT NULL,
                ai_verified INTEGER DEFAULT 0,
                ai_feedback TEXT,
                uploaded_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (request_id) REFERENCES service_requests(id)
            );
        ''')

        _seed_data(db)


# ─────────────────────────────────────────────────
# SEED DATA — 30 customers, 32 policies
# ─────────────────────────────────────────────────

CUSTOMERS = [
    # ── Original 10 (unchanged) ──────────────────────────────────────────────
    ("C001", "881324008V", "B.A.N.M. Balasooriya",    "0712345678", "tharindra0622@gmail.com",   "No 15, Negombo",                           "1988-03-24"),
    ("C002", "971742534V", "P.A.K.D. Fonseka",        "0723456789", "sathyani19103@gmail.com",         "No 04, Meegalandiya, Makolagama, Oelgama", "1997-06-22"),
    ("C003", "756234521V", "M.D. Samarawickrama",     "0734567890", "samara@email.com",          "No 25, 3rd Lane, Flower Road, Colombo 03", "1975-09-15"),
    ("C004", "852341267V", "K.L.S. Perera",           "0745678901", "perera@email.com",          "No 45, Main Street, Kandy",                "1985-11-30"),
    ("C005", "902156789V", "H.M.T. Dilrukshi",        "0756789012", "dilrukshi@email.com",       "No 328, Dambulla Road, Matale",            "1990-04-12"),
    ("C006", "781234567V", "R.M.N. Rathnayake",       "0767890123", "sathyani19103@gmail.com",   "No 78, Galle Road, Matara",                "1978-07-08"),
    ("C007", "862345678V", "S.P. Jayawardena",        "0778901234", "jayawardena@email.com",     "No 12, Temple Road, Gampaha",              "1986-02-19"),
    ("C008", "930123456V", "A.B.C. Fernando",         "0789012345", "fernando@email.com",        "No 90, Malabe Road, Athurugiriya",         "1993-08-25"),
    ("C009", "801234567V", "D.M. Wickramasinghe",     "0790123456", "tharindra0622@gmail.com",        "No 34, Station Road, Kurunegala",          "1980-12-05"),
    ("C010", "951234567V", "N.P. Liyanage",           "0701234567", "liyanage@email.com",        "No 56, Colombo Road, Negombo",             "1995-03-18"),
    

    # ── New 20 customers ─────────────────────────────────────────────────────
    ("C011", "840234567V", "T.G.S. Gunasekara",       "0711234567", "gunasekara@email.com",      "No 22, Kandy Road, Kegalle",               "1984-05-14"),
    ("C012", "920345678V", "W.M.R. Silva",            "0722345678", "silva@email.com",           "No 07, Beach Road, Beruwala",              "1992-09-28"),
    ("C013", "761234890V", "I.M.D. Dissanayake",      "0733456789", "dissanayake@email.com",     "No 18, Hospital Road, Ratnapura",          "1976-01-10"),
    ("C014", "871345678V", "C.H.K. Rajapaksa",        "0744567890", "rajapaksa@email.com",       "No 33, Nupe Road, Moratuwa",               "1987-06-03"),
    ("C015", "960456789V", "L.N.T. Bandara",          "0755678901", "bandara@email.com",         "No 11, Mahinda Mawatha, Anuradhapura",     "1996-11-22"),
    ("C016", "791567890V", "G.P.M. Senanayake",       "0766789012", "senanayake@email.com",      "No 64, Trinco Road, Polonnaruwa",          "1979-03-07"),
    ("C017", "842678901V", "U.S.K. Amarasinghe",      "0777890123", "amarasinghe@email.com",     "No 29, Badulla Road, Bandarawela",         "1984-08-19"),
    ("C018", "913789012V", "V.R.N. Herath",           "0788901234", "herath@email.com",          "No 05, Kurunegala Road, Dambulla",         "1991-12-30"),
    ("C019", "770890123V", "E.M.P. Karunaratne",      "0799012345", "karunaratne@email.com",     "No 47, Nittambuwa Road, Minuwangoda",      "1977-04-16"),
    ("C020", "961901234V", "F.L.S. Madushanka",       "0710123456", "madushanka@email.com",      "No 82, Hambantota Road, Tangalle",         "1996-07-09"),
    ("C021", "830012345V", "Z.A.M. Zubair",           "0721234567", "zubair@email.com",          "No 14, Main Street, Akkaraipattu",         "1983-02-25"),
    ("C022", "905123456V", "Q.N.T. Nawaz",            "0732345678", "nawaz@email.com",           "No 38, Batticaloa Road, Ampara",           "1990-10-11"),
    ("C023", "754234567V", "X.V.R. Mendis",           "0743456789", "mendis@email.com",          "No 60, Horana Road, Panadura",             "1975-06-20"),
    ("C024", "868345678V", "Y.B.K. Wijesuriya",       "0754567890", "wijesuriya@email.com",      "No 03, Negombo Road, Chilaw",              "1986-09-04"),
    ("C025", "947456789V", "O.C.N. Dharmasena",       "0765678901", "dharmasena@email.com",      "No 55, Avissawella Road, Hanwella",        "1994-01-17"),
    ("C026", "783567890V", "J.T.L. Pieris",           "0776789012", "pieris@email.com",          "No 19, Gampola Road, Nawalapitiya",        "1978-05-31"),
    ("C027", "856678901V", "B.H.S. Rodrigo",          "0787890123", "rodrigo@email.com",         "No 44, Kalutara Road, Aluthgama",          "1985-11-08"),
    ("C028", "924789012V", "C.M.P. Cooray",           "0798901234", "cooray@email.com",          "No 71, Havelock Road, Colombo 05",         "1992-03-23"),
    ("C029", "771890123V", "D.K.N. Siriwardena",      "0709012345", "siriwardena@email.com",     "No 26, Station Road, Vavuniya",            "1977-08-14"),
    ("C030", "943901234V", "E.P.M. Tissera",          "0720123456", "tissera@email.com",         "No 09, Weligama Road, Matara",             "1994-12-02"),
]

POLICIES = [
    # ── Original 12 (unchanged) ──────────────────────────────────────────────
    ("P001", "LI42511344", "C001", "LI4", "NGHN1",       "Active", "Monthly",   500000, "2011-06-09"),
    ("P002", "LI421775",   "C002", "LI4", "HNW",         "Active", "Monthly",   300000, "2021-01-10"),
    ("P003", "LI42514876", "C003", "LI4", "Colombo",     "Active", "Quarterly", 750000, "2020-05-15"),
    ("P004", "LI43201234", "C004", "LI5", "Kandy",       "Active", "Monthly",   400000, "2019-08-20"),
    ("P005", "LI43301235", "C005", "LI4", "Matale",      "Active", "Annual",    600000, "2022-03-10"),
    ("P006", "LI43401236", "C006", "LI3", "Matara",      "Active", "Monthly",   250000, "2018-11-25"),
    ("P007", "LI43501237", "C007", "LI5", "Gampaha",     "Active", "Monthly",   550000, "2021-07-14"),
    ("P008", "LI43601238", "C008", "LI4", "Colombo",     "Active", "Quarterly", 450000, "2023-01-08"),
    ("P009", "LI43701239", "C009", "LI3", "Kurunegala",  "Active", "Monthly",   350000, "2017-04-30"),
    ("P010", "LI43801240", "C010", "LI4", "Negombo",     "Active", "Monthly",   500000, "2022-09-18"),
    ("P011", "LI44001241", "C001", "LI3", "NGHN1",       "Active", "Annual",    200000, "2015-03-12"),
    ("P012", "LI44101242", "C003", "LI5", "Colombo",     "Active", "Monthly",   800000, "2018-07-22"),

    # ── New 20 policies (one per new customer) ────────────────────────────────
    ("P013", "LI44201243", "C011", "LI4", "Kegalle",     "Active", "Monthly",   350000, "2019-04-15"),
    ("P014", "LI44301244", "C012", "LI3", "Beruwala",    "Active", "Quarterly", 250000, "2021-06-20"),
    ("P015", "LI44401245", "C013", "LI5", "Ratnapura",   "Active", "Monthly",   600000, "2016-09-10"),
    ("P016", "LI44501246", "C014", "LI4", "Moratuwa",    "Active", "Monthly",   450000, "2020-02-28"),
    ("P017", "LI44601247", "C015", "LI3", "Anuradhapura","Active", "Annual",    300000, "2022-11-05"),
    ("P018", "LI44701248", "C016", "LI4", "Polonnaruwa", "Active", "Monthly",   400000, "2015-07-18"),
    ("P019", "LI44801249", "C017", "LI5", "Badulla",     "Active", "Quarterly", 700000, "2018-03-22"),
    ("P020", "LI44901250", "C018", "LI4", "Dambulla",    "Active", "Monthly",   500000, "2021-10-14"),
    ("P021", "LI45001251", "C019", "LI3", "Minuwangoda", "Active", "Monthly",   200000, "2014-05-30"),
    ("P022", "LI45101252", "C020", "LI4", "Tangalle",    "Active", "Annual",    550000, "2023-04-07"),
    ("P023", "LI45201253", "C021", "LI3", "Ampara",      "Active", "Monthly",   300000, "2019-08-11"),
    ("P024", "LI45301254", "C022", "LI4", "Ampara",      "Active", "Monthly",   400000, "2020-12-25"),
    ("P025", "LI45401255", "C023", "LI5", "Panadura",    "Active", "Quarterly", 650000, "2017-02-14"),
    ("P026", "LI45501256", "C024", "LI4", "Chilaw",      "Active", "Monthly",   450000, "2022-06-03"),
    ("P027", "LI45601257", "C025", "LI3", "Hanwella",    "Active", "Monthly",   250000, "2023-09-19"),
    ("P028", "LI45701258", "C026", "LI4", "Nawalapitiya","Active", "Annual",    350000, "2016-11-28"),
    ("P029", "LI45801259", "C027", "LI5", "Aluthgama",   "Active", "Monthly",   750000, "2020-04-16"),
    ("P030", "LI45901260", "C028", "LI4", "Colombo",     "Active", "Monthly",   500000, "2021-08-09"),
    ("P031", "LI46001261", "C029", "LI3", "Vavuniya",    "Active", "Quarterly", 280000, "2015-01-20"),
    ("P032", "LI46101262", "C030", "LI4", "Matara",      "Active", "Monthly",   420000, "2022-07-31"),
]


def _seed_data(db):
    for c in CUSTOMERS:
        db.execute(
            'INSERT OR IGNORE INTO customers (id,nic,full_name,phone,email,address,date_of_birth) VALUES (?,?,?,?,?,?,?)',
            c
        )
    for p in POLICIES:
        db.execute(
            'INSERT OR IGNORE INTO policies (id,policy_number,customer_id,plan,branch,status,premium_mode,sum_assured,start_date) VALUES (?,?,?,?,?,?,?,?,?)',
            p
        )