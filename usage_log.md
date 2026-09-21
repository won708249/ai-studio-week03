# AI 활용 내역

**1. 뭘별과 카테고리별을 곱하는 것은 무슨 의미인가?**  

    여기서 “월별 × 카테고리별”의 ×는 곱하기가 아닙니다.
    “월별이면서 동시에 카테고리별로 나눠서 집계한다”는 뜻입니다.

**2. === RAW_DATA csv 파일 내용 === 주문일자 상품명 카테고리 단가 수량 0 2026-01-01 크루아상 베이커리 4500 1 1 2026-01-01 스콘 디저트 4000 3 2 2026-01-01 크로플 디저트 6,000 2 3 2026-01-01 크루아상 베이커리 4500 3 4 2026-01-01 샌드위치 베이커리 7000 1 <class 'pandas.DataFrame'> RangeIndex: 500 entries, 0 to 499 Data columns (total 5 columns): # Column Non-Null Count Dtype --- ------ -------------- ----- 0 주문일자 500 non-null str 1 상품명 500 non-null str 2 카테고리 500 non-null str 3 단가 500 non-null str 4 수량 500 non-null int64 dtypes: int64(1), str(4) memory usage: 19.7 KB None 이와 같은 csv가 있다. '단가'와 '수량' 열을 곱해 '매출액' 열을 만들고, '주문일자’에서 ‘월’을 추출한 뒤, 월별 × 카테고리별 매출 총합, 평균, 거래건수를 groupby로 집계하는 코드를 작성하라.**
```python
-import pandas as pd

#1. CSV 파일 불러오기
df = pd.read_csv("RAW_DATA.csv")

#2. '단가'의 콤마 제거 후 숫자 타입으로 변환
df["단가"] = pd.to_numeric(
    df["단가"].astype(str).str.replace(",", "", regex=False),
    errors="coerce"
).astype("Int64")

#3. 매출액 = 단가 × 수량
df["매출액"] = df["단가"] * df["수량"]

#4. 주문일자를 날짜 타입으로 변환
df["주문일자"] = pd.to_datetime(df["주문일자"])

#5. 주문일자에서 월 추출
df["월"] = df["주문일자"].dt.month

#6. 월별 × 카테고리별 매출 총합, 평균, 거래건수 집계
result = df.groupby(["월", "카테고리"]).agg(
    매출액_총합=("매출액", "sum"),
    매출액_평균=("매출액", "mean"),
    거래건수=("매출액", "count")
).reset_index()

#결과 확인
print(result)
```

**3. index=False 는 무엇을 의미하는가?**

    index=False는 DataFrame의 인덱스 번호를 Excel이나 CSV에 저장하지 말라는 뜻이에요. 반대로 index=True라면 맨 왼쪽에 0, 1, 2...가 같이 저장됩니다.

**4. 이제 집계 결과를 Monthly_Report.xlsx로 저장한다. 이때, 시트는 ‘월별카테고리요약’, ‘카테고리별합계’로 구성하며 '카테고리별합계' 시트는 카테고리 총매출을 내림차순으로 정리해야 한다. index=False 적용하여 위와 이어질 코드를 작성하라.**

```python
#7. 카테고리별 총매출 집계
category_total = df.groupby("카테고리").agg(
    총매출=("매출액", "sum")
).reset_index()

#총매출 내림차순 정렬
category_total = category_total.sort_values("총매출", ascending=False)

#8. Excel 파일로 저장
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

print("Monthly_Report.xlsx 저장 완료")
```
**5. push하지 않은 커밋은 어떻게 삭제하는가?**

    git reset --soft HEAD~1

    이렇게 하면 최근 커밋은 삭제되다.
    코드 변경 내용은 그대로 남는다.
    변경 내용은 다시 커밋할 수 있다.

**6. vs code에서 xlsx 파일은 어떻게 여냐요?** 

    파일탐색기를 통해 Windows의 Excel 프로그램으로 열어야 합니다.

**7. head()로 결과 표본을 확인하고 원본 매출액 총합과 집계표 총매출 합이 일치하는지 확인하는 검증 코드를 assert를 활용한 코드 한 줄로 작성한다.**

```python
#결과 표본 확인
print(result.head())
print(category_total.head())

#전체 합계 교차 검증
assert df["매출액"].sum() == category_total["총매출"].sum()
#이를 통해 "원본 데이터 전체 매출 = 음료 총매출 + 베이커리 총매출 + 디저트 총매출"이 맞는지 확인한다.

print("Monthly_Report.xlsx 저장 및 검증 완료")
```

**8. 검증결과**   

    head()를 사용하여 집계 결과의 표본을 확인했다.
    원본 매출액 총합과 집계표 총매출 합을 assert로 교차 검증했다.
    실행 시 에러가 발생하지 않아 두 합계가 일치함을 확인했다.
    Monthly_Report.xlsx가 정상적으로 생성됨을 확인했다.