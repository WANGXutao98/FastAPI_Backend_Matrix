import fcntl
import socket
import struct
import sys

from fastapi import Request


class IpAddress:
    @staticmethod
    def get_client_ip(request: Request) -> str:
        """get client ip address by request headers

        Args:
            request (_type_): _description_
        """
        try:
            real_ip = request.headers["X-Forwarded-For"]
            if len(real_ip.split(",")) > 1:
                client_ip = real_ip.split(",")[0]

            else:
                client_ip = real_ip

        except Exception:  # pylint: disable=broad-except
            client_ip = request.client.host  # type:ignore

        return client_ip

    @staticmethod
    def get_host_ip() -> str:
        """get the host ip address by socket"""
        host_ip = None
        try:
            socket_fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            socket_fd.connect(("www.qq.com", 80))
            host_ip = socket_fd.getsockname()[0]

        finally:
            socket_fd.close()

        if host_ip:
            return host_ip

        try:
            host_ip = IpAddress.get_ip_by_interface("eth1")

        except OSError:
            try:
                host_ip = IpAddress.get_ip_by_interface("eth0")

            except OSError:
                host_ip = None

        return host_ip

    @staticmethod
    def get_ip_by_interface(ifname: str) -> str:
        """获取指定网卡的IP地址"""
        ifname = ifname[:15]
        if sys.version_info.major == 3:
            ifname = bytes(ifname, "utf-8")  # type:ignore

        socket_fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip_addr = socket.inet_ntoa(
            fcntl.ioctl(socket_fd.fileno(), 0x8915, struct.pack("256s", ifname))[20:24]  # SIOCGIFADDR
        )
        return ip_addr
