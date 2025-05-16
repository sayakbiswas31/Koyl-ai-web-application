from flask import Flask, render_template, request, jsonify
from services.data_fetcher import fetch_pubmed_data
from services.model_trainer import train_model, load_trained_model
from services.rag_pipeline import preprocess_and_embed, store_in_faiss, load_faiss_vector_store, setup_rag_pipeline, query_rag

app = Flask(__name__)

def initialize_system():
    # Fetch data
    queries = ["disease symptoms", "allergy symptoms"]
    all_documents = []
    for query in queries:
        documents = fetch_pubmed_data(query, max_results=5)
        all_documents.extend(documents)
    
    print(f"Fetched {len(all_documents)} documents: {all_documents}")
    if not all_documents:
        print("No documents fetched.")
        return None, (None, None)
    
    # Train model
    model, tokenizer = train_model(all_documents)
    if model is None:
        print("Model training failed. Proceeding without trained model.")
    
    # Setup RAG pipeline
    texts, embeddings = preprocess_and_embed(all_documents)
    vector_store = store_in_faiss(texts, embeddings)
    rag_pipeline = setup_rag_pipeline(vector_store)
    
    return rag_pipeline, (model, tokenizer)

# Initialize at startup
rag_pipeline, (model, tokenizer) = initialize_system()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    question = request.form.get('question')
    if not question:
        return jsonify({"error": "No question provided"}), 400
    
    if rag_pipeline is None:
        return jsonify({"error": "RAG pipeline not initialized due to no data"}), 500
    
    answer, sources = query_rag(rag_pipeline, question)
    source_texts = [doc.page_content[:200] + "..." for doc in sources]
    
    # Use trained model for classification if available
    category = "Unknown"
    if model and tokenizer:
        inputs = tokenizer(question, return_tensors="pt", truncation=True, padding=True, max_length=512)
        outputs = model(**inputs)
        label = torch.argmax(outputs.logits, dim=1).item()
        category = "Allergy" if label == 1 else "Disease"
    
    return jsonify({
        "answer": answer,
        "sources": source_texts,
        "category": category
    })

if __name__ == '__main__':
    app.run(debug=True)
