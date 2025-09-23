import dataclasses
import os

PATH = os.path.join(os.path.dirname(__file__).split('src')[0], 'src', 'config')

@dataclasses.dataclass
class BaseAccount:
    port: int
    username: str
    password: str

@dataclasses.dataclass
class JlyqAccount(BaseAccount):
    pass

@dataclasses.dataclass
class KsAccount(BaseAccount):
    account_url: str
