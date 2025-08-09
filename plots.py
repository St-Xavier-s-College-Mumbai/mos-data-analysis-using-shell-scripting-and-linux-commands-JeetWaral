import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re

df = pd.read_csv("products_cleaned_fixed.csv")

# Processing the price and colums
df['NumericPrice'] = df['CurrentPrice'].str.replace('[₹,]', '', regex=True).astype(float)
df['CleanReviews'] = pd.to_numeric(df['Reviews'].replace({',': ''}, regex=True), errors='coerce')
df['DiscountNum'] = df['Discount'].str.extract(r'(\d+)').astype(float)

# 1. Bar: Top 10 Most Expensive Products
expensive = df.groupby('ProductName')['NumericPrice'].max().sort_values(ascending=False).head(10)
plt.figure()
expensive.plot(kind='barh', color='tomato')
plt.title('Top 10 Most Expensive Products')
plt.xlabel('Price (₹)')
plt.ylabel('Product')
plt.tight_layout()
plt.savefig("chart_1_expensive.png")
plt.close()

# 2. Bar: Top 10 Products by Review Count
review_count = df.groupby('ProductName').size().sort_values(ascending=False).head(10)
plt.figure()
review_count.plot(kind='barh', color='cornflowerblue')
plt.title('Top 10 Products by Number of Reviews')
plt.xlabel('Review Count')
plt.ylabel('Product')
plt.tight_layout()
plt.savefig("chart_2_top_reviews.png")
plt.close()

# 3. Histogram: Distribution of Product Prices
prices = df.groupby('ProductName')['NumericPrice'].max()
plt.figure()
prices.plot.hist(bins=10, color='gold')
plt.title('Distribution of Product Prices')
plt.xlabel('Price (₹)')
plt.tight_layout()
plt.savefig("chart_3_price_histogram.png")
plt.close()

# 4. Pie: Share of Products with Discount > 50%
cnt_disc50 = (df.groupby('ProductName')['DiscountNum'].max() > 50).sum()
total_products = df['ProductName'].nunique()
plt.figure()
plt.pie([cnt_disc50, total_products-cnt_disc50], labels=['>50% Discount','≤50%/None'], autopct='%1.1f%%', colors=['#ff6666','#cccccc'])
plt.title('Products with Discount Over 50%')
plt.savefig("chart_4_discount_pie.png")
plt.close()

# 5. Bar: Top 10 Most Frequent Words in Review Titles
all_titles = ' '.join(df['ReviewTitle'].dropna().astype(str)).lower()
words = re.findall(r'\b[a-z]{3,}\b', all_titles)
common_words = Counter(words).most_common(10)
word_df = pd.DataFrame(common_words, columns=['Word', 'Count'])
plt.figure()
sns.barplot(data=word_df, x='Count', y='Word', palette='YlGnBu')
plt.title('Top 10 Words in Review Titles')
plt.tight_layout()
plt.savefig('chart_5_words_title.png')
plt.close()

# 6. Pie: Good/Excellent Review Titles Share
good_rev = df['ReviewTitle'].str.lower().str.contains("good|excellent", na=False).sum()
tot_titles = df['ReviewTitle'].notnull().sum()
plt.figure()
plt.pie([good_rev, tot_titles-good_rev], labels=['Good/Excellent','Others'], autopct='%1.1f%%', colors=['#66b3ff','#c1f0c1'])
plt.title('Good/Excellent Review Titles Proportion')
plt.savefig("chart_6_good_titles_pie.png")
plt.close()

# 7. Bar: Top 5 Products by 'Excellent' Reviews
excellent_counts = df[df['ReviewTitle'].str.lower().str.contains("excellent", na=False)]['ProductName'].value_counts().head(5)
plt.figure()
excellent_counts.plot(kind='barh', color='limegreen')
plt.title("Top 5 Products by 'Excellent' Reviews")
plt.xlabel('Number of “Excellent” Reviews')
plt.ylabel('Product')
plt.tight_layout()
plt.savefig("chart_7_excellent_reviews.png")
plt.close()

# 8. Pie: Share of Bad Review Titles
bad_rev = df['ReviewTitle'].str.lower().str.contains('bad|poor|disappointed|worst', na=False).sum()
plt.figure()
plt.pie([bad_rev, tot_titles-bad_rev], labels=['Bad','Others'], autopct='%1.1f%%', colors=['#ff9999','#e0e0e0'])
plt.title('Negative (“Bad”) Review Titles Proportion')
plt.savefig("chart_8_bad_titles_pie.png")
plt.close()

# 9. Bar: Most Frequent Word in Product Names (Top 5)
all_names = ' '.join(df['ProductName'].astype(str)).lower()
name_words = re.findall(r'\b[a-z]{4,}\b', all_names)
name_word_df = pd.DataFrame(Counter(name_words).most_common(5), columns=['Word', 'Count'])
plt.figure()
sns.barplot(data=name_word_df, x='Count', y='Word', palette='cubehelix')
plt.title('Top 5 Words in Product Names')
plt.tight_layout()
plt.savefig("chart_9_words_product.png")
plt.close()

# 10. Bar: Average Price vs Most Expensive Product
avg_price = prices.mean()
plt.figure()
prices.sort_values(ascending=False).head(10).plot(kind='bar', color='coral')
plt.axhline(avg_price, color='navy', linestyle='--', label=f'Average (₹{avg_price:.2f})')
plt.legend()
plt.title('Top 10 Most Expensive Products vs Average Price')
plt.xlabel('Product')
plt.ylabel('Max Price (₹)')
plt.tight_layout()
plt.savefig('chart_10_expensive_vs_avg.png')
plt.close()

