from bs4 import BeautifulSoup

html = """
<a href="https://example.com/outer-link" class="first">
    Outer Link
    <a href="https://example.com/inner-link-1">Inner Link 1</a>
    <a href="https://example.com/inner-link-2">Inner Link 2</a>
</a>
"""

soup = BeautifulSoup(html, 'html.parser')

# Find all <a> tags with the class "first"
all_as = soup.find_all('a', class_='first')

for a in all_as:
    print(a['href'])
