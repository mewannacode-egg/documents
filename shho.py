"""
FileSystem.py
A lightweight filesystem abstraction layer (custom API design)
"""

import os
import shutil
import subprocess
import sys
from typing import Optional, List, Union, Generator, Any
import inspect


# ─────────────────────────────────────────────
# INTERNAL HELPERS
# ─────────────────────────────────────────────

class _Internal:
    """
    Internal helper functions.
    Not part of public API.
    """

    @staticmethod
    def normalize(path: str) -> str:
        return os.path.abspath(path)

    @staticmethod
    def handle_error(error: Exception, errors: bool, fallback=None):
        if errors:
            raise error
        print(error)
        return fallback


# ─────────────────────────────────────────────
# FILE API (public)
# ─────────────────────────────────────────────

class File:

    @staticmethod
    def create(src: str, overwrite: bool = False, errors: bool = False):
        try:
            if overwrite and os.path.isfile(src):
                os.remove(src)

            with open(src, "w", encoding="utf-8"):
                pass

            return True
        except Exception as e:
            return _Internal.handle_error(e, errors, False)

    @staticmethod
    def delete(src: str, mode: str = "perm", confirm: bool = False, errors: bool = False):
        try:
            if not confirm:

                if mode == "perm":
                    prompt = f"Permanently delete '{src}'? y/n: "
                elif mode == "trash":
                    prompt = f"Move '{src}' to trash? y/n: "
                else:
                    raise ValueError("mode must be 'trash' or 'perm'")

                if input(prompt).lower() != "y":
                    return False

            if mode == "perm":
                os.remove(src)
                return True

            if mode == "trash":
                trash_dir = ".trash"
                os.makedirs(trash_dir, exist_ok=True)

                base = os.path.basename(src)
                target = os.path.join(trash_dir, base)

                shutil.move(src, target)
                return True

            return False

        except Exception as e:
            return _Internal.handle_error(e, errors, False)

    @staticmethod
    def read(src: str, line: int = None, errors: bool = False):
        try:
            size = os.path.getsize(src)
            if size > 30 * 1024 * 1024:
                choice = input(
                    f"File is large ({size / (1024 * 1024):.2f} MB). Continue reading? y/n: "
                ).lower()
                if choice != "y":
                    return None

            with open(src, "r", encoding="utf-8") as f:
                if line is None or line == 0:
                    return f.read()

                for current_line, text in enumerate(f, start=1):
                    if current_line == line:
                        return text.rstrip("\n")

            return None
        except Exception as e:
            return _Internal.handle_error(e, errors, None)

    @staticmethod
    def stream(src: str, errors: bool = False) -> Generator[str, None, None]:
        try:
            size = os.path.getsize(src)
            if size > 30 * 1024 * 1024:
                choice = input(
                    f"File is large ({size / (1024 * 1024):.2f} MB). Stream it? y/n: "
                ).lower()
                if choice != "y":
                    return

            with open(src, "r", encoding="utf-8") as f:
                for line in f:
                    yield line.rstrip("\n")
        except Exception as e:
            if errors:
                raise
            print(e)
            return

    @staticmethod
    def write(src: str, content: str, mode: str = "overwrite", line: int = None, errors: bool = False):
        try:
            if mode == "overwrite":
                with open(src, "w", encoding="utf-8") as f:
                    f.write(content + "\n")
                return True

            if mode == "append":
                with open(src, "a", encoding="utf-8") as f:
                    f.write(content + "\n")
                return True

            if mode == "line":
                if line is None or line <= 0:
                    raise ValueError("line must be a positive integer when mode='line'")

                lines = []
                try:
                    with open(src, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                except FileNotFoundError:
                    lines = []

                index = line - 1
                while len(lines) <= index:
                    lines.append("\n")

                lines[index] = content + "\n"

                with open(src, "w", encoding="utf-8") as f:
                    f.writelines(lines)

                return True

            raise ValueError("mode must be 'overwrite', 'append', or 'line'")
        except Exception as e:
            return _Internal.handle_error(e, errors, False)


# ─────────────────────────────────────────────
# FOLDER API
# ─────────────────────────────────────────────

class Folder:

    @staticmethod
    def create(src: str, overwrite: bool = False, errors: bool = False):
        try:
            if overwrite and os.path.isdir(src):
                shutil.rmtree(src)

            os.makedirs(src, exist_ok=True)
            return True
        except Exception as e:
            return _Internal.handle_error(e, errors, False)

import os
import shutil

class Folder:

    @staticmethod
    def delete(src: str, mode: str = "perm", confirm: bool = False, errors: bool = False):
        try:
            if not confirm:

                if mode == "perm":
                    prompt = f"Permanently delete folder '{src}'? y/n: "
                elif mode == "trash":
                    prompt = f"Move folder '{src}' to trash? y/n: "
                else:
                    raise ValueError("mode must be 'trash' or 'perm'")

                if input(prompt).lower() != "y":
                    return False

            if mode == "perm":
                shutil.rmtree(src)
                return True

            if mode == "trash":
                trash_dir = ".trash"
                os.makedirs(trash_dir, exist_ok=True)

                base = os.path.basename(src.rstrip("/\\"))
                target = os.path.join(trash_dir, base)

                shutil.move(src, target)
                return True

            return False

        except Exception as e:
            return _Internal.handle_error(e, errors, False)

    @staticmethod
    def is_empty(src: str, errors: bool = False):
        try:
            return len(os.listdir(src)) == 0
        except Exception as e:
            return _Internal.handle_error(e, errors, False)

    @staticmethod
    def empty(src: str, confirm: bool = False, errors: bool = False):
        try:
            if not confirm:
                choice = input(f"Empty all contents of '{src}'? y/n: ").lower()
                if choice != "y":
                    return False

            for item in os.listdir(src):
                path = os.path.join(src, item)
                try:
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                    else:
                        os.remove(path)
                except Exception as inner_error:
                    if errors:
                        raise
                    print(inner_error)

            return True
        except Exception as e:
            return _Internal.handle_error(e, errors, False)

    @staticmethod
    def list(src: str):
        try:
            return os.listdir(src)
        except Exception as e:
            print(e)
            return []

# ─────────────────────────────────────────────
# PATH API
# ─────────────────────────────────────────────

class Path:

    @staticmethod
    def copy(src: str, dst: str, errors: bool = False):
        try:
            if os.path.isfile(src):
                shutil.copy2(src, dst)
                return True

            if os.path.isdir(src):
                shutil.copytree(src, dst)
                return True

            raise FileNotFoundError(f"Source not found: {src}")
        except Exception as e:
            return _Internal.handle_error(e, errors, False)

    @staticmethod
    def move(src: str, dst: str, errors: bool = False):
        try:
            if os.path.isfile(src) and os.path.dirname(dst):
                os.makedirs(os.path.dirname(dst), exist_ok=True)

            shutil.move(src, dst)
            return True
        except Exception as e:
            return _Internal.handle_error(e, errors, False)

    @staticmethod
    def exists(src: str, kind: str = None):
        if kind == "file":
            return os.path.isfile(src)

        if kind in ("folder", "dir"):
            return os.path.isdir(src)

        return os.path.exists(src)

    @staticmethod
    def info(src: str, errors: bool = False):
        try:
            stats = os.stat(src)
            return {
                "path": _Internal.normalize(src),
                "type": "file" if os.path.isfile(src) else "folder" if os.path.isdir(src) else "unknown",
                "size": stats.st_size,
                "modified": stats.st_mtime,
                "exists": True
            }
        except Exception as e:
            return _Internal.handle_error(e, errors, None)

    @staticmethod
    def abspath(src: str):
        return os.path.abspath(src)

    @staticmethod
    def find(src: str, extensions=".png"):
        try:
            if isinstance(extensions, str):
                extensions = [extensions]

            results = []

            for root, _, files in os.walk(src):
                for file in files:
                    if any(file.endswith(ext) for ext in extensions):
                        results.append(os.path.join(root, file))

            return results

        except Exception as e:
            print(e)
            return []
        
# ─────────────────────────────────────────────
# SYSTEM LAYER ()))))))))))))))))
# ─────────────────────────────────────────────

class System:
    @staticmethod
    def run(src: str, confirm: bool = False, errors: bool = False):
        try:
            if not confirm:
                choice = input(f"Run '{src}'? y/n: ").lower()
                if choice != "y":
                    return False

            if src.endswith(".py"):
                subprocess.run([sys.executable, src], check=False)
                return True

            subprocess.run(src, shell=True, check=False)
            return True
        except Exception as e:
            return _Internal.handle_error(e, errors, False)

    @staticmethod
    def exec(command: str, confirm: bool = False, errors: bool = False):
        try:
            if not confirm:
                choice = input(f"Execute command '{command}'? y/n: ").lower()
                if choice != "y":
                    return False

            subprocess.run(command, shell=True, check=False)
            return True
        except Exception as e:
            return _Internal.handle_error(e, errors, False)

    @staticmethod
    def cwd():
        return os.getcwd()

    @staticmethod
    def cd(path: str, confirm: bool = False, errors: bool = False):
        try:
            if not confirm:
                choice = input(f"Change directory to '{path}'? y/n: ").lower()
                if choice != "y":
                    return False

            os.chdir(path)
            return True
        except Exception as e:
            return _Internal.handle_error(e, errors, False)

    @staticmethod
    def getenv(key: str, default=None):
        return os.getenv(key, default)


class Check:
    def show_fs_functions():
        targets = [File, Folder, Path, System, _Internal]

        for cls in targets:
            print(f"\n📦 {cls.__name__}")
            print("-" * 30)

            for name, obj in inspect.getmembers(cls):
                if inspect.isfunction(obj) or inspect.ismethod(obj):
                    if not name.startswith("_"):
                        print(f"🔹 {name}")

file, fl = File
folder, fd = Folder
path, p = path
system, sys, s = System
