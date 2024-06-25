import argparse
from ScrapingHtml2Text import ScrapingHtml2Text
from utility import create_logger


def main():

    myLog = None
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-n',
        default=5,
        help='nuber of pages'
    )
    parser.add_argument(
        '--query',
        default=None,
        help='query to search'
    )
    args = parser.parse_args()
    log_name="scraping"
    myLog=create_logger(log_name=log_name)
    nuber_of_pages=int(args.n)
    query=args.query
    
    scraping = ScrapingHtml2Text(
        logger=myLog
    )

    if not query:
        query=input("Ask me!\n")

    if len(query) == 0:
        print("No")
        return
    
    ris=scraping.web_scraping(
        query=query,
        num_results=nuber_of_pages
    )

    if ris:
        print("Information successfully extracted!")
    else:
        print("Information didn't extract")

if __name__ == "__main__":
    main()
