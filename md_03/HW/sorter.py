"""
Напишіть програму обробки папки "Мотлох", яка сортує файли у вказаній папці за розширеннями з використанням кількох потоків. Пришвидшіть обробку 
великих каталогів з великою кількістю вкладених папок та файлів за рахунок паралельного виконання обходу всіх папок в окремих потоках. 
Найвитратнішим за часом буде перенесення файлу та отримання списку файлів у папці (ітерація за вмістом каталогу). Щоб прискорити перенесення 
файлів, його можна виконувати в окремому потоці або пулі потоків. Це тим зручніше, що результат цієї операції ви в застосунку не обробляєте та 
можна не збирати жодних результатів. Щоб прискорити обхід вмісту каталогу з кількома рівнями вкладеності, ви можете обробку кожного підкаталогу 
виконувати в окремому потоці або передавати обробку в пул потоків.

"""

import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor


FORMATS_MAPPING ={
    'Audio': [
        '.mp3', '.wav', '.aac', '.wma', '.ogg', '.flac', '.alac', '.aiff', '.ape', '.au', 
        '.m4a', '.m4b', '.m4p', '.m4r', '.mid', '.midi', '.mpa', '.mpc', '.oga', '.opus', 
        '.ra', '.ram', '.tta', '.weba'
        ],
    'Video': [
        '.mp4', '.avi', '.mkv', '.wmv', '.mov', '.flv', '.webm', '.m4v', '.mpg', '.mpeg', 
        '.3gp', '.3g2', '.m2ts', '.mts', '.vob', '.ogv', '.mxf', '.divx', '.f4v', '.h264'
        ],
    'Images': [
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff', '.svg', '.webp', '.eps', 
        '.raw', '.cr2', '.nef', '.dng', '.orf', '.arw', '.pef', '.raf', '.sr2', '.kdc', '.mos', 
        '.mrw', '.dcr', '.x3f', '.erf', '.mef', '.pcx'
        ],
    'Documents': [
        '.dot', '.odi', '.sxc', '.sxd', '.doc', '.txt', '.odf', '.sxw', '.odt', '.pdf', '.sxg', 
        '.ott', '.odg', '.stw', '.sxi', '.stc', '.dotm', '.md', '.odc', '.docx', '.dotx', '.rtf'
        ],
    'Spreadsheets': [
        '.xls', '.xlsx', '.csv', '.xlsm', '.xlt', '.xltx', '.xlsb', '.numbers', '.ods'
        ],
    'Presentations': [
        '.ppt', '.pptx', '.key', '.odp', '.pps', '.ppsx', '.pot', '.potx', '.potm'
        ],
    'Archives': [
        '.zip', '.rar', '.tar.gz', '.7z', '.tar', '.tgz', '.bz2', '.dmg', '.iso', '.gz', '.jar', 
        '.cab', '.z', '.tar.bz2', '.xz'
        ],
    'Programs': [
        '.exe', '.apk', '.app', '.msi', '.deb', '.rpm', '.bat', '.sh', '.com', '.gadget', '.vb', 
        '.vbs', '.wsf'
        ],
    'Code': [
        '.py', '.java', '.js', '.html', '.css', '.cpp', '.c', '.php', '.xml', '.rb', '.pl', '.swift', 
        '.h', '.hpp', '.cs', '.m', '.mm', '.kt', '.dart', '.go', '.lua', '.r', '.ps1'
        ],
    'Database': [
        '.sql', '.db', '.mdb', '.accdb', '.sqlitedb', '.dbf', '.dbs', '.myd', '.frm', '.sqlite'
        ],
    'Ebook': [
        '.epub', '.azw', '.azw3', '.fb2', '.ibooks', '.lit', '.mobi', '.pdb'
        ]
}

class SortFolderHandler:
    def __init__(self, path: Path) -> None:
        '''Takes as parameter path to the folder that should be sorted.'''
        self._path = Path().cwd()
        self.path = path

    @property
    def path(self) -> Path:
        return self._path
    
    @path.setter
    def path(self, value) -> None:
        try:
            value = Path(value)
            if not value.is_dir():
                raise ValueError('Path should point to dir and not file.')
        except Exception as err:
            print(err)
        self._path = value

    def _parse_folder(self) -> list[Path]:
        '''Returns list of subdirs including nested ones.'''
        folders = [self.path]
        def parse_recursively(path) -> None:
            nonlocal folders
            for item in path.iterdir():
                if item.is_dir():
                    folders.append(item)
                    parse_recursively(item)

        parse_recursively(self.path)
        return folders


    def _map_file_category(self, file: Path, formats: dict = FORMATS_MAPPING) -> str:
        '''Map file extension with category and returns string of respective category.'''
        ext = file.suffix.lower()
        for category, ext_list in formats.items():
            if ext in ext_list:
                return category
        else:
            return 'Unknown_extensions'


    def _sort_files_to(self, source: Path) -> None:
        '''Moves files to a directory according to the extension.'''
        for item in source.iterdir():
            if item.is_file():
                category = self._map_file_category(item)
                dest_folder = self.path / category
                dest_folder.mkdir(exist_ok=True)
                try:
                    item.rename(dest_folder / item.name)
                except OSError as err:
                    print(err)

                

    def _remove_empty_dirs(self, sub_dir: str|Path = None) -> None:
        """Deletes empty dirs recursively."""
        if not sub_dir:
            current_folder = self.path
        else:
            current_folder = sub_dir
            
        for root, dirs, files in os.walk(current_folder, topdown=False):
            for dir in dirs:
                self._remove_empty_dirs(os.path.join(root, dir))
            if not dirs and not files:
                os.rmdir(root) # os.rmdir() removes only if dir is empty
            
    def sort_folder(self) -> None:
        '''Sort files using threading'''
        folders = self._parse_folder()
        with ThreadPoolExecutor() as executor:
            executor.map(self._sort_files_to, folders)    
        self._remove_empty_dirs()
        print(f'Folder: "{self.path}" was successfully sorted!')
        

if __name__ == '__main__':
    folder = SortFolderHandler('/home/maksymklym/Desktop/Download')
    folder.sort_folder()


    