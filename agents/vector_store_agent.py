import chromadb
from chromadb.utils import embedding_functions
from agents.application_pattern_learning_agent import load_fm_bundle_map

client = chromadb.Client()

collection = client.get_or_create_collection("bundle_knowledge")

def load_bundles_into_vector_db():

    bundle_map = load_fm_bundle_map()

    for bundle_name, apps in bundle_map.items():

        text = f"Bundle {bundle_name} includes applications: {', '.join(apps[:30])}"

        collection.add(
            documents=[text],
            ids=[bundle_name]
        )

    print("Bundle knowledge stored in ChromaDB")

def retrieve_bundle_options():

    results = collection.get()

    return results
