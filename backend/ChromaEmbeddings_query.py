import argparse
from ChromaEmbeddings import ChromaEmbeddings
import json
from utility import create_logger
from utility import default_model,default_collection,default_metadata,default_k
from utility import save_in_json


def main():
    myLog = None
    
    # inserimento da terminale o quello che gli viene passato dal frontend
    # in alternativa prende dei default
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
    # '{"user":"red", "theme":["music", "fantasy"]}'
    parser.add_argument(
        '-me', 
        type=json.loads,
        default=default_metadata,
        help='name of the metadata for embeddings'
    )
    parser.add_argument(
        '-k', 
        type=json.loads,
        default=default_k,
        help='number of ebeddings it must return'
    )
    args=parser.parse_args()
    name_collection=args.c
    model_name = args.mo.lower()

    try:
        k=int(args.k)
    except:
        print("TypeError: --k must be an integer")
        return False

    myLog=create_logger(log_name=name_collection)
    myLog.debug("Model name: {}\nCollection name: {}".format(model_name, name_collection))

    # richiedo la domanda
    query=""
    while len(query)==0:
        query=input("Ask me!\n")

    embedding = ChromaEmbeddings(
        logger=myLog,
        metadata=args.me, 
        model_name=args.mo, 
        name_collection=args.c
        )
    
    results=embedding.query(query=query,k=k)
    save_in_json('results.json',results['documents'])

    return True


if __name__ == "__main__":
    main()