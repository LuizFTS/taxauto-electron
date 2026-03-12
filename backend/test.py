import asyncio

import httpx
import pandas as pd

API_URL = "http://127.0.0.1:8001/api/v1/branches/"

EXCEL_FILE = "branches.csv"


async def create_branch(client: httpx.AsyncClient, payload: dict):
    API_URL = f"http://127.0.0.1:8001/api/v1/branch-group/4/branches/{payload['branch_id']}"

    response = await client.post(API_URL, json=payload)

    if response.status_code not in (200, 201, 204):
        print(f"Erro ao adicionar filial: {response.text}")
    else:
        print(f"Filial criada {payload['nome']}")


async def main():
    df = pd.read_csv(EXCEL_FILE)

    empresas = [1, 3, 13, 14, 15, 25, 26, 30, 31, 33, 53, 55, 57, 58, 59, 60, 61, 72, 80]

    async with httpx.AsyncClient(timeout=30.0) as client:
        for _, row in df.iterrows():

            if int(row["codigo"]) in empresas:
                payload = {
                    "branch_id": int(row["id"]),
                    "codigo": row["codigo"],
                    "nome": row["nome"],
                }
                # print(payload)

                await create_branch(client, payload)


if __name__ == "__main__":
    asyncio.run(main())
