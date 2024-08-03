# Projeto de Geração de PDF de DANFE

Este projeto gera um Documento Auxiliar da Nota Fiscal Eletrônica (DANFE) em formato PDF a partir de dados fornecidos em um arquivo JSON.

## Estrutura do Projeto


### Arquivos Principais

- `danfe.py`: Arquivo principal que carrega os dados do JSON e gera o PDF.
- `utils.py`: Contém funções utilitárias para formatação de dados.
- `danfe_render_nfe.py`: Contém as funções responsáveis por renderizar as páginas e os itens do DANFE.
- `payload.json`: Exemplo de arquivo JSON contendo os dados da Nota Fiscal.

## Funcionalidades

- Geração de PDF de DANFE com múltiplas páginas.
- Formatação de valores monetários, datas, CNPJ/CPF e números de celular.
- Inclusão de numeração de páginas.

## Dependências

- `reportlab`: Biblioteca para geração de PDFs.
- `locale`: Para formatação de moeda.
- `datetime`: Para manipulação de datas.
- `json`: Para leitura de arquivos JSON.
- `re`: Para manipulação de strings.

# PDF Generator API

Esta é uma API desenvolvida com FastAPI que permite a geração de documentos fiscais e financeiros em formato PDF. A API utiliza a biblioteca ReportLab para renderizar os PDFs.

## Estrutura do Projeto

## Estrutura dos Arquivos

-   `main.py`: Configuração principal do FastAPI.
-   `pdf_generator.py`: Rotas relacionadas à geração de PDFs.
-   `pdf_utils.py`: Utilitários para geração de PDFs.
-   `danfe_utils.py`: Funções específicas para geração de PDFs de DANFE.
-   `danfe_render_nfe.py`: Funções de renderização de páginas DANFE.

## Dependências

-   `fastapi`: Framework web para Python.
-   `reportlab`: Biblioteca para geração de PDFs.
-   `uvicorn`: Servidor ASGI para execução do FastAPI.

## Contribuição

Contribuições são bem-vindas! Por favor, envie um pull request ou abra uma issue para discutir o que você gostaria de mudar.