from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate    

load_dotenv()

embedding_model = HuggingFaceEmbeddings()

vectorstore = Chroma(
    embedding_function=embedding_model,
    persist_directory="chroma_db"
)

retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k":3,
        "fetch_k":10,
        "lambda_mult":0.5
   }
)

llm = ChatMistralAI(model="mistral-small-latest")

#prompt_template
prompt= ChatPromptTemplate.from_messages(
    [
        ("system", """ you are a helpful assistant that provides context to answer user queries.

         if the answer is not present in the context, say : not found in the context."""),
        (
            "human", """context: {context}
             question: {question}"""
         )
    ]
)

print("\nRAG System:\n")
print("press 0 to exit\n")

while True:
    query = input ("You: ")
    if query == "0":
        print("Exiting...")
        break

    docs = retriever.invoke(query)
    context = "\n".join([doc.page_content for doc in docs])
    final_prompt = prompt.invoke({"context": context, "question": query})
    response = llm.invoke(final_prompt) #llm = generate answer based on the retrieved context and user query

    response= llm.invoke(final_prompt)
    print(f"AI: {response.content}\n")

# Retriever = Finds information
# User Question
#       ↓
# Embedding Created
#       ↓
# Vector Similarity Search
#       ↓
# Relevant Chunks Returned