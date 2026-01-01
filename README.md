# 🐈 Floppa API - O Cérebro do Bot

Este projeto é o backend oficial desenvolvido para o **Floppa**, um bot de WhatsApp.

A API serve como uma camada de inteligência e processamento de dados, permitindo que o bot (o "corpo", provavelmente feito em Node/Baileys) seja leve e apenas repasse comandos, enquanto este serviço Python cuida da lógica pesada, integrações com terceiros e manutenção de estado.

## 🎯 Objetivo do Projeto

O objetivo principal é centralizar funcionalidades complexas que seriam difíceis ou desorganizadas de manter diretamente no código do bot de WhatsApp. Ele atua como um *middleware* entre o usuário do WhatsApp e serviços como Last.fm, Character.AI e APIs de jogos.

### Como funciona a integração?

1. **O Usuário** manda uma mensagem no WhatsApp (ex: `!musica`).
2. **O Bot** captura o ID do usuário (ex: `551199999@s.whatsapp.net`).
3. **O Bot** faz uma requisição para esta API:
   `GET /fm/recent?number=551199999&apikey=...`
4. **Esta API**:
   - Identifica o usuário no banco de dados local (`DATABASE_FM.json`).
   - Consulta a API do Last.fm.
   - Formata os dados e retorna um JSON limpo.
5. **O Bot** recebe o JSON e envia a resposta formatada no chat.

---

## 🚀 Funcionalidades (Contexto do Bot)

### 🤖 IA & Chat (A "Alma" do Floppa)
- **Conversa Natural (`/ai/floppa`):** Rota que conecta o WhatsApp diretamente ao **Character.AI**. Isso dá ao bot sua personalidade única, permitindo que os usuários conversem com o "Floppa" em tempo real.
- **Consultas Gerais (`/ai/gpt4`):** Para quando os usuários pedem resumos ou ajuda com textos, utilizando GPT-4 via provedores livres (`g4f`).

### 🎵 Sistema de Música (Last.fm)
O diferencial aqui é o mapeamento **Número de WhatsApp ↔ Usuário Last.fm**.
- **Registro Automático:** O comando de registro salva o vínculo entre o número do "Zap" e a conta do Last.fm.
- **Privacidade:** O bot só precisa enviar o número de telefone (JID) de quem enviou a mensagem; a API resolve quem é o usuário.
- **Comandos Suportados:** Música atual, top álbuns/artistas e playcount.

### 🎮 Utilitários para Grupos
- **Jogos Grátis:** A API verifica periodicamente e filtra jogos grátis, gerando thumbnails via ImgBB para que o bot possa enviar a imagem do jogo junto com o link no grupo.
- **Downloader de Mídia:** Permite que usuários enviem links (Instagram, TikTok, YouTube) e o bot receba o link direto do arquivo de vídeo para enviar nativamente no chat.

---
