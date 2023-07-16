import httpx
import base64
import argparse


def get_block_txs(height: int):
    # используем api lavender т.к. имеет минимальный lowest height
    response = httpx.get(f"https://akash-api.lavenderfive.com/blocks/{height}")
    data = response.json()

    if response.status_code != 200:
        raise Exception(data)

    # получаем список транзакций для блока
    transactions = data["block"]["data"]["txs"]
    # по документации Akash, данные сериализованы с помощью Amino
    # "... serialize it to the Amino wire protocol, and output it as base64 ..."
    # для десериализации и получения читаемых данных нужна схема .proto
    # нашёл что-то похожее тут: https://github.com/cosmos/cosmos-sdk/blob/main/proto/cosmos/tx/v1beta1/tx.proto
    # но довести дело до ума не получилось. Если можно было сделать проще, дайте обратную связь пожалуйста.
    decoded_txs = [base64.b64decode(transaction) for transaction in transactions]
    print(decoded_txs)
    return decoded_txs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="find txs for some block")
    parser.add_argument(dest='height', type=int, help="enter block id to find txs")
    args = parser.parse_args()
    get_block_txs(args.height)
