<h1 align="center"> Medical RAG system </h1>

# Setup & Usage

## 1. Installation

clone the repo
```bash
git clone git@github.com:HusamettinYilmazz/Medical_rag.git
cd Medical_rag/
```

build conda environment
```bash
conda create -n medical_rag python==3.9
conda activate medical_rag
```

install requirements
```bash
pip install -r requirements.txt
```

copy .env.example to .env
and update creditanals like LLM_API_KEY
```bash
cp .env.example .env
```

run the system from main.py
```bash 
python3 main.py
```

# Approach 
## model choice, trade-offs, what you'd change with more time.

1. I would invest more time understanding the data (required domain knowladge) and the hall system

2. I made some basic choices I would investagte more in evaluation metrics and their meaning to bussiness (since our metrics are proxy metrics not direct metrics)

3. I tried as much as I can to write clean code but since it is required to finish the system in 3-4 hours I decided to not spend much time in code orgnization (Maybe It's ok for an assessment but nor for production)

4. 

