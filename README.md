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
