from langchain_openai import ChatOpenAI
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

"""
Módulo responsável pela configuração do modelo de linguagem e pela lógica
mais simples de summarização de texto.

Neste módulo, criamos uma instância de ChatOpenAI configurada para utilizar
a API do DeepSeek e definimos uma função de sumarização simples com base em
um fluxo (prompt -> LLM -> parser).
"""

load_dotenv()

def get_model(temperature: float,
              max_tokens: int,
              top_p: float) -> ChatOpenAI:
    """
    Configura e retorna uma instância do modelo ChatOpenAI baseado na API
    do DeepSeek.

    Args:
        temperature (float): Controla a aleatoriedade na geração do texto (0 a 1).
        max_tokens (int): Número máximo de tokens para a geração.
        top_p (float): Probabilidade de corte para nucleus sampling (0 a 1).

    Returns:
        ChatOpenAI: Instância configurada para gerar textos usando a API DeepSeek.
    """
    return ChatOpenAI(
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),  # A chave deve estar armazenada no arquivo .env
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
    )

def summarizer(text: str) -> str:
    """
    Gera um sumário a partir de um texto de entrada, usando um pipeline
    pré-configurado de prompt -> modelo -> parser.

    Esta função puxa um prompt do LangChain Hub, que se encontra em
    'ambrosio/space-today', e utiliza configurações conservadoras
    (temperature=0) para produzir um sumário determinístico.

    Args:
        text (str): Texto de entrada a ser sumarizado.

    Returns:
        str: Sumário gerado pelo modelo.
    """
    # Importa o prompt do LangChain hub
    prompt = hub.pull("ambrosio/space-today")
    
    # Configura um modelo com poucos tokens para sumarização
    llm = get_model(
        max_tokens=2000,
        temperature=0,  # output determinístico
        top_p=0.95
    )
    
    # Configura o pipeline: prompt -> LLM -> parser de string
    chain = prompt | llm | StrOutputParser()
    
    # Retorna a saída do pipeline
    return chain.invoke({"text": text})