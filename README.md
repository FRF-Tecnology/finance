# Finanças pessoais — Itaú via Meu Pluggy (Open Finance)

Sistema pessoal, **somente leitura**, de controle de gastos e investimentos.
Os dados vêm do Itaú pelo Meu Pluggy e ficam só na sua máquina (pasta `dados/`,
fora do git).

## MCP escolhido

[`Moreti2002/open-finance-plugin-mcp`](https://github.com/Moreti2002/open-finance-plugin-mcp),
fixado no commit `e201190` (veja `pyproject.toml`).

- Feito para o Meu Pluggy e tem o que precisamos: contas, transações, faturas e investimentos.
- É somente leitura: a única chamada que não é GET é o `POST /auth`, e não há PIX, pagamento nem transferência.
- O código é pequeno (cerca de 300 linhas) e foi lido antes de ser fixado.

Por que não os outros:
- O MCP oficial (`pluggyai/pluggy-mcp`) só tem `getAccounts` e `listConnectors`: faltam transações, faturas e investimentos.
- Os forks do `codespar/mcp-pluggy` têm `create_payment_intent`, `delete_item` e `update_item`, o que quebra a regra de somente leitura.

## Pré-requisitos

- [uv](https://docs.astral.sh/uv/) e Python 3.12 ou mais novo.
- Claude Code rodando **nesta pasta** (`cd finance && claude`).

```bash
uv sync                 # instala as dependências
cp .env.example .env    # depois preencha o .env num editor (não no chat)
uv run testar-conexao   # lista conexões, contas e as últimas 10 transações
```

O `.mcp.json` registra o servidor `pluggy` para o Claude Code deste projeto. Ele
roda `financas.mcp_server`, que lê o `.env` e sobe o MCP. Confira com `/mcp`
dentro do Claude Code.

## Credenciais (onde pegar cada valor)

Os nomes dos menus podem mudar um pouco no painel.

1. **Meu Pluggy** ([meu.pluggy.ai](https://meu.pluggy.ai)): crie a conta e conecte o
   **Itaú** pelo fluxo de consentimento do Open Finance. Marque conta, cartão e
   investimentos.
2. **Pluggy Dashboard** ([dashboard.pluggy.ai](https://dashboard.pluggy.ai)): crie
   uma conta de desenvolvedor. Ela começa com um teste de 15 dias, então faça os
   passos 3 a 5 dentro desse prazo.
3. Em **Aplicações**, crie uma aplicação de desenvolvimento. Na página dela ficam:
   - **Client ID** → `PLUGGY_CLIENT_ID`
   - **Client Secret** → `PLUGGY_CLIENT_SECRET`
4. Na aplicação, em **Conectores**, habilite o conector **MeuPluggy**.
5. Clique em **Ir para Demo** → **Conectar conta** → **MeuPluggy**, entre com a sua
   conta do Meu Pluggy e autorize o Itaú. Na conexão criada, abra o menu de três
   pontos e use **Copiar Item ID**. Esse é o valor de `PLUGGY_ITEM_IDS`; se houver
   mais de um banco, separe os IDs por vírgula.
   - Use o conector **MeuPluggy**, não o conector direto do Itaú e não o Sandbox.
   - A API não lista os itens, por isso o ID precisa ser copiado à mão.

Os valores vão **só** no `.env`, que está no `.gitignore`. Também podem vir de
variáveis de ambiente, que têm prioridade sobre o `.env`. O
`.claude/settings.json` impede o Claude de ler o `.env`.

## Consentimento e conexões

O consentimento do Open Finance expira (normalmente em 12 meses). O
`testar-conexao`, e mais tarde o `relatorio`, avisam quando:
- a conexão não está `UPDATED` (por exemplo, `LOGIN_ERROR` ou `OUTDATED`);
- o consentimento expira em 30 dias ou menos, ou já expirou;
- a última sincronização foi há 3 dias ou mais.

Para renovar, reconecte o Itaú no Meu Pluggy.

## Regras

- Somente leitura: nada de pagamentos, transferências ou alterações no banco.
  O teste `tests/test_seguranca.py` falha se o código ganhar alguma chamada de escrita.
- Os dados financeiros não saem da máquina, exceto as chamadas à própria Pluggy.
