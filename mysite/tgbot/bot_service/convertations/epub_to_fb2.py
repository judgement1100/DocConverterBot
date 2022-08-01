import ebooklib
from ebooklib import epub
import os
from bs4 import BeautifulSoup
from ebooklib import epub
from FB2 import FictionBook2, Author, TitleInfo


class Epub_to_fb2:
    def get_chapters_from_epub(self, epub_path):
        book = epub.read_epub(epub_path)
        spine_elems = []
        chapters = []

        for item in book.spine:
            spine_elems.append(item[0])

        for i in range(len(spine_elems)):
            for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
                if item.id == spine_elems[i]:
                    chapters.append(item.get_content())

        return chapters


    def add_list_elems_to_tuple(self, my_tuple: tuple, list_to_add: list):
        list_from_tuple = list(my_tuple)
        list_to_change = list_from_tuple[1]
        list_to_change += list_to_add
        list_from_tuple = tuple([list_from_tuple[0], list_to_change])
        my_tuple = list_from_tuple
        return my_tuple


    def set_fb2_chapters(self, book_fb2: FictionBook2, epub_path: str):
        chapters = self.get_chapters_from_epub(epub_path)
        for chapter in chapters:
            soup = BeautifulSoup(chapter, 'html.parser')
            title = ""
            paragraphs = []

            for item in soup.find_all():
                if item.get('class') == ['p']:
                    title += item.getText() + " "
                elif item.get('class') == ['p1']:
                    paragraphs.append(item.getText())

            if len(title) > 0:
                book_fb2.chapters.append((title, paragraphs))
            elif len(paragraphs) > 0:
                self.add_list_elems_to_tuple(book_fb2.chapters[len(book_fb2.chapters) - 1], paragraphs)

        return book_fb2


    def convert_epub_to_fb2(self, fb2_path, epub_path):
        book_epub = epub.read_epub(epub_path)
        book_fb2 = FictionBook2()

        book_fb2.titleInfo = TitleInfo(title=f"{book_epub.title}",
                                       authors=[Author(book_epub.get_metadata('DC', 'creator')[0][0])],
                                       annotation=book_epub.get_metadata('DC', 'description')[0][0])

        book_fb2 = self.set_fb2_chapters(book_fb2, epub_path)

        book_fb2.write(fb2_path)
        return fb2_path




