from bs4 import BeautifulSoup

def clean_html(content, max_words=None, retain_h2=False):
    soup = BeautifulSoup(content, 'html.parser')
    
    # Remove all links
    for a in soup.find_all('a'):
        a.unwrap()

    # Convert headings to paragraphs
    for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        if retain_h2 and tag == soup.find('h2'):
            continue  # Retain the first <h2> as a heading
        tag.name = 'p'

    # Ensure table text is left-aligned
    for table in soup.find_all('table'):
        for cell in table.find_all(['td', 'th']):
            cell['style'] = 'text-align: left;'  # Ensure left alignment
    
    # Remove excessive paragraph spacings (consecutive <p> tags or excessive <br> tags)
    for p in soup.find_all('p'):
        if p.get_text(strip=True) == '':
            p.decompose()  # Remove empty <p> tags
        else:
            p.unwrap()  # Remove paragraph tags to eliminate unnecessary spacings
    
    # Limit to max_words if specified
    if max_words is not None:
        text_content = ' '.join(soup.get_text().split()[:max_words])
        return text_content  # Return the plain text instead of processing it with BeautifulSoup again

    return soup.prettify()
