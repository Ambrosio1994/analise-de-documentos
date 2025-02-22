from workflow import response

import streamlit as st
import tempfile
import base64

"""
Módulo principal do app de análise de artigos científicos com IA.

Este módulo utiliza Streamlit para criar uma interface de usuário
permitindo que o usuário faça upload de um PDF de um artigo científico.
Em seguida, o arquivo é processado por um pipeline de IA para gerar um
resumo e exibir o PDF na barra lateral.
"""

# Page configuration
st.set_page_config(
    page_title="Análise de artigos científicos com IA",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Análise de artigos científicos com IA")

def main():
    """
    Função principal que controla o fluxo do aplicativo Streamlit.

    1. Inicializa variáveis de sessão para armazenar o PDF carregado e o
       estado de processamento.
    2. Cria a barra lateral para configurar parâmetros do modelo e fazer
       upload do PDF.
    3. Quando o PDF é carregado, ele é gravado em um arquivo temporário,
       e o conteúdo é exibido na barra lateral através de um iframe.
    4. Chama a função 'response()' para processar o PDF e exibe o resultado.
    """

    # Se os valores não existirem na sessão, inicializa eles como None ou False
    if 'uploaded_pdf' not in st.session_state:
        st.session_state.uploaded_pdf = None
    if 'processing' not in st.session_state:
        st.session_state.processing = False

    # Sidebar: parâmetros do modelo
    with st.sidebar:
        st.title("Parâmetros do modelo")
        temperature = st.slider("Temperatura", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
        max_tokens = st.slider("Máximo de tokens", min_value=1000, max_value=128000, value=38000, step=100)
        top_p = st.slider("Top P", min_value=0.0, max_value=1.0, value=0.7, step=0.05)

        # Área de upload do PDF
        st.sidebar.markdown("### 📎 Upload do artigo")
        uploaded_file = st.file_uploader(
            "Faça upload de um arquivo PDF",
            type=['pdf'],
            help="Faça upload de um artigo científico para análise"
        )

    # Verifica se foi carregado um arquivo e se ainda não está em processamento
    if uploaded_file is not None and not st.session_state.processing:
        st.session_state.processing = True
        
        # Move o container do PDF para a barra lateral
        pdf_container = st.sidebar.container()

        # Cria arquivo temporário para gravação do PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            temp_path = tmp_file.name

            # Lê o conteúdo do PDF e armazena-o para exibição
            with open(temp_path, "rb") as pdf_file:
                st.session_state.uploaded_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
            
            # Exibe PDF na barra lateral
            with pdf_container:
                st.markdown(
                    f"""
                    <div style="height: 400px; overflow-y: scroll; border: 1px solid #ccc; padding: 10px;">
                        <iframe 
                            src="data:application/pdf;base64,{st.session_state.uploaded_pdf}" 
                            width="100%" 
                            height="100%" 
                            style="border: none;"
                        ></iframe>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # Chama a função de resposta do workflow
            resp = response(temp_path,
                            temperature=temperature,
                            max_tokens=max_tokens,
                            top_p=top_p)

            st.success("Documento processado com sucesso!")
            st.write(resp)

if __name__ == "__main__":
    main()