from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union
from bittensor.utils import networking
from bittensor.chain_data.utils import ChainDataType, from_scale_encoding
from bittensor.utils.registration import torch, use_torch


@dataclass
class IPInfo:
    """Dataclass for associated IP Info."""

    ip: str
    ip_type: int
    protocol: int

    def encode(self) -> Dict[str, Any]:
        """Returns a dictionary of the IPInfo object that can be encoded."""
        return {
            "ip": networking.ip_to_int(
                self.ip
            ),  # IP type and protocol are encoded together as a u8
            "ip_type_and_protocol": ((self.ip_type << 4) + self.protocol) & 0xFF,
        }

    @classmethod
    def from_vec_u8(cls, vec_u8: List[int]) -> Optional["IPInfo"]:
        """Returns a IPInfo object from a ``vec_u8``."""
        if len(vec_u8) == 0:
            return None

        decoded = from_scale_encoding(vec_u8, ChainDataType.IPInfo)
        if decoded is None:
            return None

        return IPInfo.fix_decoded_values(decoded)

    @classmethod
    def list_from_vec_u8(cls, vec_u8: List[int]) -> List["IPInfo"]:
        r"""Returns a list of IPInfo objects from a ``vec_u8``."""
        decoded = from_scale_encoding(vec_u8, ChainDataType.IPInfo, is_vec=True)

        if decoded is None:
            return []

        return [IPInfo.fix_decoded_values(d) for d in decoded]

    @classmethod
    def fix_decoded_values(cls, decoded: Dict) -> "IPInfo":
        """Returns a IPInfo object from a decoded IPInfo dictionary."""
        return IPInfo(
            ip=networking.int_to_ip(decoded["ip"]),
            ip_type=decoded["ip_type_and_protocol"] >> 4,
            protocol=decoded["ip_type_and_protocol"] & 0xF,
        )

    def to_parameter_dict(
        self,
    ) -> Union[dict[str, Union[str, int]], "torch.nn.ParameterDict"]:
        """Returns a torch tensor or dict of the subnet IP info."""
        if use_torch():
            return torch.nn.ParameterDict(self.__dict__)
        else:
            return self.__dict__

    @classmethod
    def from_parameter_dict(
        cls, parameter_dict: Union[dict[str, Any], "torch.nn.ParameterDict"]
    ) -> "IPInfo":
        if use_torch():
            return cls(**dict(parameter_dict))
        else:
            return cls(**parameter_dict)
