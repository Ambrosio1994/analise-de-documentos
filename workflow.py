from model import get_model, summarizer

from langchain import hub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyMuPDFLoader

from typing import Optional
from concurrent.futures import ThreadPoolExecutor
import streamlit as st

"""
Módulo 'workflow' que orquestra o carregamento do PDF, divisão em chunks,
resumo de cada chunk e construção da resposta final via cadeia de prompts.
"""

def load_pdf(file_path: str, chunk_size=8000, overlap=1000) -> list[Document]:
    """
    Carrega um PDF e divide seu conteúdo em chunks processáveis.

    Args:
        file_path (str): Caminho para o arquivo PDF.
        chunk_size (int, opcional): Tamanho máximo de cada chunk em caracteres.
        overlap (int, opcional): Sobreposição entre chunks em caracteres.

    Returns:
        list[Document]: Lista de documentos chunkados para processamento posterior.
    """
    # Usa o PyMuPDFLoader para ler o PDF
    loader = PyMuPDFLoader(file_path=file_path)
    docs = loader.load()

    # Divide os documentos em chunks usando RecursiveCharacterTextSplitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = splitter.split_documents(docs)

    st.success(f"Documento dividido")
    return chunks

def process_chunk(chunk: Document) -> str:
    """
    Processa individualmente um chunk de texto, gerando um sumário.

    Args:
        chunk (Document): Um chunk de texto (objeto Document).

    Returns:
        str: Sumário gerado para o chunk fornecido.
    """
    return summarizer(chunk.page_content)

def text_summary(pdf_path: str) -> str:
    """
    Carrega, divide e processa um PDF para gerar sumários chunk a chunk.

    Args:
        pdf_path (str): Caminho para o PDF.

    Returns:
        str: Sumário concatenado de todos os chunks processados.
    """
    chunks = load_pdf(pdf_path)
    progress_bar = st.progress(0, text="Iniciando processamento...")
    total_chunks = len(chunks)

    summaries = []
    # Usa ThreadPoolExecutor para paralelizar o processamento dos chunks
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = list(executor.map(process_chunk, chunks))
        for i, summary in enumerate(futures):
            if summary and summary.strip():
                summaries.append(summary)
            progress = (i + 1) / total_chunks
            progress_bar.progress(progress, text=f"Processando chunk {i+1} de {total_chunks}...")

    st.success(f"Processamento concluído")
    return " ".join(summaries)

def response(pdf_path: str,
             temperature: float,
             max_tokens: int,
             top_p: float,
             max_retries: int = 3) -> Optional[str]:
    """
    Orquestra o processo de summarização e geração de resposta final a partir
    de um PDF. Primeiramente gera um sumário do PDF todo (via text_summary),
    e depois chama um prompt do LangChain Hub para formatar a resposta final
    usando o modelo configurado.

    Args:
        pdf_path (str): Caminho para o arquivo PDF.
        temperature (float): Controla a aleatoriedade (0 a 1).
        max_tokens (int): Número máximo de tokens para geração de texto.
        top_p (float): Parâmetro top_p para sampling (0 a 1).
        max_retries (int, opcional): Número de tentativas em caso de falhas consecutivas.

    Returns:
        Optional[str]: Texto gerado pelo modelo ou None se não houver saída válida.
    """
    for _ in range(max_retries):
        # Gera sumário do conteúdo do PDF
        summary_article = text_summary(pdf_path)
        
        # Configura modelo com base nos parâmetros fornecidos
        model = get_model(
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p
        )
        
        # Puxa prompt do Hub e encadeia com o modelo e parser
        prompt = hub.pull("ambrosio/ciencia-sem-fim")
        chain = prompt | model | StrOutputParser()

        with st.spinner("Escrevendo..."): 
            result = chain.invoke({"query": summary_article})
            if result and result.strip():
                return result

    # Caso não seja possível gerar saída válida após max_retries
    return None