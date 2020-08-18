import mock
import pytest
from web3 import Web3

from skale.transactions.result import InsufficientBalanceError
from skale.utils.account_tools import generate_account
from skale.utils.web3_utils import wait_for_receipt_by_blocks


ETH_IN_WEI = 10 ** 18


def test_dry_run(skale):
    account = generate_account(skale.web3)
    address_to = account['address']
    address_from = Web3.toChecksumAddress(skale.wallet.address)
    address_to = Web3.toChecksumAddress(address_to)
    balance_from_before = skale.token.get_balance(address_from)
    balance_to_before = skale.token.get_balance(address_to)
    amount = 10 * ETH_IN_WEI
    tx_res = skale.token.transfer(address_to, amount, dry_run_only=True)
    assert tx_res.dry_run_result == {'payload': [], 'status': 1}
    tx_res.raise_for_status()

    balance_from_after = skale.token.get_balance(address_from)
    assert balance_from_after == balance_from_before
    balance_to_after = skale.token.get_balance(address_to)
    assert balance_to_after == balance_to_before


def test_skip_dry_run(skale):
    account = generate_account(skale.web3)
    address_to = account['address']
    address_from = Web3.toChecksumAddress(skale.wallet.address)
    address_to = Web3.toChecksumAddress(address_to)
    balance_from_before = skale.token.get_balance(address_from)
    balance_to_before = skale.token.get_balance(address_to)
    amount = 10 * ETH_IN_WEI

    tx_res = skale.token.transfer(address_to, amount, skip_dry_run=True)
    assert tx_res.tx_hash is not None, tx_res
    assert tx_res.receipt is not None
    assert tx_res.dry_run_result is None
    balance_from_after = skale.token.get_balance(address_from)
    assert balance_from_after == balance_from_before - amount
    balance_to_after = skale.token.get_balance(address_to)
    assert balance_to_after == balance_to_before + amount


def test_wait_for_false(skale):
    ETH_IN_WEI = 10 ** 18
    account = generate_account(skale.web3)
    address_to = account['address']
    address_from = Web3.toChecksumAddress(skale.wallet.address)
    address_to = Web3.toChecksumAddress(address_to)
    balance_from_before = skale.token.get_balance(address_from)
    balance_to_before = skale.token.get_balance(address_to)
    amount = 10 * ETH_IN_WEI

    tx_res = skale.token.transfer(address_to, amount, wait_for=False)
    assert tx_res.tx_hash is not None
    assert tx_res.receipt is None
    assert tx_res.dry_run_result == {'payload': [], 'status': 1}

    tx_res.receipt = wait_for_receipt_by_blocks(skale.web3, tx_res.tx_hash)
    tx_res.raise_for_status()

    balance_from_after = skale.token.get_balance(address_from)
    assert balance_from_after == balance_from_before - amount
    balance_to_after = skale.token.get_balance(address_to)
    assert balance_to_after == balance_to_before + amount


def test_tx_res_dry_run(skale):
    account = generate_account(skale.web3)
    token_amount = 10
    tx_res = skale.token.transfer(
        account['address'], token_amount, dry_run_only=True)
    assert tx_res.dry_run_result is not None
    assert tx_res.tx_hash is None
    assert tx_res.receipt is None
    tx_res.raise_for_status()


def test_tx_res_wait_for_false(skale):
    account = generate_account(skale.web3)
    token_amount = 10
    tx_res = skale.token.transfer(
        account['address'], token_amount, wait_for=False)
    assert tx_res.tx_hash is not None
    assert tx_res.receipt is None
    tx_res.raise_for_status()

    tx_res.receipt = wait_for_receipt_by_blocks(skale.web3, tx_res.tx_hash)
    tx_res.raise_for_status()


def test_tx_res_wait_for_true(skale):
    account = generate_account(skale.web3)
    token_amount = 10
    tx_res = skale.token.transfer(account['address'], token_amount)
    assert tx_res.tx_hash is not None
    assert tx_res.receipt is not None
    tx_res.raise_for_status()


@mock.patch('skale.common_contracts.base_contract.account_eth_balance_wei',
            new=mock.Mock(return_value=0))
def test_tx_res_with_insufficient_funds(skale):
    account = generate_account(skale.web3)
    token_amount = 10
    with pytest.raises(InsufficientBalanceError):
        skale.token.transfer(account['address'], token_amount)


def test_confirmation_blocks(skale):
    account = generate_account(skale.web3)
    token_amount = 10
    confirmation_blocks = 0  # todo: enable mining on ganache
    start_block = skale.web3.eth.blockNumber
    skale.token.transfer(account['address'], token_amount, confirmation_blocks=confirmation_blocks)
    assert skale.web3.eth.blockNumber >= start_block + confirmation_blocks
