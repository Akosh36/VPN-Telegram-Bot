import json
import base64
import uuid
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

class VPNLinkGenerator:
    def generate_vpn_link(
        self, link_type: str, server_address: str, port: int, security: str = "auto", network: str = "tcp", **kwargs: Any
    ) -> str:
        """
        Generates a fake or real vmess:// or vless:// link.

        Args:
            link_type (str): The type of the link ('vmess' or 'vless').
            server_address (str): The server address or IP.
            port (int): The server port.
            security (str): The security protocol (e.g., 'auto', 'none', 'tls'). Defaults to 'auto'.
            network (str): The network type (e.g., 'tcp', 'ws'). Defaults to 'tcp'.
            **kwargs: Additional parameters specific to the link type (e.g., 'path' for ws, 'flow' for vless).

        Returns:
            str: The generated VPN link string.

        Raises:
            ValueError: If the link_type is not 'vmess' or 'vless'.
        """
        logger.info(
            f"Generating VPN link of type {link_type} for server {server_address}:{port}"
        )
        user_id = str(uuid.uuid4())

        if link_type.lower() == "vmess":
            vmess_config = {
                "v": "2",
                "ps": "Test Bot Generated",  # Placeholder name
                "add": server_address,
                "port": str(port),
                "id": user_id,
                "aid": "0",  # AlterId, commonly 0 for single-user links
                "net": network,
                "type": "none",  # Usually 'none' for tcp, or 'ws'
                "host": "",
                "path": "",
                "tls": "",
                "sni": "",
                "alpn": "",
                "scy": security,  # Use the passed security parameter
            }

            # Update with specific kwargs if provided
            vmess_config.update(kwargs)
            logger.debug(f"VMess config: {vmess_config}")

            json_config = json.dumps(vmess_config)
            encoded_config = base64.b64encode(json_config.encode("utf-8")).decode("utf-8")
            link = f"vmess://{encoded_config}"
            logger.info("VMess link generated successfully.")
            return link

        elif link_type.lower() == "vless":
            # Construct VLESS parameters
            params = f"security={security}&type={network}"

            # Add specific kwargs as parameters
            for key, value in kwargs.items():
                params += f"&{key}={value}"

            link = (
                f"vless://{user_id}@{server_address}:{port}?{params}#Test Bot Generated"
            )  # Placeholder name
            logger.info("VLESS link generated successfully.")
            return link

        else:
            logger.error(f"Invalid link_type specified: {link_type}")
            raise ValueError("Invalid link_type. Must be 'vmess' or 'vless'.")
