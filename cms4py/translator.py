import config, os
from . import file_helper


async def translate(words: str, target_language: str) -> str:
    target_language_file = os.path.join(config.LANGUAGES_ROOT, target_language)
    if await file_helper.file_exists(target_language_file) and await file_helper.isfile(target_language_file):
        pass
    else:
        return words
