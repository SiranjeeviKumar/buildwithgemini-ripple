# scripts/create_rag_corpus.py
"""Creates a serverless Vertex AI RAG corpus and imports pg49513.txt."""

import time
import vertexai
from vertexai.preview import rag
from vertexai.preview.rag.utils import resources as rr

PROJECT_ID = "qwiklabs-gcp-03-3773bdab8c6e"
LOCATION = "us-central1"  # Serverless RAG is us-central1 only
GCS_PATH = "gs://ripple-public-assets-qwiklabs-gcp-03-3773bdab8c6e/rag/pg49513.txt"


def main():
    print(f"Initializing Vertex AI RAG Engine (project: {PROJECT_ID}, location: {LOCATION})...")
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    # 1. Switch region's RAG managed DB to serverless mode
    cfg_name = f"projects/{PROJECT_ID}/locations/{LOCATION}/ragEngineConfig"
    print("Setting RAG Engine to Serverless mode...")
    try:
        rag.update_rag_engine_config(
            rag_engine_config=rag.RagEngineConfig(
                name=cfg_name,
                rag_managed_db_config=rag.RagManagedDbConfig(mode=rr.Serverless()),
            )
        )
        print("RAG Engine successfully configured for Serverless mode.")
    except Exception as e:
        print(f"Serverless mode update notice/warning: {e}")

    # 2. Create the RAG Corpus
    print("Creating RAG Corpus 'ripple-gutenberg-corpus'...")
    corpus = rag.create_corpus(
        display_name="ripple-gutenberg-corpus",
        embedding_model_config=rag.EmbeddingModelConfig(
            publisher_model="publishers/google/models/text-embedding-005"
        ),
    )
    print(f"✅ RAG Corpus Created: {corpus.name}")

    # 3. Import and index the GCS file
    print(f"Importing and indexing {GCS_PATH} into corpus...")
    response = rag.import_files(
        corpus_name=corpus.name,
        paths=[GCS_PATH],
        transformation_config=rag.TransformationConfig(
            chunking_config=rag.ChunkingConfig(chunk_size=512, chunk_overlap=100)
        ),
    )
    print(f"✅ Import Complete! Imported files count: {response.imported_rag_files_count}")
    print(f"Corpus Resource Name: {corpus.name}")

    # Write Corpus Resource Name to a local file for tool reference
    with open("rag_corpus_name.txt", "w") as f:
        f.write(corpus.name.strip())


if __name__ == "__main__":
    main()
