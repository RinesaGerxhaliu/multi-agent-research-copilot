from retrieval.retriever import Retriever

r = Retriever()
results = r.search("payment api security")

print("RESULTS:")
for res in results:
    print(res["document_name"], res["chunk_id"])
