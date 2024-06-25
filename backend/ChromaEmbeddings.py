import chromadb
from chromadb.utils import embedding_functions
from pypdf import PdfReader
from tqdm import tqdm
from langchain.text_splitter import RecursiveCharacterTextSplitter
import uuid

class ChromaEmbeddings:
    logger=None
    name_collection = ""
    model_name = ""
    metadata = {}

    def __init__(self, logger=None, metadata={}, model_name="BAAI/bge-small-en-v1.5", name_collection="collection"):
        self.logger=logger
        self.name_collection=name_collection
        self.model_name=model_name

        if 'user' not in metadata:
            metadata['user'] = 'admin'
        self.metadata=metadata

        if logger is not None:
            self.logger.info("ChromaEmbeddings:__init__")


    # LEGGE UN PDF E LO RESTITUISCE COME UNA STRINGA
    def new_collection_from_pdf(self, pdf_path): 
        self.logger.info("new_collection_from_pdf() - IN")
        reader = PdfReader(pdf_path)
        pdf_texts = ""

        for p in tqdm(reader.pages, desc="Reader pdf"):
            if p:
                pdf_texts += p.extract_text().strip() 

        self.logger.info("new_collection_from_pdf() - OUT")
        return [pdf_texts]

    # LEGGE UN TXT E LO RESTITUISCE COME UNA STRINGA
    def new_collection_from_text(self, text_path): 
        self.logger.info("new_collection_from_text() - IN")

        with open(text_path,'r') as f:
            lines=f.readlines()

        self.logger.info("new_collection_from_text() - OUT")
        return lines


    def new_collection(self, data_file, delete_collection=False):
       
        self.logger.info("new_collection() - IN")
        client = chromadb.PersistentClient()
        collection=None
        new_metadata={}

        # SALVA IN `new_metadata` I METADATI NELLA STRUTTURA ["m"]="m"
        self.logger.info("new_metadata: start")
        for key in self.metadata.keys():
            if type(self.metadata[key]) == list:
                for t in self.metadata[key]:
                    new_metadata[t]=t
            else:
                new_metadata[key]=self.metadata[key]
        self.logger.info("new_metadata: OK")

        if delete_collection:
            client.delete_collection(self.name_collection)
            self.logger.info("Deleted collection")
            collection = client.create_collection(name=self.name_collection)
            self.logger.info("Created collection")
        else:
            collection = client.get_or_create_collection(name=self.name_collection)
            self.logger.info("Collection found or created")
        
        if type(data_file) == dict:
            print('È un dizionario')
            try:
                file_text=[data_file['text']]
                self.logger.info('Text extraction')
            except Exception as e:
                print("New_Collection - data_file json ", e)
                self.logger.error("New_Collection - data_file json")
                return False
        else:
            print("No, non è un dict")
            print("data_file:",data_file)
            # PER CONTROLLARE ESTENSIONE
            name_split=data_file.split('.')

            if name_split[len(name_split)-1] == "pdf":
                file_text=self.new_collection_from_pdf(pdf_path=data_file)
            elif name_split[len(name_split)-1] == "txt":
                file_text=self.new_collection_from_text(text_path=data_file)
            else:
                self.logger.info("Invalid file")
                return False

        # SPLITTO IL TESTO IN CHUNK DI 512 CARATTERI; SE TROVO UN PUNTO SEGUITO DA N, 
        # LO CONSIDERO COME FINE DI FRASE E QUINDI INTERROMPO IL CHUNK PRIMA DEI 512 CARATTERI
        # 
        # CREO UN OGGETTO DI TIPO `langchain.text_splitter.RecursiveCharacterTextSplitter`, CHE CONTIENE LA LISTA DI CHNUK DI TESTO
        character_splitter = RecursiveCharacterTextSplitter(
            separators=[".\n","."],
            chunk_size=1000,
            chunk_overlap=0
        )

        # CREO UNA LISTA DI STRINGHE A PARTIRE DALL'OGGETTO CHARACTER_SPLITTER
        character_split_texts = character_splitter.split_text('\n\n'.join(file_text))
        
        # CREO GLI EMBEDDING A SECONDA DEL MODELLO
        if self.model_name=="openai":

            import os
            import openai
            from openai import OpenAI
            from dotenv import load_dotenv, find_dotenv

            _ = load_dotenv(find_dotenv()) 
            openai.api_key = os.environ['OPENAI_API_KEY']
            self.logger.info("Embeddings: start")
            with tqdm(total=2, desc="Embeddings")as pbar:
                openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                    model_name="text-embedding-ada-002"
                )
                pbar.update(1)

                # CREO UNA LISTA DI EMBEDDINGS A PARTIRE DALLA LISTA DI STRINGHE
                # UTILIZZANDO LA FUNZIONE DI EMBEDDING OPENAI_EF DEFINITA PRIMA                embeddings = openai_ef(character_split_texts)
                pbar.update(1)
            self.logger.info("Embeddings: Ok")
        else:
            # IMPOSTO IL MODELLO DA UTILIZZARE PER L'EMBEDDING 
            # LA CLASSE SentenceTransformerEmbeddingFunction RICIEDE UN MODELLO DI HuggingFace
            # IL MODELLO BAAI/bge-small-en-v1.5 È UN MODELLO DI SentenceTransformer
            # LA CLASSE SentenceTransformerEmbeddingFunction A DIFFERENZA DI HuggingFaceEmbeddingFunction NON RICHIEDE UNA CHIAVE API
            self.logger.info("Embeddings: start")
            with tqdm(total=2, desc="Embeddings")as pbar:
                sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
                    model_name=self.model_name
                )
                pbar.update(1)
                # CREO UNA LISTA DI EMBEDDINGS A PARTIRE DALLA LISTA DI STRINGHE
                # UTILIZZANDO LA FUNZIONE DI EMBEDDING SENTENCE_TRANSFORMER_EF DEFINITA PRIMA                
                embeddings = sentence_transformer_ef(character_split_texts)
                pbar.update(1)
            self.logger.info("Embeddings: Ok")

        ids = []
        metadatas=[]
        # CREO UNA LISTA DI INDICI UNICI E METADATA, UN NUMERO DI VOLTE QUANTI SONO GLI EMBEDDING
        for i in range(len(character_split_texts)):
            if character_split_texts[i][0:2] == '.\n':
                character_split_texts[i] = character_split_texts[i][2:]

            metadatas.append(new_metadata)
            ids.append(str(uuid.uuid4()))
        
        self.logger.info("Collection add: start")
        # AGGIUNGO LA COLLEZIONE
        with tqdm(total=1, desc="Collection add") as pbar:
            collection.add(
                embeddings=embeddings,
                documents=character_split_texts,
                metadatas=metadatas,
                ids=ids
            )
            pbar.update(1)
        self.logger.info("Collection add: OK")
        self.logger.info("new_collection() - OUT")
        return True


    def query(self, query, k=5):
        
        self.logger.info("query() - IN")
        client = chromadb.PersistentClient()
        chroma_collection = None

        try:
            # RICERCO LA COLLEZIONE E SE NON ESISTE ESCE
            self.logger.info("Get collection - IN")
            with tqdm(total=1, desc="Get collection") as pbar:
                chroma_collection=client.get_collection(name=self.name_collection)
                pbar.update(1)
            self.logger.info("Get collection - OUT")
        except:
            self.logger.error("The collection does not exist")
            print("The collection does not exist")
            return None
        
        if self.model_name.lower()=='openai':
            # FACCIO GLI EMBEDDING DELLA QUERY CON IL MODELLO OPENAI
            import os
            import openai
            from openai import OpenAI
            from dotenv import load_dotenv, find_dotenv

            _=load_dotenv(find_dotenv())
            self.logger.info("Embeddings: start")
            with tqdm(total=3, desc="Embeddings")as pbar:
                openai.api_key = os.environ['OPENAI_API_KEY']
                pbar.update(1)
                openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                                model_name="text-embedding-ada-002"
                            )
                pbar.update(1)
                embeddings = openai_ef([query])
                pbar.update(1)
            self.logger.info("Embeddings: OK")
        else:
            # FACCIO GLI EMBEDDING DELLA QUERY CON UN MODELLO CHE NON SIA DI OPENAI
            self.logger.info("Embeddings: start")
            with tqdm(total=2, desc="Embeddings")as pbar:
                sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=self.model_name)
                pbar.update(1)
                embeddings = sentence_transformer_ef([query])
                pbar.update(1)
            self.logger.info("Embeddings: OK")
            
        where_cond={}
        new_metadata=[]

        self.logger.info("New Metadata")
        for key in self.metadata.keys():
            if type(self.metadata[key]) == list:
                for v in self.metadata[key]:
                    new_metadata.append({v:v})
            else:
                new_metadata.append({key:self.metadata[key]})

        if len(new_metadata)==1:
            where_cond=new_metadata[0]
        else:
            where_cond={"$and":new_metadata}

        self.logger.info("Query: start")
        with tqdm(total=1, desc="Query")as pbar:
            results = chroma_collection.query(
                query_embeddings=embeddings, 
                n_results=k,
                where=where_cond,
                include=['documents']
            )
            pbar.update(1)
            
        self.logger.info("Query: OK")

        self.logger.info("query() - OUT")
        return results
