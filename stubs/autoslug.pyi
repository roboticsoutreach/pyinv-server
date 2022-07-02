
from typing import Optional
from django.forms import SlugField


class AutoSlugField(SlugField):
    
    def __init__(
        self,
        *,
        max_length: int = 50,
        populate_from: Optional[str] = None,
        editable: bool = False,
        unique: bool = False,
        null: bool = False,
        default: Optional[str] = None,
    ) -> None: ...
