"""Credenciais e cliente da Pluggy.

As credenciais vêm de variáveis de ambiente ou do arquivo .env na raiz do
projeto (que está no .gitignore). Variáveis já definidas no ambiente têm
prioridade sobre o .env.
"""
from __future__ import annotations

import os
from functools import cache
from pathlib import Path

from pluggy_mcp.cliente import ClientePluggy

RAIZ = Path(__file__).resolve().parent.parent
ARQUIVO_ENV = RAIZ / ".env"
OBRIGATORIAS = ("PLUGGY_CLIENT_ID", "PLUGGY_CLIENT_SECRET", "PLUGGY_ITEM_IDS")


def carregar_env(arquivo: Path = ARQUIVO_ENV) -> None:
    """Lê linhas CHAVE=valor do .env sem sobrescrever o que já está no ambiente."""
    if not arquivo.exists():
        return
    for linha in arquivo.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        chave, valor = linha.split("=", 1)
        valor = valor.strip()
        if len(valor) >= 2 and valor[0] == valor[-1] and valor[0] in "'\"":
            valor = valor[1:-1]
        os.environ.setdefault(chave.strip(), valor)


def verificar_credenciais() -> None:
    carregar_env()
    faltando = [v for v in OBRIGATORIAS if not os.environ.get(v, "").strip()]
    if faltando:
        raise SystemExit(
            "Faltam variáveis: " + ", ".join(faltando)
            + f"\nPreencha em {ARQUIVO_ENV} (copie de .env.example). Veja o README.")


@cache
def cliente() -> ClientePluggy:
    verificar_credenciais()
    return ClientePluggy(os.environ["PLUGGY_CLIENT_ID"], os.environ["PLUGGY_CLIENT_SECRET"])


def item_ids() -> list[str]:
    verificar_credenciais()
    return [i.strip() for i in os.environ["PLUGGY_ITEM_IDS"].split(",") if i.strip()]
