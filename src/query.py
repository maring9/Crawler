from googlesearch import search

# Function to search a wanted query
def search_query(wanted_query,results_per_page, number_of_results):
  query = wanted_query
  lines = []
  for j in search(query, tld="co.in", num=results_per_page, stop=number_of_results, pause=2): 
    lines.append(j + ",\n")
  return lines