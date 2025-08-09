#!/bin/bash
echo "Filename,ProductName,Ratings,Reviews,CurrentPrice,Discount,ReviewTitle,ReviewComment" > products_cleaned_fixed.csv
for file in raw_*.html; do
  # Extract main product info fields once (escape quotes)
  product_name=$(grep -oP '(?<=<h1 class="_6EBuvT"><span class="VU-ZEz">)[^<]+' "$file" | head -1 | sed 's/"/""/g')
  ratings=$(grep -oP '[0-9,]+ Ratings' "$file" | head -1 | sed 's/ Ratings//; s/"/""/g')
  reviews=$(grep -oP '[0-9,]+ Reviews' "$file" | head -1 | sed 's/ Reviews//; s/"/""/g')

  # Extract the entire price string carefully and clean it
  current_price=$(grep -oP '<div class="Nx9bqj[^"]*">₹[0-9,]+' "$file" | head -1 | grep -oP '₹[0-9,]+')
  current_price=${current_price:-""}  # fallback to empty if not found
  current_price=$(echo "$current_price" | sed 's/"/""/g')

  discount=$(grep -oP '<div class="UkUFwK WW8yVX"><span>[^<]+' "$file" | sed 's/<[^>]*>//g' | head -1)
  discount=${discount:-""}
  discount=$(echo "$discount" | sed 's/"/""/g')

  # Extract all review titles and comments - arrays to keep order
  mapfile -t review_titles < <(grep -oP '<p class="z9E0IG">[^<]+' "$file" | sed 's/<[^>]*>//g' | sed 's/"/""/g')
  mapfile -t review_comments < <(grep -oP '<div class="">[^<]+' "$file" | sed 's/<[^>]*>//g' | sed 's/"/""/g')

  # Determine max reviews between titles and comments
  max_reviews=${#review_titles[@]}
  if [ ${#review_comments[@]} -gt $max_reviews ]; then
    max_reviews=${#review_comments[@]}
  fi

  # If no reviews found, output one row with empty review fields
  if [ "$max_reviews" -eq 0 ]; then
    echo "\"$file\",\"$product_name\",\"$ratings\",\"$reviews\",\"$current_price\",\"$discount\",\"\",\"\"" >> products_cleaned_fixed.csv
  else
    # Output one CSV row per review pairing
    for ((i=0; i<max_reviews; i++)); do
      title=${review_titles[i]:-""}
      comment=${review_comments[i]:-""}
      echo "\"$file\",\"$product_name\",\"$ratings\",\"$reviews\",\"$current_price\",\"$discount\",\"$title\",\"$comment\"" >> products_cleaned_fixed.csv
    done
  fi
done
