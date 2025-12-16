# Copyright (C) 2024 by Badhacker98@Github, < https://github.com/Badhacker98 >.
# Owner https://t.me/ll_BAD_MUNDA_ll

import glob
import importlib
import logging
import os
import shutil
import subprocess
import sys
from os.path import abspath, dirname, isfile, join

from config import (
    EXTRA_PLUGINS_REPO,
    EXTRA_PLUGINS_FOLDER,
    EXTRA_PLUGINS, 
    CHATBOT_REPO,
    CHATBOT_ENABLED,
    CHATBOT_FOLDER,
)
from BADMUSIC import LOGGER

logger = LOGGER(__name__)

ROOT_DIR = abspath(join(dirname(__file__), "..", ".."))

# ============================
if EXTRA_PLUGINS_FOLDER in os.listdir():
    shutil.rmtree(EXTRA_PLUGINS_FOLDER)

if "utils" in os.listdir():
    shutil.rmtree("utils")

# ==============(PbxBad/PLUGINS) ==============
EXTRA_REPO_PATH = join(ROOT_DIR, EXTRA_PLUGINS_FOLDER)
extra_plugins_enabled = EXTRA_PLUGINS.lower() == "true" if "EXTRA_PLUGINS" in globals() else True

if extra_plugins_enabled:
    if not os.path.exists(EXTRA_REPO_PATH):
        with open(os.devnull, "w") as devnull:
            clone_result = subprocess.run(
                ["git", "clone", EXTRA_PLUGINS_REPO, EXTRA_REPO_PATH],
                stdout=devnull,
                stderr=subprocess.PIPE,
            )
            if clone_result.returncode != 0:
                logger.error(f"Error cloning main extra plugins repo: {clone_result.stderr.decode()}")

    utils_source = join(EXTRA_REPO_PATH, "utils")
    utils_target = join(ROOT_DIR, "utils")
    if os.path.isdir(utils_source):
        if os.path.exists(utils_target):
            shutil.rmtree(utils_target)
        shutil.move(utils_source, utils_target)
        sys.path.append(utils_target)

    # Install requirements
    req_path = join(EXTRA_REPO_PATH, "requirements.txt")
    if os.path.isfile(req_path):
        with open(os.devnull, "w") as devnull:
            subprocess.run(["pip", "install", "-r", req_path], stdout=devnull, stderr=subprocess.PIPE)

# ============== ChatBot ==============
CHATBOT_REPO_PATH = join(ROOT_DIR, "chatbot_plugins") 

if CHATBOT_ENABLED:
    logger.info("ʟᴏᴀᴅɪɴɢ ᴄʜᴀᴛʙᴏᴛ ᴇxᴛʀᴀ ᴘʟᴜɢɪɴꜱ...")
    if os.path.exists(CHATBOT_REPO_PATH):
        shutil.rmtree(CHATBOT_REPO_PATH)

    with open(os.devnull, "w") as devnull:
        clone_result = subprocess.run(
            ["git", "clone", CHATBOT_REPO, CHATBOT_REPO_PATH],
            stdout=devnull,
            stderr=subprocess.PIPE,
        )
        if clone_result.returncode != 0:
            logger.error(f"ᴇʀʀᴏʀ ᴄʟᴏɴɪɴɢ ᴄʜᴀᴛʙᴏᴛ ʀᴇᴘᴏ: {clone_result.stderr.decode()}")
        else:
            logger.info("ᴄʜᴀᴛʙᴏᴛ ʀᴇᴘᴏ ᴄʟᴏɴᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ.")

    # Install requirements if any
    chatbot_req = join(CHATBOT_REPO_PATH, "requirements.txt")
    if os.path.isfile(chatbot_req):
        with open(os.devnull, "w") as devnull:
            subprocess.run(["pip", "install", "-r", chatbot_req], stdout=devnull, stderr=subprocess.PIPE)

def __list_all_modules():
    main_repo_plugins_dir = dirname(__file__)
    work_dirs = [main_repo_plugins_dir]

    if extra_plugins_enabled and os.path.exists(EXTRA_REPO_PATH):
        extra_plugins_dir = join(EXTRA_REPO_PATH, "plugins")
        if os.path.exists(extra_plugins_dir):
            work_dirs.append(extra_plugins_dir)

    if CHATBOT_ENABLED and os.path.exists(CHATBOT_REPO_PATH):
        chatbot_plugins_dir = join(CHATBOT_REPO_PATH, CHATBOT_FOLDER)
        if os.path.exists(chatbot_plugins_dir):
            work_dirs.append(chatbot_plugins_dir)
            logger.info(f"ᴀᴅᴅᴇᴅ ᴄʜᴀᴛʙᴏᴛ ᴘʟᴜɢɪɴꜱ ꜰᴏʟᴅᴇʀ: {chatbot_plugins_dir}")

    all_modules = []

    for work_dir in work_dirs:
        mod_paths = glob.glob(join(work_dir, "*.py"))
        mod_paths += glob.glob(join(work_dir, "*/*.py"))

        modules = [
            os.path.relpath(f, ROOT_DIR).replace(os.sep, ".")[:-3]
            for f in mod_paths
            if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
        ]
        all_modules.extend(modules)

    return sorted(set(all_modules))  


ALL_MODULES = __list_all_modules()
__all__ = ALL_MODULES + ["ALL_MODULES"]

logger.info(f"ᴛᴏᴛᴀʟ ᴍᴏᴅᴜʟᴇꜱ ʟᴏᴀᴅᴇᴅ: {len(ALL_MODULES)}")
