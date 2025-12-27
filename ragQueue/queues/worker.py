from dotenv import load_dotenv
from openai import OpenAI 
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
load_dotenv()
openai_client = OpenAI()
embedding_model= OpenAIEmbeddings(
    model="text-embedding-3-large"
)
vector_db= QdrantVectorStore.from_existing_collection(
    url="http://host.docker.internal:6333",
    collection_name="learning_rag",
    embedding=embedding_model,
)
def process_query(query:str):
    print("Processing query in worker...")
    search_results= vector_db.similarity_search(query=query)
    context= "\n\n\n".join([f"Page Content:{result.page_content}\n Page Number: {result.metadata['page_label']} \n File Location: {result.metadata['source']}"
                            for result in search_results])
    SYSTEM_PROMPT= f"""You
    are a helpfull Al Assistant who answeres user query based on the available
    context retrieved from a PDF file along with page_contents and page number.
    You should only ans the user based on the following context and navigate the
    user to open the right page number to know more.
    Context: {context}"""
    response= openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT },
            {"role": "user", "content": query},
        ]
    )
    print(f"AI:{response.choices[0].message.content}")
    return response.choices[0].message.content