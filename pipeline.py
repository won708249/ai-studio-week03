import pandas as pd
pd.set_option("display.width", 180)
df = pd.read_csv("RAW_DATA.csv", encoding="cp949")

print(" === RAW_DATA csv 파일 내용 === ")
print(df.head())
print(df.info())
print(df.describe())
print(df.shape)
