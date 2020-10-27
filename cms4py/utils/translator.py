
import config, os
from cms4py.utils import aiofile
from cms4py.cache.json_file_cache_manager import JsonFileCacheManager


async def get_language_dict(language):
    """
    根据语言名将对应的JSON文件读成Python对象
    :param language: 语言名，如：zh-CN、en-US等
    :return: 如果文件不存在，返回 None
    """
    language_dict = None
    language_file = os.path.join(
        config.LANGUAGES_ROOT, f"{language}.json"
    )
    if await aiofile.exists(
            language_file
    ) and await aiofile.isfile(language_file):
        language_dict = await JsonFileCacheManager \
            .get_instance() \
            .get_data(language_file)
    return language_dict


async def translate(words: str, target_language: str) -> str:
    """
    将指定的句子翻译成目标语言
    :param words:
    :param target_language:
    :return:
    """
    result = words
    # 加载语言表
    language_dict = await get_language_dict(target_language)
    if language_dict and words in language_dict:
        # 获取语言对应的翻译
        result = language_dict[words]
    return result
