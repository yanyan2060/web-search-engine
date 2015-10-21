def get_page(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ""

#page = "" #website
# webcrawler
def get_next_page(s):
    start_link = s.find ('<a href=')
    start_quote = s.find ('"', start_link)
    end_quote = s.find('"', start_quote + 1)
    url = s[start_quote + 1:end_quote]
    return url,end_quote

def get_all_links (page):
    links = []
    while True:
        url, endpos = get_next_page(page)
        if url:
            print url
            page = page[endpos:]
        else:
            break
    return links

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)

def crawl_web (seed):
    tocrawl = [seed]
    crawled = []
  #  index = {}
  #  index = {}
    # page rank, construct a directed graph
    graph = {}
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            union(tocrawl,outlinks)
            crawled.append(page)
    return crawled

#Build Index
index = {}
def add_to_index(index, keyword, url): #using hashtable as index to improve
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = url
    '''for entry in index:
        if entry[0] == keyword:
            entry[1].append(url)
            return
    index.append([keyword,[url]])'''

def lookup (index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None
    ''''for entry in index:
        if entry[0] == keyword:
            return entry[1]
    return []'''
def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)

def compute_ranks(graph):
    d = 0.8 #damping factor
    numloops = 10

    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    for i in range (0, npages):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            # update by suming in the inlink ranks, find all nodes has the link to this page
            for node in graph:
                if page in graph[node]:
                    newrank += ranks[node] * d / len(graph[node])
            newranks[page] = newrank
        ranks = newranks
    return ranks

add_page_to_index (index, 'http://dilbert.com',
"""
Another strategy is to ignore the fact that you
are slowly killing yourself by not sleeping and
exercising enough. That frees up several hours a
day. The only downside is that you get fat and die.--- Scott Adams on Time Management """)
print index



