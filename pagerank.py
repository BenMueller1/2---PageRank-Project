import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages

def populate_probabilities(page, page_probabilities, damping_factor, pages_linked_to_by_current_page, corpus):

    prob_of_visiting_link_on_page = float(damping_factor) / len(pages_linked_to_by_current_page)
    prob_of_visting_link_not_on_page = float(1 - damping_factor) / (len(corpus.keys()) - 1)   # -1 bc we don't count the page we are currently on
    
    for k, v in page_probabilities:
        if k in pages_linked_to_by_current_page:
            page_probabilities[k] = prob_of_visiting_link_on_page + prob_of_visting_link_not_on_page
        else:
            page_probabilities[k] = prob_of_visting_link_not_on_page
    
    del page_probabilities[page] # we don't want to travel back to current page

    return page_probabilities


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    page_probabilities = corpus
    for k, v in page_probabilities:
        page_probabilities[k] = 0
    pages_linked_to_by_current_page = corpus[page]

    page_probabilities = populate_probabilities(page, page_probabilities, damping_factor, pages_linked_to_by_current_page, corpus)
    return page_probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # start w a random page and take n steps

    times_each_page_visited_on_random_walk = corpus
    for k, v in times_each_page_visited_on_random_walk:
        times_each_page_visited_on_random_walk = 0
    
    # take n random steps



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
