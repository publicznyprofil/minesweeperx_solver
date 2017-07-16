from enum import Enum


class FieldType(Enum):
    EMPTY = 0
    ONE_BOMB = 1
    TWO_BOMB = 2
    THREE_BOMB = 3
    FOUR_BOMB = 4
    FIVE_BOMB = 5
    SIX_BOMB = 6
    SEVEN_BOMB = 7
    EIGHT_BOMB = 8
    UNCLICKABLE = 9
    BOMB = 11


BOMBS_AROUND_FIELDS = (
    FieldType.ONE_BOMB,
    FieldType.TWO_BOMB,
    FieldType.THREE_BOMB,
    FieldType.FOUR_BOMB,
    FieldType.FIVE_BOMB,
    FieldType.SIX_BOMB,
    FieldType.SEVEN_BOMB,
    FieldType.EIGHT_BOMB,
)

FIELD_BY_COLOR = {
    (192, 192, 192): FieldType.UNCLICKABLE,
    (0, 0, 255): FieldType.ONE_BOMB,
    (0, 128, 0): FieldType.TWO_BOMB,
    (255, 0, 0): FieldType.THREE_BOMB,
    (0, 0, 128): FieldType.FOUR_BOMB,
    (128, 0, 0): FieldType.FIVE_BOMB,
    (0, 128, 128): FieldType.SIX_BOMB,
    (0, 0, 0): FieldType.SEVEN_BOMB,
}
