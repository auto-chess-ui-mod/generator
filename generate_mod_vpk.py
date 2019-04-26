
# coding: utf-8

# ## Imports

import os, re, sys, shutil, argparse

# Import config file

import config

# ## Parameters

parser = argparse.ArgumentParser()

parser.add_argument("--no-drawStats", action='store_false', dest='drawStats')
parser.add_argument("--no-tierIndicator", action='store_false', dest='tierIndicator')
parser.add_argument("--saveGithub", action='store_true', dest='saveGithub')

parser.set_defaults(drawStats=True)
parser.set_defaults(tierIndicator=True)
parser.set_defaults(saveGithub=False)

args = parser.parse_args()

DRAW_STATS = args.drawStats
TIER_INDICATOR = args.tierIndicator
SAVE_GITHUB = args.saveGithub

# ## Paths

path_to_vpk = config.paths['path_to_vpk']
path_to_decompiler = config.paths['path_to_decompiler']
path_to_custom_code = config.paths['path_to_custom_code']
path_to_store_og_code = config.paths['path_to_store_og_code']
path_to_store_uncompiled_code = config.paths['path_to_store_uncompiled_code']
path_to_content_folder = config.paths['path_to_content_folder']
path_to_mod_folder = config.paths['path_to_mod_folder']
path_to_compiler = config.paths['path_to_compiler']
path_to_folder_to_compile = config.paths['path_to_folder_to_compile']
path_to_game = config.paths['path_to_game'] 
path_to_vpk_packager = config.paths['path_to_vpk_packager']

# ### Make sure the tmp folders exists

for folder in [path_to_store_og_code, path_to_store_uncompiled_code]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# # Main logic:

# ## First get the original `dota_hud_pregame.vjs_c` file

# For this we use: https://github.com/SteamDatabase/ValveResourceFormat  
# This requires .dot CORE SDK: https://dotnet.microsoft.com/download

command_template = 'dotnet "{}" -i "{}" -e "vjs_c" -f "panorama/scripts/hud/dota_hud_pregame.vjs_c" -o {} -d'
command = command_template.format(path_to_decompiler, path_to_vpk, path_to_store_og_code)

status_retrieval = os.system(command)

if status_retrieval == 0:
    print('good')
else:
    raise

# ## Create modified code

# ### Load original code

with open(os.path.join(path_to_store_og_code, os.path.normpath('panorama/scripts/hud/dota_hud_pregame.js')), 'r') as file:
    original_code = file.read()

# ### Load modded code

with open(os.path.join(path_to_custom_code, 'dota_hud_pregame.js'), 'r', encoding='utf-8') as file:
    modded_code = file.read()

# ### Modify based on parameters

# Include / Exclude draw statistics

if not DRAW_STATS:
    modded_code = re.sub('\/\*START-DRAWSTAT\*\/(.*?)\/\*END-DRAWSTAT\*\/', '', modded_code, flags=re.DOTALL)
    modded_code = re.sub('var DISPLAY_DRAW_PROB = true;', 'var DISPLAY_DRAW_PROB = false;', modded_code)


# Include / Exclude tier indicator

if not TIER_INDICATOR:
    modded_code = re.sub('var DISPLAY_TIER = true;', 'var DISPLAY_TIER = false;', modded_code)

# ### Combine

modified_code = original_code + '\n' + modded_code

# Save

tmp_path = os.path.join(path_to_store_uncompiled_code, os.path.normpath('panorama/scripts/hud'))
if not os.path.exists(tmp_path):
    os.makedirs(tmp_path)

with open(os.path.join(tmp_path, 'dota_hud_pregame.js'), 'w', encoding='utf-8') as file:
    file.write(modified_code)

# ## Create VPK file for mod

# ### Move new data to content folder

if os.path.exists(path_to_content_folder):
    shutil.rmtree(path_to_content_folder)
os.mkdir(path_to_content_folder)
shutil.copytree(os.path.join(path_to_store_uncompiled_code, 'panorama'), os.path.join(path_to_content_folder, 'panorama'))


# ### Compile

if os.path.exists(path_to_mod_folder):
    shutil.rmtree(path_to_mod_folder)

compile_command = r'"{}" -v -i "{}\\*" -r -game "{}"'.format(path_to_compiler, path_to_folder_to_compile, path_to_game)

print(compile_command)

# ### Run command

o=os.popen(compile_command).read()
print(o)


# ## Create VPK

# ### Create `vpk_list.txt`

file_list = ['panorama/scripts/hud/dota_hud_pregame.vjs_c']
with open(os.path.join(path_to_mod_folder, 'vpk_list.txt'), 'w') as f:
    for item in file_list:
        f.write("%s\n" % item)    

# ### Command

old_wd = os.getcwd()
os.chdir(path_to_mod_folder)

o=os.popen('"{}" a pak01 @vpk_list.txt'.format(path_to_vpk_packager)).read()
print(o)

os.chdir(old_wd)

## Final log message

print('Mod file generated: {}'.format(path_to_mod_folder))

# Save for GitHub

GITHUB_FOLDER = r'D:\modding_tools\auto-chess-ui-mod\download\vpk'

if SAVE_GITHUB:
    if DRAW_STATS:
        if TIER_INDICATOR:
            tmp_path = os.path.join(GITHUB_FOLDER, 'full_tier')
        else:
            tmp_path = os.path.join(GITHUB_FOLDER, 'full')
    else:
        tmp_path = os.path.join(GITHUB_FOLDER, 'lite')

    shutil.copyfile(os.path.join(path_to_mod_folder, 'pak01_dir.vpk'), os.path.join(tmp_path, 'pak01_dir.vpk'))
    print('Saved file to: {}'.format(tmp_path))




