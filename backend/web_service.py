from fastapi import FastAPI
from pydantic import BaseModel
from utility import create_logger
from ScrapingHtml2Text import ScrapingHtml2Text
from ScrapingBeautifulSoup import ScrapingBeautifulSoup
from ChromaEmbeddings import ChromaEmbeddings
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from utility import save_in_json

app = FastAPI()
logger=create_logger(log_name="log_web_scraping")
name_collection = "web_app_collection"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DataScraping(BaseModel):

    n:int | None=5
    query:str | None=None


class DataScrapingBS(BaseModel):

    http:str | None=None
    d:int | None=0
    summary:bool | None=False
    lc:bool | None=False
    query:str | None=""
    n:int| None=5


class DataEmbedding(BaseModel):

    model:str | None="BAAI/bge-small-en-v1.5"
    collection:str | None="collection"
    metadata:dict | None={'user':'admin'}
    path:str | None=None
    delete:bool | None=False


class DataScrapingEmbedding(BaseModel):

    http:str | None=None
    d:int | None=0
    summary:bool | None=False
    lc:bool | None=False


def web_scraping_real(data):

    scraping = ScrapingBeautifulSoup(
        logger=logger
    )

    if data.http == None:
        return "Html not inserted"
    
    ris_scraping=scraping.scraping(
        initial_url=data.http,
        depth=data.d,
        lang_chain=data.lc
    )

    return ris_scraping


@app.post("/scraping_bs")
def web_scraping_bs(data:DataScrapingBS):
    print(data.http)

    scraping = ScrapingBeautifulSoup(
        logger=logger
    )

    if data.http == None:
        return "Html not inserted"
    
    ris_scraping=scraping.scraping(
        initial_url=data.http,
        depth=data.d,
        lang_chain=data.lc
    )

    if ris_scraping:
        print('Dentro ris_scraping')
        

        name_file = 'file.json'
        
        if data.summary:
            print("Dentro data.summary")
            ris_generate_summary=scraping.generate_summary()
            if ris_generate_summary:
                print("Dentro -if")

                save_in_json(name_file, scraping.summary_pages_list, True)
                return FileResponse('json/'+name_file)
            else:
                print('scraping: ok | summary no ok')
        print('scraping.scraping_result_list:',scraping.scraping_result_list)
        save_in_json(name_file, scraping.scraping_result_list, True)
        return FileResponse('json/'+name_file)
    else:
        print('Dentro else')
        msg_ris="Information didn't extract"
    
    return msg_ris


# url per lo scraping
@app.post("/scraping")
def web_scraping(data:DataScraping):
    
    # inizializzo oggetto scraping
    scraping = ScrapingHtml2Text(
        logger=logger
    )
    
    if data.query == None:
        return "Query not inserted"
    
    # esegue lo scraping dell'oggetto
    ris_scraping=scraping.web_scraping(
        query=data.query,
        num_results=data.n
    )

    if ris_scraping:
        msg_ris="Information successfully extracted!"
    else:
        msg_ris="Information didn't extract"

    return FileResponse('json/ris_scraping.json')


@app.post("/embedding")
def chroma_embedding(data:DataEmbedding):

    if data.path == None:
        print('Error: path')
        return False

    embedding = ChromaEmbeddings(
        logger=logger,
        name_collection=data.collection,
        model_name=data.model,
        metadata=data.metadata
    )
    ris_new_collection = embedding.new_collection(delete_collection=data.delete,data_file=data.path)

    if ris_new_collection:
        print('Collection created successfully!')
        return True
    else:
        print("Collezione non creata")
        return False


@app.post("/inquireMate/web_search")
def inquireMate(data:DataScrapingBS):
    s = ScrapingBeautifulSoup(logger=logger)

    if data.query is None:
        return None
    ris = s.web_search(data.query, data.n)
    return ris


@app.post("/inquireMate/scraping_embedding")
def scraping_embedding(data:DataScrapingEmbedding):
    s = ScrapingBeautifulSoup(logger=logger)
    
    if s.query is None:
        s.query = ""
    print(s.query)

    if data.http == None:
        return "Html not inserted"
    
    print("LISTA:",s.url_list)

    ris_scraping=s.scraping(
        initial_url=data.http,
        depth=data.d,
        lang_chain=data.lc
    )

    if not ris_scraping:
        return False

    name_file = "scraping_embedding.json"
    
    save_in_json(name_file, s.scraping_result_list, True)

    for scraping in s.scraping_result_list:
        metadata = {}
        metadata['url'] = scraping['url']
        metadata['rank'] = scraping['rank']
        metadata['query'] = s.query

        c = ChromaEmbeddings(
            logger=logger,
            metadata=metadata,
            name_collection=name_collection
        )
        c.new_collection(
            data_file={'text': scraping['text']}
        )
    
    if data.summary:
        s.generate_summary()
        save_in_json('scraping_ris_gpt.json', s.summary_pages_list, True)
        return s.summary_pages_list

    res = s.scraping_result_list
    return res


class DataQuery(BaseModel):
    query:str | None=None 


@app.post("/query")
def query(data:DataQuery):
    if data.query is None:
        return False
    e = ChromaEmbeddings(
        logger=logger,
        name_collection=name_collection
    )
    ris = e.query(query=data.query)
    print(ris['documents'])
    return ris['documents'] 
