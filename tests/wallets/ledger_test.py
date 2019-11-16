import mock

from skale.utils.web3_utils import init_web3
from skale.wallets.ledger_wallet import LedgerWallet

from tests.constants import ENDPOINT


def get_dongle_mock(debug):
    class DongleMock:
        def __init__(debug):
            pass

        def exchange(self, apdu):
            if apdu.startswith(b'\xe0\x02'):
                return bytearray(b'A\x042\x11\ta\xe4s\x80\x8f-\x15\xce\x80\xff\x81\xea\xf5\xcb\xbc\xea\xe2W\xe7\xa8\xe0\xbe\xcf\x8aMMO\x99\xae\x13k\xb6Lj\x9fv\x1d\xea\xe49N \xe5\xa34\xf3A\xa0\xa26\x07\xb7=\x0b\xcd\xeb4\xd4\xf4\x83\xdc(47be82C32BF112f7bEa3f225a2a97091ca133FA2')  # noqa
            else:
                return bytearray(b'\x1c\xad\xf1\xcdp<\xa9\xde\xd1\x06p$46h\xbd_\xb1\x90\x06,\x8a:\xa8yL\xac\xba$g\xbc;\xd8x\xee5M\x13\xb1\xdd\xad\x8e\xb2yS\xabh\xea\x81\xe8\xe2\xc9\x8c!\x98v\x93\x80\xd3\xe5\xc7\x8dJB0')  # noqa

    return DongleMock()


def test_hardware_sign_and_send():
    with mock.patch('skale.wallets.ledger_wallet.getDongle',
                    new=get_dongle_mock):
        web3 = init_web3(ENDPOINT)
        wallet = LedgerWallet(web3)
        tx_dict = {
            'to': '0x1057dc7277a319927D3eB43e05680B75a00eb5f4',
            'value': 9,
            'gas': 200000,
            'gasPrice': 1,
            'nonce': 7,
            'chainId': None,
            'data': b'\x9b\xd9\xbb\xc6\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x95qY\xc4i\xfc;\xba\xa8\xe3\x9e\xe0\xa3$\xc28\x8a\xd6Q\xe5\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\r\xe0\xb6\xb3\xa7d\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00`\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x006\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa8\xc0\x04/Rglamorous-kitalpha\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  # noqa
        }
        wallet.sign(tx_dict)
