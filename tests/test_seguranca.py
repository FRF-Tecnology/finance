"""Garantias que não dependem de rede nem de credenciais."""
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from financas.conexoes import alertas_item

RAIZ = Path(__file__).resolve().parent.parent


def test_codigo_nao_faz_escrita_na_api():
    # Só leitura: nosso código usa apenas cliente.get/paginado/métodos de leitura.
    proibido = re.compile(r'"(POST|PUT|PATCH|DELETE)"|payment|transfer', re.I)
    for arq in (RAIZ / "financas").rglob("*.py"):
        assert not proibido.search(arq.read_text()), arq


def test_env_esta_no_gitignore():
    r = subprocess.run(["git", "check-ignore", "-q", ".env"], cwd=RAIZ)
    assert r.returncode == 0


def test_alerta_consentimento_perto_de_expirar():
    agora = datetime(2026, 11, 5, tzinfo=timezone.utc)
    item = {"status": "UPDATED", "consentExpiresAt": "2026-11-20T00:00:00Z",
            "lastUpdatedAt": "2026-11-05T00:00:00Z"}
    assert any("expira em 15 dias" in a for a in alertas_item(item, agora))


def test_alerta_conexao_caida():
    item = {"status": "LOGIN_ERROR", "lastUpdatedAt": "2026-11-05T00:00:00Z"}
    agora = datetime(2026, 11, 5, tzinfo=timezone.utc)
    assert any("LOGIN_ERROR" in a for a in alertas_item(item, agora))
