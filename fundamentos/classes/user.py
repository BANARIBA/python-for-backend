from dataclasses import dataclass
from typing import List

@dataclass
class User:
  name: str
  age: int
  roles: List[str]
  is_Active: bool