# README da API

## Visão Geral do Projeto

Este projeto é estruturado para fornecer uma arquitetura limpa, escalável e organizada para construir uma API utilizando FastAPI, SQLAlchemy e Pydantic. A API foi projetada para ser modular, permitindo fácil extensão e manutenção. Os principais componentes do projeto estão organizados em diretórios específicos para separar responsabilidades e garantir uma estrutura clara e eficiente.

## Estrutura de Pastas

### `app/`
- Diretório principal da aplicação. Contém todos os subdiretórios e arquivos que compõem a aplicação.

### `api/`
- Contém os endpoints da API. Dentro deste diretório, é possível organizar diferentes versões da API (como `v1/`, `v2/`) e subdiretórios para diferentes grupos de endpoints (ex: `users.py`, `items.py`).

### `core/`
- Armazena a configuração central e funcionalidades principais do projeto, como:
  - `config.py`: Configurações da aplicação (ex: variáveis de ambiente).
  - `security.py`: Configurações de segurança, como autenticação e autorização.
  - Inicialização de logs e outras configurações centrais.
    
### `schemas/`
- Contém os esquemas Pydantic, que são utilizados para validação de dados nas requisições e respostas da API. Isso garante que os dados manipulados estejam no formato esperado e sigam as regras de negócio.

### `services/`
- Este diretório armazena classes e funções que implementam a lógica de negócios do projeto, como:
  - Operações em PDFs.
  - Integrações com serviços de terceiros.
  - Qualquer outra classe utilitária que não esteja diretamente relacionada ao banco de dados ou aos esquemas.

### `utils/`
- Contém funções utilitárias que podem ser usadas em várias partes do projeto, como:
  - `pdf_generator.py`: Geradores de PDFs.
  - Funções auxiliares e outras ferramentas utilitárias.

### `tests/`
- Diretório que contém os testes automatizados da aplicação. Cada arquivo de teste (ex: `test_main.py`, `test_users.py`) pode testar diferentes partes da aplicação, garantindo que a API funcione conforme esperado.

