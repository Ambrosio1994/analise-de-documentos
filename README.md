# Análise de PDFs com IA

Este projeto permite que você faça o upload de um arquivo PDF e gere sumários ou análises de conteúdo utilizando modelos de linguagem avançados, como o GPT-4 ou equivalentes.

## Pré-requisitos

1. **Python 3.8+** (ou versão compatível).
2. **Chave de API** para o modelo que você deseja usar, por exemplo `OPENAI_API_KEY`:
   - Acesse https://platform.openai.com/account/api-keys.
   - Crie uma nova chave.
   - Copie a chave e edite o arquivo `.env` (ou renomeie `.env_example` para `.env`) para inserir sua chave:
     ```plaintext
     OPENAI_API_KEY="SUA_CHAVE_AQUI"
     ```
   - Se for usar outros provedores, adicione cada chave correspondente também em `.env` (ex.: `DEEP_SEEK_API_KEY`).

3. **Instale as dependências** listadas em [requirements.txt] ou execute:
   ```bash
   pip install -r requirements.txt
   ```
   Se não tiver um arquivo `requirements.txt`, instale individualmente os pacotes usados pelo projeto (ex.: `streamlit`, `langchain-openai`, `python-dotenv`, etc.).

## Executando o Projeto

1. Abra o terminal na pasta do projeto (por exemplo, `pdf_analysis/`).
2. Execute o aplicativo Streamlit:
   ```bash
   streamlit run app.py
   ```
3. A aplicação será aberta no seu navegador padrão, geralmente em http://localhost:8501.

## Funcionalidades Principais

- **Upload e Análise de PDF**: Faça o upload de um ou mais PDFs e visualize-os na barra lateral.  
- **Sumarização Automática**: Gere um sumário do PDF usando IA.  
- **Parâmetros Ajustáveis**: Mude valores de `temperature`, `max_tokens`, e `top_p` para personalizar a geração do texto.  
- **Flexibilidade de Prompts**: Personalize seus prompts por meio do LangChain Hub (ou outro repositório).  

## Estrutura dos Arquivos

A árvore de diretórios típica para este projeto é algo como:

```
pdf_analysis/
├── app.py         # Interface principal usando Streamlit
├── workflow.py    # Lida com o fluxo de análise e sumarização
├── model.py       # Configuração do modelo de linguagem (API Keys, etc.)
├── .env           # Variáveis de ambiente importantes (API Keys)
├── .gitignore
├── README.md
└── ...
```

## Observações

- Renomeie o arquivo `.env_example` para `.env` e adicione suas chaves de API.  
- Mantenha suas chaves privadas — o arquivo `.gitignore` já ignora por padrão o arquivo `.env` para não versioná-lo.  
- Caso precise de outras integrações (Twitter, Twilio, etc.), é só adicionar as chaves necessárias ao `.env`.  

## Contribuindo

Pull requests são bem-vindos. Para mudanças maiores, abra uma issue primeiro para discutir o que você gostaria de mudar. Fique à vontade para contribuir com melhorias, correções ou novas funcionalidades.