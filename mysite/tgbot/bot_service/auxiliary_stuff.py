import enum


class Message_Type(enum.Enum):

    text = 1
    document = 2
    image = 3
    sticker = 4
    garbage = 5
    compressed_image = 6
    pdf_document = 7
    callback_query = 8


class Extensions(enum.Enum):

    fb2 = 1
    epub = 2


class InlineKeyboard_Status(enum.Enum):

    after_end = 4