import logging as log
import json

class CatStore:

    def __init__(self, file_name):
        self.file_name = file_name
        try:
            with open(file_name) as cat_file:
                self.cats = json.load(cat_file)
        except FileNotFoundError:
            self.cats = dict()
            log.info('"%s" not found. Initializing empty cat store.', file_name)


    def add(self, cats):
        self._new_cats = []
        for cat in cats:
            if cat['url'] not in self.cats:
                self._new_cats.append(cat)
            self.cats[cat['url']] = cat


    def get_new_cats(self):
        return self._new_cats


    def save(self):
        if not self.cats:
            log.warning('Did not find any cats! Not saving anything.')
            return

        # Save the cats. (Overwrite the old file, if any.)
        with open(self.file_name, 'w') as cat_file:
            json.dump(self.cats, cat_file, indent=2)
            log.info('Successfully dumped cats into "%s"', self.file_name)
