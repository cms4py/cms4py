from cms4py import file_helper
from .cached_data_wrapper import CachedDataWrapper

cached_files_map = {}


async def _cache_file(file_path):
    file_content = await file_helper.read_file_async(file_path)
    cached_files_map[file_path] = CachedDataWrapper(file_content, await file_helper.getmtime(file_path))
    return file_content


async def get_file_content(file_path) -> bytes:
    """
    If the file is modified, we will reread it
    :param file_path:
    :return:
    """
    file_content = None
    file_exists = await file_helper.file_exists(file_path) and await file_helper.isfile(file_path)
    if file_path in cached_files_map:
        wrapper: CachedDataWrapper = cached_files_map[file_path]
        file_content = wrapper.data
        if file_exists and await file_helper.getmtime(file_path) != wrapper.timestamp:
            file_content = _cache_file(file_path)
    elif file_exists:
        file_content = _cache_file(file_path)
    return file_content
