import pandas as pd
pd.set_option("display.width", 180)
df = pd.read_csv("RAW_DATA.csv", encoding="cp949")

print(" === RAW_DATA csv 파일 내용 === ")
print(df.shape)
print(df.info())
print(df.describe())
print(df.head())

df["단가"] = ( pd.to_numeric( df["단가"].astype(str).str.replace(",", "", regex=False), errors="coerce" ) .astype("Int64") )

df["매출액"] = df["단가"] * df["수량"]
df["주문일자"] = pd.to_datetime(df["주문일자"])

df["월"] = df["주문일자"].dt.month

result = df.groupby(["월", "카테고리"]).agg(
    매출액_총합=("매출액", "sum"),
    매출액_평균=("매출액", "mean"),
    거래건수=("매출액", "count")
).reset_index()
print(result)

category_total = df.groupby("카테고리").agg(
    총매출=("매출액", "sum")
).reset_index()
category_total = category_total.sort_values("총매출", ascending=False)


with pd.ExcelWriter("Monthly_Report.xlsx", engine="openpyxl") as writer:
    result.to_excel(
        writer,
        sheet_name="월별카테고리요약",
        index=False
    )

    category_total.to_excel(
        writer,
        sheet_name="카테고리별합계",
        index=False
    )

print(result.head())
print(category_total.head())


assert df["매출액"].sum() == category_total["총매출"].sum()

print("Monthly_Report.xlsx 저장 및 검증 완료")
