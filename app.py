from flask import Flask, jsonify, render_template, request
from langchain.vectorstores import Chroma 
from dotenv import load_dotenv
from src.helper import repo_ingestion, load_embedding
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryMemory
import os 



app = Flask(__name__, template_folder='template')

load_dotenv()
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')


embedding = load_embedding()
presist_directory = "db"

vectordb = Chroma(persist_directory=presist_directory,
                  embedding_function=embedding)



llm = ChatOpenAI(model= 'qwen/qwen3-4b:free',
             base_url="https://openrouter.ai/api/v1",
             api_key=OPENROUTER_API_KEY,
)


memory = ConversationSummaryMemory(llm=llm, memory_key="chat_history", return_messages=True)

rag_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectordb.as_retriever(search_type='mmr', search_kwargs={'k':8}),
    memory=memory
)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("chat.html")


@app.route('/chatbot', methods=['GET', 'POST'])
def gitRepo():

    if request.method == "POST":
        user_input = request.form['question']
        repo_ingestion(user_input)
        os.system("python store_index.py")

    return jsonify({'response': str(user_input)})


@app.route('/get', methods=['GET', 'POST'])
def chat():
    msg = request.form['msg']
    input = msg
    print(input)

    if input == 'clear':
        os.system('rm -rf repo')

    result = rag_chain(input)
    print(result['answer'])
    return str(result['answer'])


if __name__ == '__main__':
    app.run(debug=True)