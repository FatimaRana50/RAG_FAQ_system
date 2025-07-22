#########part2#####################
faq_documents = [
    "What is Git? Git is a distributed version control system for tracking changes in source code during software development.",
    "How do I create a Python virtual environment? You can create a virtual environment using `python -m venv myenv` or `conda create -n myenv python=3.9`.",
    "What is a FastAPI endpoint? A FastAPI endpoint is a function decorated with an HTTP method (like `@app.get` or `@app.post`) that handles incoming web requests.",
    "Explain Python's `list` data structure. A list in Python is an ordered, mutable collection of items. It allows duplicate members and can contain items of different data types."
]
##########part 3####################
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

import chromadb
client = chromadb.EphemeralClient()
#loading model
model = SentenceTransformer('all-MiniLM-L6-v2')
# Initialize the ChromaDB client

# Create a collection for the FAQ documents
collection = client.create_collection(name="faq_collection")
## . Embed and add documents
for i, doc in enumerate(faq_documents):
    embedding = model.encode(doc).tolist()
    collection.add(documents=[doc], embeddings=[embedding], ids=[f"doc_{i}"])
print("FAQ documents have been embedded and added to the ChromaDB collection.")

###############part4 ##################

#defining query
query_text = "How do I make a virtual environment?"
# Embed the query
query_embedding = model.encode(query_text).tolist()

# Query the collection
results = collection.query(query_embeddings=[query_embedding], n_results=1)

# Display the results
print("Query Results:")
print(f"\n Query: {query_text}")
print(f" Retrieved Document: {results['documents'][0][0]}")
print(f"Distance: {results['distances'][0][0]}")

############part 5######################

# Define new query
query_text = "Explain python's list data structure?"

# Embed the new query
query_embedding = model.encode(query_text).tolist()

# Perform the new query
results = collection.query(query_embeddings=[query_embedding], n_results=3)

# Use the new result
retrieved_docs = results['documents'][0]
combined_context = "\n---\n".join(retrieved_docs)


# Generate conceptual LLM prompt
llm_prompt = f"Based on the following context, please answer the question.\n\nContext:\n{combined_context}\n\nQuestion: {query_text}"
# Display

print("\n Conceptual LLM Prompt:")
print(f"Question: {query_text}")
for i, doc in enumerate(retrieved_docs, 1):
    print(f"Answer Context {i}: {doc}")







