# vim: expandtab tabstop=4 shiftwidth=4

from csv import DictReader
from dataclasses import dataclass
from pathlib import Path

import sys

@dataclass
class Field:
    has_empties: bool
    is_int: bool
    is_float: bool
    shortest_value: str
    longest_value: str

def has_empties(current_field: Field|None, value: str) -> bool:
    return len(value) == 0 or (current_field is not None and current_field.has_empties)

def is_int(current_field: Field|None, value: str) -> bool:
    try:
        int_val = int(value)
    except ValueError:
        return False

    value_is_int = str(int_val) == value

    if current_field is not None:
        return value_is_int and current_field.is_int

    return value_is_int

def is_float(current_field: Field|None, value: str) -> bool:
    try:
        float_val = float(value)
    except ValueError:
        return False

    value_is_float = str(float_val) == value

    if current_field is not None:
        return value_is_float and current_field.is_float

    return value_is_float

def shortest_value(current_field: Field|None, value: str) -> str:
    if current_field is not None:
        if len(value) < len(current_field.shortest_value):
            return value

        return current_field.shortest_value

    return value

def longest_value(current_field: Field|None, value: str) -> str:
    if current_field is not None:
        if len(value) > len(current_field.longest_value):
            return value

        return current_field.longest_value

    return value

def analyze_field(current_field: Field|None, value: str) -> Field:
    return Field(
        has_empties=has_empties(current_field, value),
        is_int=is_int(current_field, value),
        is_float=is_float(current_field, value),
        shortest_value=shortest_value(current_field, value),
        longest_value=longest_value(current_field, value),
    )

def analyze(path: Path) -> None:
    with path.open('r') as f:
        reader = DictReader(f)
        fields = {}

        for count, record in enumerate(reader):
            if count % 1000 == 0:
                print(f'{count}...')

            for field in record.keys():
                fields[field] = analyze_field(fields.get(field), record[field])

    for field in sorted(fields.keys()):
        print(f'{path}: {field}: {fields[field]}: VARCHAR({len(fields[field].longest_value)})')


def main():
    paths = [Path(x) for x in sys.argv[1:]]

    for path in paths:
        analyze(path)

if __name__ == "__main__":
    main()
