from typing import List, Optional

from pydantic import BaseModel


class Sorting(BaseModel):
    sort_by: Optional[List[str]] = None
    sort_order: Optional[List[str]] = None
