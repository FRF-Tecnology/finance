"""Sobe o MCP somente leitura do Meu Pluggy com as credenciais do .env."""
from financas.config import carregar_env


def main() -> None:
    carregar_env()
    from pluggy_mcp.servidor import main as rodar  # importa depois de carregar o .env
    rodar()


if __name__ == "__main__":
    main()
