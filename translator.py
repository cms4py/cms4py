import config, os
from .helpers import file_helper
from . import cache_managers


async def get_language_dict(language):
    language_dict = None
    language_file = os.path.join(config.LANGUAGES_ROOT, f"{language}.json")
    if await file_helper.file_exists(language_file) and await file_helper.isfile(language_file):
        language_dict = await cache_managers.JsonFileCacheManager.get_instance().get_data(language_file)
    return language_dict


async def translate(words: str, target_language: str) -> str:
    result = words
    language_dict = await get_language_dict(target_language)
    if language_dict and words in language_dict:
        result = language_dict[words]
    return result
