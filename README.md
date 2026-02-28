# SupportLens

SupportLens is a lightweight observability platform for a customer support chatbot. It consists of:
1. A **Support Chatbot** (using Hugging Face free LLMs via InferenceClient).
2. A **Backend API** (FastAPI, SQLite) to handle generating responses and classifying traces into explicit categories.
3. An **Observability Dashboard** (React, Vite, Tailwind CSS) displaying aggregate metrics and an interactive stream of conversation traces.

## Running Locally

Everything is containerized and runs with a single command. 

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) installed and running.
- A free Hugging Face API token (for LLM calling).

### Quickstart

1. Clone or navigate to this repository.
2. In the root directory (where `docker-compose.yml` is located), create a `.env` file and add your Hugging Face API token:
   ```bash
   HF_TOKEN="hf_your_huggingface_access_token_here"
   ```
   *(Note: The server uses `meta-llama/Llama-3.2-3B-Instruct` which is freely available on the Serverless Inference API)*

3. Run the container cluster:
   ```bash
   docker-compose up --build
   ```

4. Open your browser and navigate to:
   - **App:** [http://localhost:5173](http://localhost:5173) (Interact with the Chatbot on the left and see the Dashboard on the right).
   - **Backend API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI).

### Architecture Notes
- The database is seeded with 20 traces on first startup.
- The Dashboard automatically refreshes whenever a new trace is sent from the Chat section.
- **Classification Approach:** The conversation intent is classified strictly into one of 5 classes (Billing, Refund, Account Access, Cancellation, General Inquiry) using a zero-shot system prompt tailored for LLMs.
