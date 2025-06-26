from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

def traduzir_mensagem(msg: str, tipo: str) -> str:
    traducoes = {
        "missing": "O campo é obrigatório. Por favor, forneça um valor para este campo.",
        "string_type": "O campo deve ser uma string válida. Verifique o tipo do dado fornecido.",
        "type_error.str": "O campo deve ser uma string. Verifique o tipo do dado fornecido.",
        "value_error.none.not_allowed": "O campo não pode ser nulo. Por favor, forneça um valor válido.",
        "value_error.any_str.min_length": "O campo deve ter pelo menos {limit_value} caracteres.",
        "value_error.any_str.max_length": "O campo deve ter no máximo {limit_value} caracteres.",
        "value_error.number.not_gt": "O valor deve ser maior que {limit_value}.",
        "value_error.number.not_lt": "O valor deve ser menor que {limit_value}.",
    }
    if tipo in traducoes and "{limit_value}" in traducoes[tipo]:
        return traducoes[tipo].format(limit_value=msg)
    return traducoes.get(tipo, msg)

def formatar_erro(erro: dict) -> dict:
    localizacao = " -> ".join([str(elem) for elem in erro.get("loc", [])])
    mensagem = traduzir_mensagem(erro.get("msg", ""), erro.get("type", ""))
    return {"localizacao": localizacao, "mensagem": mensagem, "tipo": erro.get("type", "")}

async def manipulador_validacao(request: Request, exc: RequestValidationError):
    erros_formatados = [formatar_erro(erro) for erro in exc.errors()]
    return JSONResponse(status_code=422, content={"detalhes": erros_formatados})
