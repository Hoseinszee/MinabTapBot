import os
import asyncio
from pytoniq_core import Address, begin_cell
from tonutils.client import ToncenterV3Client
from tonutils.jetton import JettonMasterStandard, JettonWalletStandard
from tonutils.wallet import WalletV4R2

MNEMONIC = os.environ["MNEMONIC"].split()
JETTON_MASTER_ADDRESS = "EQDQfl5nyYjuh8hXVvzIxgvgsMKsCe6uUld3TjBnZ1-xWVRj"
JETTON_DECIMALS = 9

async def send_zkr(destination_address: str, amount_tokens: float, comment: str = "ZKR reward"):
    client = ToncenterV3Client(is_testnet=False, rps=1, max_retries=3)
    wallet, _, _, _ = WalletV4R2.from_mnemonic(client, MNEMONIC)
    jetton_wallet_address = await JettonMasterStandard.get_wallet_address(
        client=client,
        owner_address=wallet.address.to_str(),
        jetton_master_address=JETTON_MASTER_ADDRESS,
    )
    body = JettonWalletStandard.build_transfer_body(
        recipient_address=Address(destination_address),
        response_address=wallet.address,
        jetton_amount=int(amount_tokens * (10 ** JETTON_DECIMALS)),
        forward_payload=begin_cell().store_uint(0, 32).store_snake_string(comment).end_cell(),
    )
    tx_hash = await wallet.transfer(destination=jetton_wallet_address, amount=0.05, body=body)
    return tx_hash

def send_zkr_sync(destination_address: str, amount_tokens: float, comment: str = "ZKR reward"):
    return asyncio.run(send_zkr(destination_address, amount_tokens, comment))
