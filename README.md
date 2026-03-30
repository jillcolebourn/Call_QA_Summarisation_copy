Here are the summarised steps for getting it running locally in windows:

1. create venv
2. activate venv 
    .venv\Scripts\Activate.ps1
3. install requirements
    pip install -r requirements.txt
4. run API backend
    uvicorn api_backend:app --reload --port 8000

5. leave the terminal running and start a new terminal

6. run the frontend 
    streamlit run streamlit_app.py --server.port=8501

This will get the code running locally without docker however you will need to make changes to teh get_llm() function to use the ChatOpenAI endpoint and remove the Azure credentials and secrets. You will also have to set the OpenAI API ket as an environmental variable