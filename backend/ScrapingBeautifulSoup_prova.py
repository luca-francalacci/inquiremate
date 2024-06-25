from ScrapingBeautifulSoup import ScrapingBeautifulSoup
from utility import save_in_json
from utility import create_logger
import argparse
from tqdm import tqdm


def main():

    name_collection="ScrapingBeautifulSoup"
    myLog=create_logger(log_name=name_collection)
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-d',
        default=1,
        help='website depth'
    )

    parser.add_argument(
        '--http',
        default="https://it.wikipedia.org/wiki/Fuffi",
        help='initial website'
    )

    parser.add_argument(
        '--summary',
        default='false',
        help='generate summary with api calls to ChatGPT (default: False)'
    )

    parser.add_argument(
        '-lc',
        default='false',
        help='LangChain mode (default: True)'
    )

    args=parser.parse_args()
    depth=int(args.d)
    initial_url=args.http

    if parser.parse_args().summary.lower() == 'false':
        print("dentro false")
        summary=False
    elif parser.parse_args().summary.lower() == 'true':
        print("dentro true")
        summary=True
    else:
        print("--summary error")
        return
    
    if parser.parse_args().lc.lower() == 'false':
        lang_chain=False
    elif parser.parse_args().lc.lower() == 'true':
        lang_chain=True
    else:
        print("--lc error")
        return

    myLog.debug("Collection name: {}".format(name_collection)) 

    s = ScrapingBeautifulSoup(logger=myLog)
    scraping_ok = s.scraping(initial_url=initial_url,depth=depth,lang_chain=lang_chain)
    
    if not scraping_ok:
        print("Error")
        return
    elif summary == True:
        s.generate_summary()
        save_in_json('scraping_ris_gpt.json', s.summary_pages_list, True)  
    save_in_json('scraping_ris.json', s.scraping_result_list, True)

if __name__ == "__main__":
    main()