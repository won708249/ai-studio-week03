import pandas as pd
pd.set_option("display.width", 180)
df = pd.read_csv("RAW_DATA.csv", encoding="cp949")

print(" === RAW_DATA csv 파일 내용 === ")
print(df.head())
print(df.info())
print(df.describe())
print(df.shape)

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

