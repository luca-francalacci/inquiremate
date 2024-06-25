from lxml import etree
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.parse import urlunparse
from tqdm import tqdm
from googlesearch import search


class ScrapingBeautifulSoup:

    logger=None
    url_list:list
    scraping_result_list:list
    summary_pages_list:list
    query: str|None=None


    def __init__(self,logger=None):

        self.url_list = []
        self.scraping_result_list = []
        self.summary_pages_list = []
        self.logger=logger

        if logger is not None:
            self.logger.info("ScrapingBeautifulSoup: __init__")


    # TRAMITE L'API DI GOOGLE, RESTITUISCE UN NUMERO DI URL, IN BASE ALLA QUERY IN INGRESSO
    def web_search(self, query, num_results):

        self.query = query
        
        self.logger.info("scraping() - IN")

        try:
            # RICERCA SU GOOGLE
            # RADDOPPIO IL NUMERO DA RICERCARE E POI PRENDO SOLAMENTE I PRIMI N NUM_RESULTS NON DUPLICATI
            search_results = search(query, num_results=num_results*2, lang="en")
        except Exception as e:
            print("ERROR while searching on Google: ", e)
            return None

        # SALVA I LINK SU UNA LISTA
        urls=[]
        # AGGIUNGO GLI URL DELLE PAGINE TROVATE UNA VOLTA SOLA UN MASSIMO IL NUMERO MESSO DA INPUT
        for _, result in tqdm(enumerate(search_results, start=1), desc="Urls append"):

            if len(urls)==num_results:
                break

            url_temp = urlparse(result)
            domain = url_temp.netloc
            t = False
            
            for u in urls:
                if domain == u.netloc:
                    t = True
                    break

            if not t:
                urls.append(url_temp)
        
        ris = [urlunparse(u) for u in urls]
        print(ris)
        return ris


    # FUNZIONE CHE INIZIALIZZA LO SCRAPING
    def scraping(self, initial_url=None, depth=0, lang_chain=False):

        if depth<0:
            return False

        return self.__real_scraping(initial_url=initial_url, max_depth=depth,depth=0, lang_chain=lang_chain)

  
    # FUNZIONE CHE EFFETTUA REALMENTE LO SCRAPING:
    # PARTENDO DA UN URL, INIZIA A SCENDERE DI PROFONDITÀ
    # È POSSIBILE UTILIZZARE L'API DI LANGCHAIN, OPPURE UTILIZZARE DIRETTAMENTE BEAUTIFULSOUP
    # LANGCHAIN È PIÙ LENTO, DATO CHE GENERA UN MOTORE DI RICERCA
    def __real_scraping(self, initial_url, max_depth, depth, lang_chain):

        print("-----------------------------")
        print("+++ DENTRO SCRAPING()")
        print("+++ URL INIZIALE: ", initial_url)
        print("+++ ", depth)
        print("+++ ", max_depth)        

        self.logger.info("ScrapingBeautifulSoup: scraping - IN")

        if initial_url == None:
            self.logger.info("ScrapingBeautifulSoup: scraping - initial_url == None or depth == 0")
            return False

        add_item=True

        # CONTROLLO SE LA PAGINA È GIÀ STATA VISITATA
        # NEL CASO LO FOSSE CONTROLLO CON QUALE RANK
        #   SE L'ATTUALE PROFONDITÀ È INFERIORE RISPETTO ALLA PROFONDITÀ CON CUI È STATA SCREPATA 
        #       =>  NON SCRAPIAMO LA PAGINA, MA TROVIAMO I LINK DI QUESTA PAGINA (add_item=False)
        #   ALTRIMENTI NON ESEGUO NIENTE (return True)
        for u in self.scraping_result_list:
            print(u['url'])
            if u['url']==initial_url:
                if u['rank']<depth:
                    print('True')
                    return True
                else:
                    add_item=False
                    print('False')
                    break
        
        # SCOMPOSIZIONE URL
        initial_url_parsed = urlparse(initial_url)
        initial_url_domain = initial_url_parsed.netloc

        if not lang_chain:
            from bs4 import BeautifulSoup
            import requests
            
            # RICHIESTA HTTP PER IL CONTENUTO DELLA PAGINA
            self.logger.info("ScrapingBeautifulSoup: scraping - richiesta http")
            results = requests.get(initial_url)
            doc = BeautifulSoup(results.text, "html.parser")
            # urls: LISTA DI URL RIPETUTI UNA VOLTA SOLA
            urls = self.__url_extraction(initial_url,initial_url_domain, results.text)
            
            # SE LA PAGINA VA SCREPATA => RIMUOVI HEADER E FOOTER
            if add_item:
                self.logger.info("ScrapingBeautifulSoup: scraping - rimozione header")
                nav_tag = doc.find('header')
                if nav_tag:
                    nav_tag.extract()
            self.logger.info("ScrapingBeautifulSoup: scraping - rimozione footer")
            footer_tag = doc.find('footer')
            if footer_tag:
                footer_tag.extract()

            # ESTRAZIONE DELLA PAGINA
            self.logger.info("ScrapingBeautifulSoup: scraping - trasformazione pag web in testo")
            page_text = doc.find('body').get_text()
            page_text = '\n'.join([line for line in page_text.splitlines() if line.strip()])
        else:
            from langchain_community.document_loaders import AsyncChromiumLoader
            from langchain_community.document_transformers import BeautifulSoupTransformer
            
            # CARICAMENTO DELLA PAGINA
            self.logger.info("ScrapingBeautifulSoup-LangChain: scraping - richiesta http")
            loader = AsyncChromiumLoader([initial_url])
            html = loader.load()
            pattern = r'<!--(.*?)-->'
            import re
            page_content = re.sub(pattern,'',html[0].page_content)
            # urls: LISTA DI URL RIPETUTI UNA VOLTA SOLA
            html[0].page_content=page_content
            urls = self.__url_extraction(initial_url,initial_url_domain, page_content)
            bs_transformer = BeautifulSoupTransformer()
            # ESTRAPOLAZIONE PAGINA WEB
            docs_transformed = bs_transformer.transform_documents(html,unwanted_tags= ["script", "style","nav", "footer","header"],)
            page_text = docs_transformed[0].page_content
            pattern = r'\(https?:\/\/\S+\b\)|\(/\S+\)|\(#\S+\)'
            page_text=re.sub(pattern, '', page_text)
            
        # SE LA PAGINA ANDAVA SCREPATA => AGGIUNGI ALLA LISTA DELLE PAGINE
        if add_item:
            element = {
                'url': initial_url,
                'rank': depth,  
                'text': page_text
            }
            self.scraping_result_list.append(element)
            self.url_list.append(initial_url)
        
        if depth>=max_depth:
            print("depth>=max_depth")
            return True

        # SCORRO LA LISTA DEGLI URL E CONTROLLO SE È DIVERSA DALL'URL DI PARTENZA
        # E NEL CASO ESEGUO LO SCRAPING
        for url in urls:
            url_parsed = urlparse(url)
            if url_parsed != initial_url_parsed:
                self.__real_scraping(initial_url=url, max_depth=max_depth, depth=(depth + 1), lang_chain=lang_chain)
                    
        self.logger.info("ScrapingBeautifulSoup: scraping - OUT")

        return True


    # METODO CHE CHIAMA L'API DI OPENAI, EFFETTUA UN RIASSUNTO, E LO RESTITUISCE
    def generate_summary_gpt(self, input_text, model="gpt-3.5-turbo"):

        import os
        import openai
        from openai import OpenAI
        from dotenv import load_dotenv, find_dotenv
        _ = load_dotenv(find_dotenv()) 

        openai.api_key = os.environ['OPENAI_API_KEY']
        openai_client = OpenAI()

        messages = [
            {
                "role": "user",
                "content": f"Riassumi il seguente testo:{input_text}"
            }
        ]

        response = openai_client.chat.completions.create(
            model=model,
            messages=messages,
        )

        return response.choices[0].message.content


    # METODO CHE RICHIMA IL METODO `generate_summary_gpt` PER OGNI PAGINA CHE È STATA SCRAPATA
    # E SALVA IL CONTENUTO NELLA LISTA `summary_pages_list`
    def generate_summary(self):

        from tqdm import tqdm

        for el in tqdm(self.scraping_result_list, desc="Processing"):
            try:
                page={
                    'url': el['url'],
                    'rank': el['rank'],
                    'text': self.generate_summary_gpt(input_text=el['text']),
                }
            except:
                return False
            
            self.summary_pages_list.append(page)
            
        return True

    
    # METODO PRIVATO FINALIZZATO ALL'ESTRAPOLAZIONE DEGLI URL
    # ESCLUDE UN URL SE ABBIAMO GIÀ INCONTRATO UN URL CON LO STESSO DOMINIO 
    def __url_extraction(self, initial_url, initial_url_domain, html_string):

        html_tree = etree.HTML(html_string)
        # TROVA ELEMENTI 'a' E NE FORMA UNA LISTA
        link_elements = html_tree.findall('.//a')
        urls=[]

        # FORMA UNA LISTA (urls) SENZA URL RIPETUTI
        for link in link_elements:
            link_with_domain = urljoin(initial_url, link.get('href'))
            if ( 
                    (link_with_domain not in urls) and 
                    (initial_url != link_with_domain) and 
                    (urlparse(link_with_domain).netloc == initial_url_domain)
                ):
                urls.append(link_with_domain)

        return urls 

