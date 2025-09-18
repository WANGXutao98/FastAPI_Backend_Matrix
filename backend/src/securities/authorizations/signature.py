import base64
import hmac
import secrets
import time
from typing import Callable


def generate_aksk():
    ak = secrets.token_hex(16)
    sk = base64.b64encode(secrets.token_bytes(32)).decode("utf-8")
    return ak, sk


def _hash_hmac(key: str, message: str) -> str:
    return hmac.new(key.encode(), message.encode(), "sha1").hexdigest().upper()


def generate_signature(access_key: str, secret_key: str, nonce: str, timestamp: str) -> str:
    message = f"{timestamp}{access_key}{nonce}{timestamp}"
    return _hash_hmac(secret_key, message)


def verify(access_key: str, nonce: str, timestamp: str, input_signature: str) -> bool:
    """
    校验摘要

    :param security_key: 身份标识，根据这个标识服务端找到对应的私钥
    :param nonce: 唯一请求标识，根据这个标识可以防止重复请求攻击
    :param timestamp: 可以用来做超时判断
    :param input_signature: 要校验的传入参数
    :return: 通过返回true 不通过返回 false
    """
    # 验证时间戳，以防止重放攻击
    current_timestamp = int(time.time())
    request_timestamp = int(timestamp)
    if abs(current_timestamp - request_timestamp) > 300:  # 允许的最大时间差（秒）
        return False

    message = f"{timestamp}{access_key}{nonce}{timestamp}"
    sig = _hash_hmac(access_key, message)
    return hmac.compare_digest(sig, input_signature)
