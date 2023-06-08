from dataclasses import dataclass
from sqlalchemy.sql.schema import Column


@dataclass
class AlchemizedModelColumn:
    column: Column
    column_name: str
    header_display_name: str = None
    flags: dict = None
