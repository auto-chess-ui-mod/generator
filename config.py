import os 

## Modify these paths to your system!

paths = dict(
    path_to_game = os.path.abspath(r"D:\Steam\steamapps\common\dota 2 beta\game\dota"),
    path_to_vpk = os.path.abspath(r"D:\Steam\steamapps\common\dota 2 beta\game\dota\pak01_dir.vpk"),
    path_to_decompiler = os.path.abspath(r"D:\modding_tools\auto-chess-ui-mod\generator\utils\dota2_decompiler\Decompiler.dll"),
    path_to_compiler = os.path.abspath(r"D:\Steam\steamapps\common\dota 2 beta\game\bin\win64\resourcecompiler.exe"),
    path_to_custom_code = os.path.abspath(r"D:\modding_tools\auto-chess-ui-mod\source"),
    path_to_content_folder = os.path.abspath(r"D:\Steam\steamapps\common\dota 2 beta\content\custom_dac_ui"),
    path_to_mod_folder = os.path.abspath(r"D:\Steam\steamapps\common\dota 2 beta\game\custom_dac_ui"),
    path_to_folder_to_compile = os.path.abspath(r"D:\Steam\steamapps\common\dota 2 beta\content\custom_dac_ui\panorama"),
    path_to_vpk_packager = os.path.abspath(r"D:\modding_tools\auto-chess-ui-mod\generator\utils\vpk_packager\vpk.exe"),
    path_to_store_og_code = os.path.normpath("tmp/original_code"),
    path_to_store_uncompiled_code = os.path.normpath("tmp/modified_code_uncompiled"),
)

params = dict(
    DRAW_STATS = True,
    TIER_INDICATOR = True,
)