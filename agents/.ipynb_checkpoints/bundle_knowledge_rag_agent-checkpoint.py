import chromadb
from agents.bundle_tier_agent import build_bundle_options

client = chromadb.Client()
collection = client.get_or_create_collection("bundle_knowledge")


def seed_bundle_knowledge(user_profile=None):

    bundle_options = build_bundle_options(user_profile or {})

    existing = set(collection.get().get("ids", []))

    for bundle_name, apps in bundle_options.items():

        doc = f"""
Bundle: {bundle_name}

Core Applications:
{", ".join(apps[:12])}

Security Stack:
Cisco Secure Client, CyberArk, Netskope

Collaboration:
Microsoft 365, Microsoft Teams

Provisioning Category:
Enterprise Workplace Bundle
"""

        if bundle_name in existing:

            collection.update(
                ids=[bundle_name],
                documents=[doc],
                metadatas=[{"bundle_name": bundle_name}]
            )

        else:

            collection.add(
                ids=[bundle_name],
                documents=[doc],
                metadatas=[{"bundle_name": bundle_name}]
            )

    return bundle_options


def retrieve_bundle_knowledge(bundle_name, top_k=1):

    results = collection.query(
        query_texts=[bundle_name],
        n_results=top_k
    )

    docs = results.get("documents", [[]])[0]

    return {
        "documents": docs
    }