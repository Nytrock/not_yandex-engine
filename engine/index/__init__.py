import threading

import json

import os


class SearchIndex:
    def __init__(self, parser, stop_words):
        self.parser = parser

        self.page_terms = {}
        self.total_index = {}
        self.stop_words = stop_words

        self._sl = {}

    # делает промежуточные хеш таблицы
    def _process_pages(self):
        self.parser.get_urls()
        self.page_terms = self.parser.content_dict
        return self.page_terms

    # индексирует один файл
    def _index_one_page(self, terms, key):
        page_index = {}
        for ind, word in enumerate(terms):
            if word in page_index.keys():
                page_index[word].append(ind)
            else:
                page_index[word] = [ind]
        self._sl[key] = page_index
        print(self._sl[key])

    # индексирует все файлы
    def _index_all_pages(self):
        self._sl = {}
        index_threads = []
        for key, terms in self.page_terms.items():
            index_threads.append(threading.Thread(target=self._index_one_page, args=(terms, key)))
        for thread in index_threads:
            thread.start()
        for thread in index_threads:
            thread.join()
        self.page_terms = self._sl
        print('finish')

    # формирует окончательный индекс
    def _full_index(self):
        buffer = {}
        for page_url in self.page_terms.keys():
            for word in self.page_terms[page_url].keys():
                if word in buffer.keys():
                    if page_url in buffer[word].keys():
                        buffer[word][page_url].extend(self.page_terms[page_url][word][:])
                    else:
                        buffer[word][page_url] = self.page_terms[page_url][word]
                else:
                    buffer[word] = {page_url: self.page_terms[page_url][word]}
            print(len(buffer))
        self.total_index = buffer

    # формирует индекс
    def create(self):
        self._process_pages()
        self._index_all_pages()
        self._full_index()

        self.save_index()

    def save_index(self):
        with open(f'{self.parser.main_url}.json', 'w', encoding='UTF-8') as save_file:
            json.dump(self.total_index, save_file, indent=4, ensure_ascii=False)

    def load_index(self):
        if 'save.json' in os.listdir():
            with open(f'{self.parser.main_url}.json', 'r', encoding='UTF-8') as load_file:
                self.total_index = json.load(load_file)
        else:
            self.create()
