""" Tests for contracts/delegation/validator_service.py """

import pytest

from skale.contracts.delegation.validator_service import FIELDS
from skale.wallets.web3_wallet import generate_wallet
from skale.utils.web3_utils import check_receipt
from skale.utils.account_tools import send_ether

from tests.constants import (
    NOT_EXISTING_ID, D_VALIDATOR_ID, D_VALIDATOR_NAME, D_VALIDATOR_DESC,
    D_VALIDATOR_FEE, D_VALIDATOR_MIN_DEL
)


def test_get_raw_not_exist(skale):
    empty_struct = skale.validator_service._ValidatorService__get_raw(NOT_EXISTING_ID)
    assert empty_struct[0] == ''
    assert empty_struct[1] == '0x0000000000000000000000000000000000000000'


def test_get(skale):
    validator = skale.validator_service.get(D_VALIDATOR_ID)
    assert list(validator.keys()) == FIELDS
    assert [k for k, v in validator.items() if v is None] == []


def test_get_with_id(skale):
    validator = skale.validator_service.get_with_id(D_VALIDATOR_ID)
    assert validator['id'] == D_VALIDATOR_ID


def test_number_of_validators(skale):
    n_of_validators_before = skale.validator_service.number_of_validators()
    _generate_new_validator(skale)
    n_of_validators_after = skale.validator_service.number_of_validators()
    assert n_of_validators_after == n_of_validators_before + 1


def test_ls(skale):
    n_of_validators = skale.validator_service.number_of_validators()
    validators = skale.validator_service.ls()
    assert all([validator['name'] == D_VALIDATOR_NAME for validator in validators])
    assert n_of_validators == len(validators)
    trusted_validators = skale.validator_service.ls(trusted_only=True)
    assert trusted_validators == [v for v in validators if v['trusted']]


def test_get_linked_addresses_by_validator_address(skale):
    addresses = skale.validator_service.get_linked_addresses_by_validator_address(
        address=skale.wallet.address
    )
    assert skale.wallet.address in addresses

    wallet = generate_wallet(skale.web3)
    tx_res = skale.validator_service.link_node_address(
        node_address=wallet.address,
        wait_for=True
    )
    check_receipt(tx_res.receipt)

    assert wallet.address not in addresses
    addresses = skale.validator_service.get_linked_addresses_by_validator_address(
        address=skale.wallet.address
    )
    assert wallet.address in addresses


def test_get_linked_addresses_by_validator_id(skale):
    addresses = skale.validator_service.get_linked_addresses_by_validator_address(
        address=skale.wallet.address
    )
    assert skale.wallet.address in addresses


def test_is_main_address(skale):
    is_main_address = skale.validator_service.is_main_address(skale.wallet.address)
    assert is_main_address

    wallet = generate_wallet(skale.web3)
    tx_res = skale.validator_service.link_node_address(
        node_address=wallet.address,
        wait_for=True
    )
    check_receipt(tx_res.receipt)

    is_main_address = skale.validator_service.is_main_address(wallet.address)
    assert not is_main_address


def test_validator_address_exists(skale):
    address_exists = skale.validator_service.validator_address_exists(skale.wallet.address)
    assert address_exists

    wallet = generate_wallet(skale.web3)
    address_exists = skale.validator_service.validator_address_exists(wallet.address)
    assert not address_exists


def test_validator_id_by_address(skale):
    validator_id = skale.validator_service.validator_id_by_address(skale.wallet.address)
    assert validator_id == D_VALIDATOR_ID


def test_get_validator_node_indices(skale):  # todo: improve test
    node_indices = skale.validator_service.get_validator_node_indices(
        validator_id=D_VALIDATOR_ID
    )
    assert isinstance(node_indices, list)


def test_enable_validator(skale):
    _generate_new_validator(skale)
    latest_id = skale.validator_service.number_of_validators()

    is_validator_trusted = skale.validator_service._is_validator_trusted(latest_id)
    assert not is_validator_trusted

    tx_res = skale.validator_service._enable_validator(
        validator_id=latest_id,
        wait_for=True
    )
    check_receipt(tx_res.receipt)

    is_validator_trusted = skale.validator_service._is_validator_trusted(latest_id)
    assert is_validator_trusted


def test_disable_validator(skale):
    _generate_new_validator(skale)
    latest_id = skale.validator_service.number_of_validators()

    is_validator_trusted = skale.validator_service._is_validator_trusted(latest_id)
    assert not is_validator_trusted

    tx_res = skale.validator_service._enable_validator(
        validator_id=latest_id,
        wait_for=True
    )
    check_receipt(tx_res.receipt)

    is_validator_trusted = skale.validator_service._is_validator_trusted(latest_id)
    assert is_validator_trusted

    tx_res = skale.validator_service._disable_validator(
        validator_id=latest_id,
        wait_for=True
    )
    is_validator_trusted = skale.validator_service._is_validator_trusted(latest_id)
    assert not is_validator_trusted


def test_is_validator_trusted(skale):
    is_validator_trusted = skale.validator_service._is_validator_trusted(D_VALIDATOR_ID)
    assert is_validator_trusted


def test_register_existing_validator(skale):
    with pytest.raises(ValueError):
        skale.validator_service.register_validator(
            name=D_VALIDATOR_NAME,
            description=D_VALIDATOR_DESC,
            fee_rate=D_VALIDATOR_FEE,
            min_delegation_amount=D_VALIDATOR_MIN_DEL,
            wait_for=True
        )


def _generate_new_validator(skale):
    eth_amount = 0.1
    main_wallet = skale.wallet
    wallet = generate_wallet(skale.web3)
    send_ether(skale.web3, skale.wallet, wallet.address, eth_amount)
    skale.wallet = wallet
    tx_res = skale.validator_service.register_validator(
        name=D_VALIDATOR_NAME,
        description=D_VALIDATOR_DESC,
        fee_rate=D_VALIDATOR_FEE,
        min_delegation_amount=D_VALIDATOR_MIN_DEL,
        wait_for=True
    )
    check_receipt(tx_res.receipt)
    skale.wallet = main_wallet


def test_register_new_validator(skale):
    n_of_validators_before = skale.validator_service.number_of_validators()
    _generate_new_validator(skale)
    n_of_validators_after = skale.validator_service.number_of_validators()
    assert n_of_validators_after == n_of_validators_before + 1


def test_link_node_address(skale):
    wallet = generate_wallet(skale.web3)
    addresses = skale.validator_service.get_linked_addresses_by_validator_address(
        skale.wallet.address
    )
    assert wallet.address not in addresses

    tx_res = skale.validator_service.link_node_address(
        node_address=wallet.address,
        wait_for=True
    )
    check_receipt(tx_res.receipt)

    addresses = skale.validator_service.get_linked_addresses_by_validator_address(
        skale.wallet.address
    )
    assert wallet.address in addresses


def test_unlink_node_address(skale):
    wallet = generate_wallet(skale.web3)
    tx_res = skale.validator_service.link_node_address(
        node_address=wallet.address,
        wait_for=True
    )
    check_receipt(tx_res.receipt)

    addresses = skale.validator_service.get_linked_addresses_by_validator_address(
        skale.wallet.address
    )
    assert wallet.address in addresses

    tx_res = skale.validator_service.unlink_node_address(
        node_address=wallet.address,
        wait_for=True
    )
    check_receipt(tx_res.receipt)
    addresses = skale.validator_service.get_linked_addresses_by_validator_address(
        skale.wallet.address
    )
    assert wallet.address not in addresses
