from tqdm import tqdm
from langchain_community.document_transformers import Html2TextTransformer
from langchain_community.document_loaders import AsyncHtmlLoader
from googlesearch import search
import json
import os


class ScrapingHtml2Text:
    
    logger=None

    def __init__(self, logger=None):
        self.logger=logger

    def web_scraping(self, query, num_results):
        
        self.logger.info("scraping() - IN")

        try:
            # ricerca su Google
            self.logger.info("scraping(): Search info")
            # raddoppio il numero da ricercare e poi prendo solamente i primi n num_results non duplicati
            search_results = search(query, num_results=num_results*2, lang="en")
        except Exception as e:
            print("ERROR while searching on Google: ", e)
            return False

        # salva i link su una lista
        urls=[]
        self.logger.info("scraping(): Urls append")
        # aggiungo gli url delle pagine trovate una volta sola un massimo il numero messo da imput
        for _, result in tqdm(enumerate(search_results, start=1), desc="Urls append"):
            if len(urls)==num_results:
                break
            if not result in urls:
                print("Presa")
                urls.append(result)
        
        print(urls)

        self.logger.info("scraping(): AsyncHtmlLoader")
        with tqdm(total=2, desc="AsyncHtmlLoader") as pbar:
            # caricamento della pagina e viene salvato su docs
            try:
                loader = AsyncHtmlLoader(urls)
            except Exception as e:
                print("ERROR converting HTML to text: ", e)
                return False
            
            pbar.update(1)
            docs = loader.load()
            pbar.update(1)

        self.logger.info("scraping(): Html2TextTransformer")
        with tqdm(total=2, desc="Html2TextTransformer") as pbar:
            # estraggo attraverso html2text le informazioni consultabili della pagina web
            html2text = Html2TextTransformer()
            pbar.update(1)
            docs_trasf=html2text.transform_documents(docs)
            pbar.update(1)

        self.logger.info("scraping(): Ris_scraping")

        # lista di dizionari della struttura: 
        # list_scraping=[{'urls': ... ,'rank': ... ,'text': ... }, {}, ...]
        list_scraping=[]
        for i in tqdm(range(len(docs_trasf)), desc="Add elem to list scraping"):
            element_scraping={}
            element_scraping['url']=urls[i]
            element_scraping['rank']=i+1
            element_scraping['text']=docs_trasf[i].page_content[0:]
            list_scraping.append(element_scraping)
        
        os.makedirs('json',exist_ok=True)

        with open('json/ris_scraping.json', "w") as file:
            json.dump(list_scraping, file, indent=4)
        self.logger.info("scraping() OK")
        
        return True