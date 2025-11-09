"""API documentation routes."""
from __future__ import annotations

from typing import Any

from flask import Blueprint, current_app, jsonify, request, url_for

docs_bp = Blueprint("docs", __name__)


@docs_bp.get("/docs")
def api_docs() -> tuple[Any, int]:
    """List all available API routes with examples."""
    app = current_app
    routes_info = []
    
    # Base URL - tenta detectar automaticamente ou usa um padrão
    base_url = request.host_url.rstrip("/")
    
    # Mapeamento de rotas com informações detalhadas
    route_details = {
        # AI Routes
        "ai.ai_gpt4": {
            "path": "/ai/gpt4",
            "method": "GET",
            "description": "Gera texto usando GPT-4",
            "required_params": ["apikey", "input"],
            "optional_params": [],
            "example": f"{base_url}/ai/gpt4?apikey=SUA_API_KEY&input=Olá, como você está?",
        },
        "ai.ai_frosting": {
            "path": "/ia/frosting",
            "method": "GET",
            "description": "Gera imagem usando Frosting AI",
            "required_params": ["apikey", "input"],
            "optional_params": ["model", "inputnegative", "auto"],
            "example": f"{base_url}/ia/frosting?apikey=SUA_API_KEY&input=um gato fofo&model=anime&auto=1",
        },
        # Alerts Routes
        "alerts.free_games": {
            "path": "/alert/games",
            "method": "GET",
            "description": "Lista jogos grátis disponíveis (rate limit: 1 por 4 minutos)",
            "required_params": ["apikey"],
            "optional_params": [],
            "example": f"{base_url}/alert/games?apikey=SUA_API_KEY",
        },
        # Downloads Routes
        "downloads.download_general": {
            "path": "/downloader/geral",
            "method": "GET",
            "description": "Baixa conteúdo de redes sociais",
            "required_params": ["apikey", "input"],
            "optional_params": [],
            "example": f"{base_url}/downloader/geral?apikey=SUA_API_KEY&input=https://www.youtube.com/watch?v=VIDEO_ID",
        },
        "downloads.serve_temp_image": {
            "path": "/temp_image/<filename>",
            "method": "GET",
            "description": "Serve imagens temporárias",
            "required_params": ["filename"],
            "optional_params": [],
            "example": f"{base_url}/temp_image/imagem.png",
        },
        # LastFM Routes
        "lastfm.register_user": {
            "path": "/fm/register",
            "method": "GET",
            "description": "Registra um usuário do Last.fm",
            "required_params": ["apikey", "user", "number"],
            "optional_params": [],
            "example": f"{base_url}/fm/register?apikey=SUA_API_KEY&user=nomeusuario&number=5511999999999",
        },
        "lastfm.album": {
            "path": "/fm/album",
            "method": "GET",
            "description": "Obtém informações do álbum atual",
            "required_params": ["apikey", "number"],
            "optional_params": [],
            "example": f"{base_url}/fm/album?apikey=SUA_API_KEY&number=5511999999999",
        },
        "lastfm.top_albums": {
            "path": "/fm/top/album",
            "method": "GET",
            "description": "Obtém top 5 álbuns do usuário",
            "required_params": ["apikey", "number"],
            "optional_params": [],
            "example": f"{base_url}/fm/top/album?apikey=SUA_API_KEY&number=5511999999999",
        },
        "lastfm.top_tracks": {
            "path": "/fm/top/track",
            "method": "GET",
            "description": "Obtém top 5 músicas do usuário",
            "required_params": ["apikey", "number"],
            "optional_params": [],
            "example": f"{base_url}/fm/top/track?apikey=SUA_API_KEY&number=5511999999999",
        },
        "lastfm.top_artists": {
            "path": "/fm/top/artist",
            "method": "GET",
            "description": "Obtém top 5 artistas do usuário",
            "required_params": ["apikey", "number"],
            "optional_params": [],
            "example": f"{base_url}/fm/top/artist?apikey=SUA_API_KEY&number=5511999999999",
        },
        "lastfm.artist": {
            "path": "/fm/artist",
            "method": "GET",
            "description": "Obtém informações do artista atual",
            "required_params": ["apikey", "number"],
            "optional_params": [],
            "example": f"{base_url}/fm/artist?apikey=SUA_API_KEY&number=5511999999999",
        },
        "lastfm.recent": {
            "path": "/fm/recent",
            "method": "GET",
            "description": "Obtém música recente do usuário",
            "required_params": ["apikey"],
            "optional_params": ["number", "user"],
            "example": f"{base_url}/fm/recent?apikey=SUA_API_KEY&number=5511999999999",
        },
    }
    
    # Coleta todas as rotas do Flask
    for rule in app.url_map.iter_rules():
        if rule.endpoint in route_details:
            route_info = route_details[rule.endpoint].copy()
            route_info["endpoint"] = rule.endpoint
            routes_info.append(route_info)
        elif not rule.endpoint.startswith("static") and rule.endpoint != "docs.api_docs":
            # Rotas não documentadas manualmente
            methods = list(rule.methods - {"HEAD", "OPTIONS"})
            routes_info.append({
                "endpoint": rule.endpoint,
                "path": rule.rule,
                "method": methods[0] if methods else "GET",
                "description": "Rota não documentada",
                "required_params": [],
                "optional_params": [],
                "example": f"{base_url}{rule.rule}",
            })
    
    return jsonify({
        "base_url": base_url,
        "total_routes": len(routes_info),
        "routes": sorted(routes_info, key=lambda x: x["path"]),
    }), 200


@docs_bp.get("/docs/simple")
def api_docs_simple() -> tuple[Any, int]:
    """Lista simples de todas as rotas com exemplos de URL."""
    app = current_app
    base_url = request.host_url.rstrip("/")
    
    routes_list = []
    
    for rule in app.url_map.iter_rules():
        if rule.endpoint.startswith("static") or rule.endpoint == "docs.api_docs" or rule.endpoint == "docs.api_docs_simple":
            continue
            
        methods = list(rule.methods - {"HEAD", "OPTIONS"})
        method = methods[0] if methods else "GET"
        
        # Constrói exemplo de URL
        example_url = f"{base_url}{rule.rule}"
        
        # Adiciona parâmetros comuns se necessário
        if "apikey" in rule.rule or any("apikey" in str(param) for param in rule.arguments):
            example_url += "?apikey=SUA_API_KEY"
            if "input" in rule.rule or any("input" in str(param) for param in rule.arguments):
                example_url += "&input=exemplo"
            if "number" in rule.rule or any("number" in str(param) for param in rule.arguments):
                example_url += "&number=5511999999999"
            if "user" in rule.rule or any("user" in str(param) for param in rule.arguments):
                example_url += "&user=nomeusuario"
        
        routes_list.append({
            "method": method,
            "path": rule.rule,
            "example": example_url,
        })
    
    return jsonify({
        "base_url": base_url,
        "routes": sorted(routes_list, key=lambda x: x["path"]),
    }), 200
