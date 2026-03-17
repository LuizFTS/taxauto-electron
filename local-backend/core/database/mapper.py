from dataclasses import fields
from typing import Type, TypeVar

T = TypeVar("T")


def row_to_entity(row, entity_class: Type[T]) -> T:
    if row is None:
        return None

    entity_fields = {f.name for f in fields(entity_class)}

    data = {k: row[k] for k in row.keys() if k in entity_fields}

    return entity_class(**data)


def rows_to_entities(rows, entity_class: Type[T]) -> list[T]:
    return [row_to_entity(row, entity_class) for row in rows]
