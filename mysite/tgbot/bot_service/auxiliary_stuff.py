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

    pdf = 1
    doc = 2
    txt = 3
    fb2 = 4


class InlineKeyboard_Status(enum.Enum):

    initial = 1
    asking_for_end = 2
    asking_for_convertation = 3
    after_end = 4