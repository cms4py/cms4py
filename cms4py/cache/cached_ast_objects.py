from cms4py import file_helper
import os
cached_map = {}


async def _cache_source(source_file_path):
    file_content = await file_helper.read_file_async(source_file_path)
    ast_object = compile(
        file_content,
        source_file_path,
        "exec"
    )
    cached_map[source_file_path] = {
        "ast": ast_object,
        "mtime": await file_helper.getmtime(source_file_path)
    }
    return ast_object


async def get_ast_object(source_file_path):
    """
    If there is no file and no cache, return None
    """
    ast_object = None
    source_file_exists = await file_helper.file_exists(source_file_path) and await file_helper.isfile(source_file_path)
    if source_file_path in cached_map:
        cached_object = cached_map[source_file_path]
        ast_object = cached_object['ast']
        if source_file_exists:
            source_file_mtime = await file_helper.getmtime(source_file_path)
            if source_file_mtime != cached_object['mtime']:
                ast_object = await _cache_source(source_file_path)
    elif source_file_exists:
        ast_object = await _cache_source(source_file_path)
    return ast_object
