#Command 1: To Find Total Number of Products
cut -d, -f1 products_cleaned_fixed.csv | tail -n +2 | sort | uniq | wc -l


#Command 2: Most Expensive Product and Price from all the products
awk -F, 'NR>1 {
  	gsub(/₹|,/,"",$5);
  	price = $5+0;
  	prod = $2;
 	if(price > max) {
    	max = price;
    	maxprod = prod;
  	}}
END {print "Most expensive product:", maxprod, "with price: ₹" max}' products_cleaned_fixed.cs


#Command 3: To Find the Average Product Price
awk -F, 'NR>1 {
  gsub(/₹|,/,"",$5);
  a[$2] = a[$2] > $5+0 ? a[$2] : $5+0
}END {
  sum = 0; count = 0;
  for (p in a) { sum += a[p]; count++ }
  printf("Average product price: ₹%.2f\n", sum/count)
}' products_cleaned_fixed.csv


# Command 4: Find Product with Most Reviews
cut -d, -f2 products_cleaned_fixed.csv | tail -n +2 | sort | uniq -c | sort -nr | head -1


#Command 5: To Find Number of Products with Discount > 50%
awk -F, 'NR>1 && $6 ~ /[0-9]+/ {
  match($6, /[0-9]+/);
  disc=substr($6, RSTART, RLENGTH)+0;
  p=$2;
  if(disc > 50) d[p]=1;
}
END {print "Products with discount >50%:", length(d)}' products_cleaned_fixed.csv


#Command 6: Top 10 Most Frequent Words in Review Titles 
cut -d, -f7 products_cleaned_fixed.csv | tail -n +2 | sed 's/"//g' | \ tr '[:upper:]' '[:lower:]' | tr -cs '[:alpha:]' '\n' | grep -v -w -e off -e and -e the -e for -e but | \ grep '.\{3,\}' | sort | uniq -c | sort -nr | head -10


#Command 7: Number of Good Reviews (titles with "good" or "excellent")
cut -d, -f7 products_cleaned_fixed.csv | grep -i -w -E 'good|excellent' | wc -l

#Command 8: Product with Most "Excellent" Reviews
awk -F, 'NR>1 && tolower($7) ~ /excellent/ {c[$2]++} END {for(p in c) print c[p],p}' products_cleaned_fixed.csv | sort -nr |  head -1

#Command 9: Number of “Bad” Review Titles
cut -d, -f7 products_cleaned_fixed.csv | tail -n +2 | grep -i -E 'bad|poor|worst|disappointed' | wc -l

#Command 10: Most Frequent Word in Product Names
cut -d, -f2 products_cleaned_fixed.csv | tail -n +2 | tr '[:upper:]' '[:lower:]' | tr -cs '[:alpha:]' '\n' | \ grep '.\{4,\}' | sort | uniq -c | sort -nr | head -1

