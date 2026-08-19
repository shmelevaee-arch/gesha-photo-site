# -*- coding: utf-8 -*-
"""Скачивает оригиналы фото из публичной папки Яндекс.Диска в _raw/<категория>/."""
import json, os, sys, urllib.parse, urllib.request

PUBLIC_KEY = "https://disk.yandex.ru/d/2yPGJBq6wZ5iFQ"
API = "https://cloud-api.yandex.net/v1/disk/public/resources"
ROOT = os.path.join(os.path.dirname(__file__), "..", "_raw")

# папка на диске -> папка у нас (латиницей, чтобы не мучиться с путями и URL)
FOLDERS = {"/Лавстори": "lovestory", "/Персональные": "personal", "/Семья": "family"}


def api(path):
    url = API + "?" + urllib.parse.urlencode({"public_key": PUBLIC_KEY, "path": path, "limit": 300})
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)


def fetch(href, dest, expected, attempts=5):
    """Качает файл чанками. Яндекс.Диск иногда рвёт соединение (IncompleteRead) —
    поэтому несколько попыток и проверка итогового размера."""
    last = None
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(href, timeout=120) as r, open(dest, "wb") as f:
                while True:
                    chunk = r.read(1 << 20)
                    if not chunk:
                        break
                    f.write(chunk)
            size = os.path.getsize(dest)
            if expected is None or size == expected:
                return size
            last = f"размер {size} вместо {expected}"
        except Exception as e:
            last = repr(e)
        print(f"    попытка {attempt} не удалась: {last}", flush=True)
    raise RuntimeError(f"не смог скачать {dest}: {last}")


def main():
    total_bytes = 0
    for remote, local in FOLDERS.items():
        data = api(remote)
        items = [i for i in data["_embedded"]["items"] if i["type"] == "file"]
        target = os.path.join(ROOT, local)
        os.makedirs(target, exist_ok=True)
        print(f"== {remote} -> _raw/{local}: {len(items)} файлов", flush=True)
        for n, item in enumerate(sorted(items, key=lambda x: x["name"]), 1):
            dest = os.path.join(target, item["name"])
            if os.path.exists(dest) and os.path.getsize(dest) == item.get("size", -1):
                print(f"  [{n}] {item['name']} — уже скачан", flush=True)
                continue
            size = fetch(item["file"], dest, item.get("size"))
            total_bytes += size
            print(f"  [{n}] {item['name']} — {size/1024/1024:.1f} МБ", flush=True)
    print(f"Готово. Скачано {total_bytes/1024/1024:.1f} МБ", flush=True)


if __name__ == "__main__":
    sys.exit(main())
