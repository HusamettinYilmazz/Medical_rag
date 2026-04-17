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

# BM25 Analysis

# RRF Analysis
- What does k (default 60) do?
the author idicates
> We conducted four pilot experiments, each combining the results of 30 configurations of Wumpus Search applied to four different TREC collections. The results of the first, shown in table 1, indicated that k = 60 was near-optimal

So we can say it is Emprical result

1. What happens at k=0 vs k=1000?
k is a smoothing constant 
- small k let top ranks dominates:
At K=0 
one document ranked first in one list will dominate all other documents even if we have a document ranked 2 in multiple lists

- large k like k=1000 ignores the exact rank and cares more about wheter the item appears in multiple lists

2. Why use rank position instead of raw scores when combining BM25 with cosine similarity?

Because of scale mismatch, it is a well known problem appears in e.g loss functions 

addin to different scales like unbounded BM25  and bounded cosine similarity (0-1), will make the unbounded one dominates the result easily



# Evaluation
To tell the truth I used what ever chatgpt suggested me I didn't work that much over NLP evaluation before, so I don't have that much knowladge

# Hardest problem
the system isn't hard but some details needs time like evaluation part.

# Scenario Question
> Your team needs to benchmark a 70B open-source LLM for medical QA. Your usual GPU provider doesn't have L40S available today. Your manager is busy all day. Results needed by end of week.

## What do you do? Be specific — platforms, alternatives, trade-offs.

1. If we are allowed to use any paltform, I will use vast.ai they provide cheap GPU

2. I will use multible gpus (distributed) from the same provider
