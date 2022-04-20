import os
import random
import re
import sys

import pdb

DAMPING = 0.85
SAMPLES = 10000
ITERATIONS = 10000

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

    if len(pages_linked_to_by_current_page) == 0:  # if there are no outgoing links, we don't want to divide by 0
        prob_of_visiting_link_on_page = 0
    else: 
        prob_of_visiting_link_on_page = float(damping_factor) / len(pages_linked_to_by_current_page)

    prob_of_visting_link_not_on_page = float(1 - damping_factor) / (len(corpus.keys()) - 1)   # -1 bc we don't count the page we are currently on
    
    for k, v in page_probabilities.items():
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

    page_probabilities = corpus.copy()
    for k, v in page_probabilities.items():
        page_probabilities[k] = 0
    if type(page) == list:
        page = page[0]

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
    

    times_each_page_visited_on_random_walk = corpus.copy()
    for k, v in times_each_page_visited_on_random_walk.items():
        times_each_page_visited_on_random_walk[k] = 0
    
    # start w a random page and take n random steps
    random_page_index = int(random.random() * len(corpus.keys()))
    starting_page = (list(corpus.keys()))[random_page_index]
    times_each_page_visited_on_random_walk[starting_page] += 1

    current_page = starting_page
    for i in range(1, n):   # start at 1 (not 0) bc we already took the first step
        trans_model = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(list(trans_model.keys()), weights = list(trans_model.values()), k=1)    #make sure keys() and values() are properly ordered
        times_each_page_visited_on_random_walk[current_page[0]] += 1   # current_page[0] bc current_page is a list

    # to compute pagerank need to divide each value in times_each_page_visited_on_random_walk by n
    pageranks = times_each_page_visited_on_random_walk.copy()
    for k, v in pageranks.items():
        pageranks[k] = float(pageranks[k]) / n
    return pageranks


def find_pages_that_link_to_current_page(currentPage, corpus):
    """
    Returns all pages that contain a link to currentPage
    """
    pages_that_link_to_current_page = []
    for k, v in corpus.items():
        if currentPage in v:
            pages_that_link_to_current_page.append(k)
    return pages_that_link_to_current_page


def compute_second_term(pages_that_link_to_current_page, pageranks, damping_factor, corpus):
    """
    computes the second term in the iterative pagerank formula
    """
    terms_in_sum = []
    for page in pages_that_link_to_current_page:
        term = float(pageranks[page]) / len(corpus[page])     # pagerank of page over the number of links on that page
        terms_in_sum.append(term)
    return damping_factor * sum(terms_in_sum)


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # initialize each pagerank to 1 / N  (N is the num of pages)
    pageranks = corpus.copy()
    for k, v in pageranks.items():
        pageranks[k] = float(1)/len(list(corpus.keys()))     

    # for second condition we must consider each possible page i that links to p
    # we will have to get all pages that link to current page

    iterations = ITERATIONS   # this is how many times we iterate through all pages and update pageranks
    for i in range(iterations):
        for k, v in pageranks.items():
            pages_that_link_to_current_page = find_pages_that_link_to_current_page(k, corpus)
            first_term = (1 - damping_factor) / len(list(corpus.keys()))
            second_term = compute_second_term(pages_that_link_to_current_page, pageranks, damping_factor, corpus)
            pageranks[k] = first_term + second_term

    return pageranks


if __name__ == "__main__":
    main()
