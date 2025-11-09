"""Common error handling utilities."""
from __future__ import annotations

from flask import jsonify


_ERROR_MESSAGES = {
    200: "Solicitação feita com sucesso.",
    400: "Parametros incorretos.",
    401: "Acesso não autorizado.",
    403: "Arquivo não encontrado.",
    404: "Dados não encontrados.",
    408: "Timeout.",
    500: "Erro interno do servidor.",
}


def error_response(status_code: int):
    message = _ERROR_MESSAGES.get(status_code, "Erro desconhecido")
    return jsonify({"error": str(status_code), "error_desc": message}), status_code
