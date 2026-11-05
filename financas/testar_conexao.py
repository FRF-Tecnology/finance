"""Teste da Etapa 1: lista conexões, contas e as últimas 10 transações."""
from __future__ import annotations

from datetime import date, timedelta

from financas import conexoes
from financas.config import cliente, item_ids


def brl(v: float | None) -> str:
    if v is None:
        return "-"
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def main() -> None:
    print("== Conexões")
    for item_id, item, alertas in conexoes.verificar():
        print(f"  {item_id[:8]}…  status={item.get('status')}  "
              f"atualizado={str(item.get('lastUpdatedAt'))[:10]}  "
              f"consentimento até={str(item.get('consentExpiresAt'))[:10]}")
        for a in alertas:
            print(f"  ⚠️  {a}")

    contas = [c for i in item_ids() for c in cliente().contas(i)]
    print("\n== Contas")
    for c in contas:
        print(f"  {c.get('type'):7} {c.get('subtype') or '':22} {c.get('name') or '':30} saldo {brl(c.get('balance'))}")

    desde = (date.today() - timedelta(days=45)).isoformat()
    txs = []
    for c in contas:
        for tx in cliente().transacoes(c["id"], desde):
            txs.append((tx.get("date", "")[:10], c.get("type"), tx))
    txs.sort(key=lambda t: t[0], reverse=True)
    print("\n== Últimas 10 transações")
    for dia, tipo_conta, tx in txs[:10]:
        print(f"  {dia}  {tipo_conta:6} {tx.get('type'):6} {brl(tx.get('amount')):>14}  {tx.get('description')}")
    if not txs:
        print("  nenhuma transação nos últimos 45 dias")


if __name__ == "__main__":
    main()
