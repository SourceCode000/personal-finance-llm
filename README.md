# Personal Finance LLM

A fine-tuned LLM for personal finance guidance, deployed on AWS.

---

## Overview

This project fine-tunes an open-source LLM on personal finance data to answer questions about budgeting, savings, investments, and debt management. The model is deployed on AWS and served through a REST API built for production use.

---

## Tech Stack

- **Model:** Fine-tuned Llama / Mistral
- **Training:** PyTorch, Hugging Face Transformers, LoRA
- **Deployment:** AWS SageMaker, Lambda, API Gateway
- **Infra:** Docker, Terraform

---

## Getting Started

### Prerequisites
- Python 3.10+
- AWS account
- Docker

### Installation

```bash
git clone https://github.com/YOUR_USERNAME/personal-finance-llm.git
cd personal-finance-llm
pip install -r requirements.txt
```

### Usage

```bash
python inference.py --prompt "How should I start an emergency fund?"
```

---

## Example

**Prompt:** *"I earn $60k a year. How much should I save monthly?"*

**Response:** *"A common approach is the 50/30/20 rule — 50% needs, 30% wants, 20% savings. On $60k gross, that's roughly $800/month toward savings and debt repayment."*

---
