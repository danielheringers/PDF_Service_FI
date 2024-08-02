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
