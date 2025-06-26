## Visão Geral do Projeto

Este projeto é estruturado para fornecer uma arquitetura limpa, escalável e organizada para construir uma API utilizando **FastAPI**. A API foi projetada para ser modular, permitindo fácil extensão e manutenção. Os principais componentes do projeto estão organizados em diretórios específicos para separar responsabilidades e garantir uma estrutura clara e eficiente.

## Estrutura de Pastas

- **app**  
  Diretório principal da aplicação. Contém todos os subdiretórios e arquivos que compõem a aplicação.

- **api/**  
  Contém os endpoints da API. Dentro deste diretório, é possível organizar diferentes versões da API (como `v1/`, `v2/`) e subdiretórios para diferentes grupos de endpoints (ex: `users.py`, `items.py`).

- **core/**  
  Armazena a configuração central e funcionalidades principais do projeto, como:

  - **config.py**: Configurações da aplicação (ex: variáveis de ambiente).
  - **security.py**: Configurações de segurança, como autenticação e autorização.
  - Inicialização de logs e outras configurações centrais.

- **schemas/**  
  Contém os esquemas **Pydantic**, que são utilizados para validação de dados nas requisições e respostas da API. Isso garante que os dados manipulados estejam no formato esperado e sigam as regras de negócio.

- **services/**  
  Este diretório armazena classes e funções que implementam a lógica de negócios do projeto, como:

  - Operações em PDFs.
  - Integrações com serviços de terceiros.
  - Qualquer outra classe utilitária que não esteja diretamente relacionada ao banco de dados ou aos esquemas.

- **utils/**  
  Contém funções utilitárias que podem ser usadas em várias partes do projeto, como:

  - **general_pdf_utils.py**: Funções auxiliares.
  - Funções auxiliares e outras ferramentas utilitárias.

- **tests/**  
  Diretório que contém os testes automatizados da aplicação. Cada arquivo de teste (ex: `test_main.py`, `test_users.py`) pode testar diferentes partes da aplicação, garantindo que a API funcione conforme esperado.

## Configuração e Execução

### Pré-requisitos

- Python 3.8+
- Pipenv (para gerenciamento de dependências)

### Instalação

Clone o repositório:

```bash
git clone <URL-do-repositório>
```

Instale as dependências:

```bash
pipenv install
```

Ative o ambiente virtual:

```bash
pipenv shell
```

### Executando a Aplicação

Para rodar a aplicação em modo de desenvolvimento:

```bash
uvicorn app.main:app --reload --port 8004
uvicorn app.main:app --host 127.0.0.1 --port 8004 --workers 4
```

### Sugiro Criar um alias para facilitar

Criar um comando no seu terminal (opcional)

Se você não quer rodar o Python diretamente, pode criar um alias ou comando no seu terminal.

#### No Linux/macOS:

```
alias runapi="uvicorn app.main:app --reload --port 8004"
```

Depois, recarregue o terminal com:

source ~/.bashrc

Agora, você pode rodar sua API com:

runapi

No Windows:

Adicione o caminho do script ao Path do sistema ou crie um arquivo .bat para executar o comando Python.

## Estrutura de Endpoints

- **Health Check**

  - `GET /health`: Verifica se a API está funcionando corretamente.

- **DFe (Documentos Fiscais Eletrônicos)**

  - `POST /dfes/mdfe/damdfe`: Gera o DAMDFE (Documento Auxiliar de Manifesto Eletrônico de Documentos Fiscais).

- **Boletos**
  - `POST /boletos`: Gera boletos bancários em PDF.

## Testes

Para rodar os testes automatizados:

```bash
pytest
```

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.

---

# Utilizando Pydantic para Modelagem de Dados

## O que é Pydantic?

Pydantic é uma biblioteca de validação de dados e configuração baseada em Python. Ela permite a criação de modelos de dados que garantem que os dados manipulados estejam no formato esperado e sigam as regras de negócio definidas. Pydantic utiliza a tipagem estática do Python para definir e validar dados de forma eficiente e intuitiva.

## Como Montar um Modelo Pydantic

Para criar um modelo Pydantic, você define uma classe que herda de `BaseModel` e utiliza anotações de tipo para definir os campos e suas validações.

### Exemplo de Modelo

```python
from pydantic import BaseModel, Field
from typing import Optional

class Usuario(BaseModel):
    nome: str
    idade: int
    email: Optional[str] = Field(None, description="E-mail do usuário")

# Instanciando o modelo
usuario = Usuario(nome="João", idade=30, email="joao@example.com")
```

## Possibilidades que Pydantic Permite

### 1. Validação Automática

Pydantic valida automaticamente os dados de entrada com base nas anotações de tipo. Se os dados não estiverem no formato esperado, uma exceção será levantada.

### 2. Conversão de Tipos

Pydantic tenta converter os tipos de dados automaticamente. Por exemplo, se um campo é definido como `int` e uma string que representa um número é fornecida, Pydantic tentará converter a string para um inteiro.

### 3. Campos Opcionais

Campos podem ser definidos como opcionais usando `Optional` do módulo `typing`. Isso permite que os campos sejam omitidos sem causar erros de validação.

### 4. Campos Aninhados

Pydantic permite a definição de campos aninhados, onde um campo pode ser outro modelo Pydantic. Isso facilita a modelagem de estruturas de dados complexas.

### 5. Descrições e Documentação

Usando o parâmetro `description` do `Field`, você pode adicionar descrições aos campos, o que melhora a documentação e a legibilidade do código.

### 6. Valores Padrão

Campos podem ter valores padrão definidos, o que permite que os modelos sejam instanciados com valores padrão quando certos campos não são fornecidos.

## Exemplo de Uso

Aqui está um exemplo de como instanciar e usar os modelos Pydantic definidos:

```python
from typing import List

class Endereco(BaseModel):
    rua: str
    cidade: str
    estado: str
    cep: str

class Usuario(BaseModel):
    nome: str
    idade: int
    enderecos: List[Endereco] = []

# Instanciando os modelos
endereco = Endereco(rua="Rua das Flores", cidade="São Paulo", estado="SP", cep="12345-678")
usuario = Usuario(nome="Maria", idade=25, enderecos=[endereco])
```

Com Pydantic, você pode garantir que seus dados estejam sempre no formato correto e que todas as validações necessárias sejam aplicadas automaticamente, facilitando o desenvolvimento e a manutenção do seu projeto.

## Documentação Oficial

Para mais detalhes, consulte a [documentação oficial do Pydantic](https://pydantic-docs.helpmanual.io/).

---

# Geração de PDF com ReportLab

## O que é o ReportLab?

O ReportLab é uma biblioteca Python utilizada para a criação de documentos PDF de maneira programática. Com ele, é possível desenhar elementos como texto, imagens, tabelas e gráficos diretamente no PDF, o que é muito útil para geração de relatórios e documentos automatizados.

## Estrutura da Função `generate_damdfe_pdf_bytes`

Criada para os documentos `damdfe`, na rota `/dfe/mdfe/damdfe`, a função `generate_damdfe_pdf_bytes` gera um documento PDF baseado em um modelo de dados chamado `DamdfePayload`. Essa função utiliza a biblioteca ReportLab para desenhar elementos gráficos no PDF, incluindo texto, QR Codes, códigos de barras e imagens.

## Estrutura da Função `generate_dacte_pdf_bytes`

Criada para os documentos `dacte`, na rota `/dfe/cte/dacte`, a função `generate_dacte_pdf_bytes` gera um documento PDF baseado em um modelo de dados chamado `DactePayload`. Essa função utiliza a biblioteca ReportLab para desenhar elementos gráficos no PDF, incluindo texto, QR Codes, códigos de barras e imagens.

### Exemplo Simples

Aqui está uma explicação mais detalhada de cada método utilizado no código e exemplos básicos de como usá-los.

### 1. Configuração Inicial e Criação do Canvas

O `canvas.Canvas` é o ponto de partida para criar um PDF. Ele representa a "tela" onde os elementos serão desenhados.

```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO

buffer = BytesIO()
pdf_canvas = canvas.Canvas(buffer, pagesize=A4)
```

### 2. Desenhando Texto no PDF

Para desenhar texto, o ReportLab permite especificar a fonte, tamanho e posição no PDF usando os métodos `setFont` e `drawString`.

```python
pdf_canvas.setFont("Helvetica", 12)  # Define a fonte e o tamanho
pdf_canvas.drawString(50, 800, "Exemplo de texto no PDF")  # Define a posição do texto no PDF
```

### 3. Adicionando Imagens

No exemplo fornecido, uma imagem de logo é desenhada no PDF. O ReportLab usa `drawImage` para inserir imagens no documento.

```python
from reportlab.lib.utils import ImageReader
import base64

logo_data = base64.b64decode("imagem_base64")  # Decodifique o logo se estiver em base64
logo_image = ImageReader(BytesIO(logo_data))
pdf_canvas.drawImage(logo_image, x=10, y=750, width=100, height=50)  # Posição e tamanho da imagem
```

### 4. Desenhando um QR Code

Para gerar um QR Code, a biblioteca `qrcode` é usada para criar a imagem. A imagem resultante é então desenhada no PDF.

```python
import qrcode
from reportlab.lib.units import mm

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data("https://www.exemplo.com")  # Adiciona dados ao QR code
qr.make(fit=True)
qr_image = qr.make_image(fill_color="black", back_color="white")
image_reader = ImageReader(BytesIO())
qr_image.save(image_reader, format="PNG")
pdf_canvas.drawImage(image_reader, x=150*mm, y=250*mm, width=50, height=50)
```

### 5. Adicionando Código de Barras

Para códigos de barras, a biblioteca `reportlab.graphics.barcode` é usada para gerar e posicionar o código de barras no documento.

```python
from reportlab.graphics.barcode import code128

barcode = code128.Code128("123456789", barWidth=0.3 * mm, barHeight=15 * mm)
barcode.drawOn(pdf_canvas, 100, 500)  # Desenha o código de barras na posição especificada
```

### 6. Desenhando Retângulos e Outras Formas

É possível desenhar formas simples, como retângulos, com o método `rect`. No exemplo, um retângulo é desenhado ao redor do logo.

```python
pdf_canvas.rect(10 * mm, 250 * mm, 30 * mm, 18 * mm, stroke=1, fill=0)  # Retângulo na posição e tamanho desejados
```

### 7. Conclusão do PDF e Retorno dos Dados

Para finalizar o PDF, chamamos `showPage()` e `save()`. Em seguida, retornamos o buffer que contém o PDF gerado.

```python
pdf_canvas.showPage()  # Finaliza a página atual
pdf_canvas.save()      # Salva o conteúdo do PDF
buffer.seek(0)         # Posiciona o buffer no início
return buffer
```

## Exemplo Básico Completo

```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO

def generate_sample_pdf():
    buffer = BytesIO()
    pdf_canvas = canvas.Canvas(buffer, pagesize=A4)

    # Adicionando texto
    pdf_canvas.setFont("Helvetica-Bold", 16)
    pdf_canvas.drawString(100, 750, "Exemplo de Geração de PDF com ReportLab")

    # Adicionando retângulo
    pdf_canvas.rect(100, 720, 200, 25, stroke=1, fill=0)

    # Finalizando e retornando o PDF
    pdf_canvas.showPage()
    pdf_canvas.save()
    buffer.seek(0)
    return buffer
```

Esse código cria um PDF com texto e um retângulo simples, demonstrando como usar o ReportLab para desenhar elementos no PDF.

## Documentação Oficial

Para mais detalhes, consulte a [documentação oficial do ReportLab](https://www.reportlab.com/docs/reportlab-userguide.pdf)!

---
 