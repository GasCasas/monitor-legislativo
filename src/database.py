"""
Módulo de persistência de dados.

Usa Supabase quando as credenciais estiverem configuradas
(via .streamlit/secrets.toml ou variáveis de ambiente).
Faz fallback transparente para arquivos JSON locais.
"""

import json
import os


def _credenciais():
    url = key = ""
    try:
        import streamlit as st
        url = st.secrets.get("SUPABASE_URL", "")
        key = st.secrets.get("SUPABASE_KEY", "")
    except Exception:
        pass
    if not url:
        url = os.getenv("SUPABASE_URL", "")
    if not key:
        key = os.getenv("SUPABASE_KEY", "")
    return url, key


_cliente_cache = None

def _cliente():
    global _cliente_cache
    if _cliente_cache is not None:
        return _cliente_cache
    url, key = _credenciais()
    if url and key:
        try:
            from supabase import create_client
            _cliente_cache = create_client(url, key)
        except Exception as e:
            print(f"[Database] Supabase indisponível: {e}. Usando JSON local.")
    return _cliente_cache


def usando_supabase() -> bool:
    return _cliente() is not None


_ARQUIVO_MON = "data/monitorados.json"

def carregar_monitorados() -> dict:
    sb = _cliente()
    if sb:
        try:
            res = sb.table("monitorados").select("chave, dados").execute()
            return {row["chave"]: row["dados"] for row in (res.data or [])}
        except Exception as e:
            print(f"[Database] Erro ao carregar monitorados: {e}")
    if not os.path.exists(_ARQUIVO_MON):
        return {}
    with open(_ARQUIVO_MON, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_monitorados(monitorados: dict):
    sb = _cliente()
    if sb:
        try:
            res = sb.table("monitorados").select("chave").execute()
            chaves_atuais = {row["chave"] for row in (res.data or [])}
            for chave, dados in monitorados.items():
                sb.table("monitorados").upsert({"chave": chave, "dados": dados}).execute()
            for chave in chaves_atuais - set(monitorados.keys()):
                sb.table("monitorados").delete().eq("chave", chave).execute()
            return
        except Exception as e:
            print(f"[Database] Erro ao salvar monitorados: {e}")
    os.makedirs("data", exist_ok=True)
    with open(_ARQUIVO_MON, "w", encoding="utf-8") as f:
        json.dump(monitorados, f, ensure_ascii=False, indent=2)


_ARQUIVO_HIST = "data/historico.json"

def carregar_historico() -> list:
    sb = _cliente()
    if sb:
        try:
            res = (
                sb.table("historico")
                .select("data, casa, proposicao, mensagem")
                .order("id", desc=True)
                .limit(500)
                .execute()
            )
            return list(reversed(res.data or []))
        except Exception as e:
            print(f"[Database] Erro ao carregar histórico: {e}")
    if not os.path.exists(_ARQUIVO_HIST):
        return []
    with open(_ARQUIVO_HIST, "r", encoding="utf-8") as f:
        return json.load(f)


def registrar_mudancas(atualizacoes: list):
    if not atualizacoes:
        return
    from datetime import datetime
    agora = datetime.now().strftime("%Y-%m-%d %H:%M")
    sb = _cliente()
    if sb:
        try:
            rows = []
            for upd in atualizacoes:
                casa, numero, ano = upd["chave"].split(":")
                rows.append({
                    "data": agora,
                    "casa": casa,
                    "proposicao": f"{upd.get('tipo', '')} {numero}/{ano}".strip(),
                    "mensagem": upd["mensagem"],
                })
            sb.table("historico").insert(rows).execute()
            res = sb.table("historico").select("id").order("id", desc=True).limit(501).execute()
            ids = [r["id"] for r in (res.data or [])]
            if len(ids) > 500:
                sb.table("historico").delete().eq("id", ids[-1]).execute()
            return
        except Exception as e:
            print(f"[Database] Erro ao registrar mudanças: {e}")
    historico = carregar_historico()
    for upd in atualizacoes:
        casa, numero, ano = upd["chave"].split(":")
        historico.append({
            "data": agora,
            "casa": casa,
            "proposicao": f"{upd.get('tipo', '')} {numero}/{ano}".strip(),
            "mensagem": upd["mensagem"],
        })
    _salvar_historico_json(historico[-500:])


def limpar_historico():
    sb = _cliente()
    if sb:
        try:
            sb.table("historico").delete().neq("id", 0).execute()
            return
        except Exception as e:
            print(f"[Database] Erro ao limpar histórico: {e}")
    _salvar_historico_json([])


def _salvar_historico_json(historico: list):
    os.makedirs("data", exist_ok=True)
    with open(_ARQUIVO_HIST, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)


_ARQUIVO_CFG = "data/agendador.json"
_CONFIG_PADRAO = {
    "ativo": False, "intervalo_horas": 1,
    "email_destinatario": "", "email_remetente": "", "email_senha_app": "",
    "whatsapp_numero": "", "whatsapp_api_key": "",
    "notif_email": False, "notif_whatsapp": False, "ultima_verificacao": None,
}

def carregar_config() -> dict:
    sb = _cliente()
    if sb:
        try:
            res = sb.table("config").select("valor").eq("chave", "agendador").execute()
            if res.data:
                return res.data[0]["valor"]
        except Exception as e:
            print(f"[Database] Erro ao carregar config: {e}")
    if not os.path.exists(_ARQUIVO_CFG):
        return _CONFIG_PADRAO.copy()
    with open(_ARQUIVO_CFG, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_config(config: dict):
    sb = _cliente()
    if sb:
        try:
            sb.table("config").upsert({"chave": "agendador", "valor": config}).execute()
            return
        except Exception as e:
            print(f"[Database] Erro ao salvar config: {e}")
    os.makedirs("data", exist_ok=True)
    with open(_ARQUIVO_CFG, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
