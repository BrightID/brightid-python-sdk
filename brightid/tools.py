import json
import base64
import pyqrcode
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


def create_deep_link(app, app_user_id):
    url = "http://node.brightid.org".replace('/', '%2f')
    deep_link = f'brightid://link-verification/{url}/{app}/{app_user_id}'
    return deep_link


def create_qr(deep_link, scale=8):
    qr = pyqrcode.create(deep_link)
    return qr.png_as_base64_str(scale=scale)


def sign(op, private):
    signing_key = Ed25519PrivateKey.from_private_bytes(base64.b64decode(private))
    message = json.dumps(op, sort_keys=True,
                         separators=(',', ':')).encode('ascii')
    sig = signing_key.sign(message)
    sig = base64.b64encode(sig).decode('ascii')
    return sig


def create_bright_id():
    private = Ed25519PrivateKey.generate()
    public = private.public_key()
    private = base64.b64encode(private.private_bytes_raw()).decode('ascii')
    public = base64.b64encode(public.public_bytes_raw()).decode('ascii')
    id = public.strip('=').replace('/', '_').replace('+', '-')
    return {
        'id': id,
        'private': private,
        'public': public
    }
