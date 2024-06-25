import argparse
from ChromaEmbeddings import ChromaEmbeddings
import json
from utility import default_model,default_collection,default_metadata,default_path_documents
from utility import create_logger


def main():
    myLog = None
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        '-mo',
        default=default_model,
        help='name of the model for embeddings'
    )
    parser.add_argument(
        '-c', 
        default=default_collection,
        help='name of the collection for embeddings'
    )
    # {"user":nome_utente,
    #   "theme": [temaA, temaB, ...] } theme è facoltativo
    parser.add_argument(
        '-me', 
        type=json.loads,
        default=default_metadata,
        help='name of the metadata for embeddings'
    )
    parser.add_argument(
        '-d', 
        default=default_path_documents,
        help='name of the document for embeddings'
    )
    parser.add_argument(
        '--delete',
        default=False,
        help='delete the collection if it already exists'
    )
    args = parser.parse_args()
    name_collection=args.c
    myLog=create_logger(log_name=name_collection)
    model_name = args.mo.lower()
    myLog.debug("Model name: {}\nCollection name: {}".format(model_name, name_collection)) 
    
    embedding = ChromaEmbeddings(
        logger=myLog,
        name_collection=name_collection,
        model_name=model_name,
        metadata=args.me
    )
    ris=embedding.new_collection(delete_collection=args.delete,data_file=args.d)

    if ris:
        print("Collection created successfully!")
    else:
        print("Collezione non creata")

if __name__ == "__main__":
    main()
