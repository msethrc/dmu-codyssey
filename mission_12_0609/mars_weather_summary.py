import csv
import mysql.connector

# [과제 4] DB 연결 설정
DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "mysql",
    "database": "mars_db",
}

CSV_FILE = "mars_weathers_data.csv"


# ──────────────────────────────────────────────
# [보너스] MySQLHelper 클래스
# ──────────────────────────────────────────────
class MySQLHelper:
    def __init__(self, **config):
        self.conn   = mysql.connector.connect(**config)
        self.cursor = self.conn.cursor()
        print("[DB] 연결 성공")

    def execute(self, query, params=None):
        self.cursor.execute(query, params or ())
        self.conn.commit()

    def fetch_all(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()
        print("[DB] 연결 종료")


# [과제 5] CSV 읽기
def read_csv(filepath):
    rows = []
    with open(filepath, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    print(f"[CSV] {len(rows)}개 행 읽음")
    return rows


# [과제 6] INSERT
def insert_data(db, rows):
    query = "INSERT INTO mars_weather (mars_date, temp, storm) VALUES (%s, %s, %s)"
    for i, row in enumerate(rows, 1):
        params = (
            row["mars_date"],
            int(float(row["temp"])),   # float 문자열 → int 변환
            int(row["storm"]),
        )
        db.execute(query, params)
        print(f"  [{i:>4}] INSERT OK → {params}")
    print(f"\n[INSERT] 완료: {len(rows)}개")


# 메인
def main():
    rows = read_csv(CSV_FILE)

    db = MySQLHelper(**DB_CONFIG)
    try:
        insert_data(db, rows)
    finally:
        db.close()


if __name__ == "__main__":
    main()