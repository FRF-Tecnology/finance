"""Saúde das conexões: status do item e validade do consentimento Open Finance."""
from __future__ import annotations

from datetime import datetime, timezone

from financas.config import cliente, item_ids

AVISAR_CONSENTIMENTO_DIAS = 30
AVISAR_SEM_SYNC_DIAS = 3
STATUS_OK = {"UPDATED", "UPDATING"}


def _data(iso: str | None) -> datetime | None:
    if not iso:
        return None
    return datetime.fromisoformat(iso.replace("Z", "+00:00"))


def alertas_item(item: dict, agora: datetime | None = None) -> list[str]:
    agora = agora or datetime.now(timezone.utc)
    alertas = []
    status = item.get("status")
    if status not in STATUS_OK:
        alertas.append(f"conexão com status {status}: reconecte no Meu Pluggy "
                       "(meu.pluggy.ai) e confira o consentimento do Itaú")
    expira = _data(item.get("consentExpiresAt"))
    if expira:
        dias = (expira - agora).days
        if dias < 0:
            alertas.append(f"consentimento Open Finance EXPIROU em {expira:%d/%m/%Y}: renove no Meu Pluggy")
        elif dias <= AVISAR_CONSENTIMENTO_DIAS:
            alertas.append(f"consentimento Open Finance expira em {dias} dias ({expira:%d/%m/%Y}): renove no Meu Pluggy")
    sync = _data(item.get("lastUpdatedAt"))
    if sync and (agora - sync).days >= AVISAR_SEM_SYNC_DIAS:
        alertas.append(f"sem sincronizar desde {sync:%d/%m/%Y}: os dados podem estar desatualizados")
    return alertas


def verificar() -> list[tuple[str, dict, list[str]]]:
    """[(item_id, item, alertas)] para cada conexão configurada."""
    saida = []
    for item_id in item_ids():
        item = cliente().item(item_id)
        saida.append((item_id, item, alertas_item(item)))
    return saida
