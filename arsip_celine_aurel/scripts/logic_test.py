from pathlib import Path
from tempfile import TemporaryDirectory

from ziyan_bot.archive import ArchiveService, LocalFile
from ziyan_bot.db import Database
from ziyan_bot.parser import ProductDraft


class FakeGoogle:
    root_folder_id = "root"

    def __init__(self):
        self.n = 0

    def find_or_create_folder(self, name, parent_id):
        self.n += 1
        return {"id": f"folder-{self.n}", "webViewLink": f"https://drive/folder-{self.n}"}

    def create_folder(self, name, parent_id):
        self.n += 1
        return {"id": f"folder-{self.n}", "webViewLink": f"https://drive/folder-{self.n}"}

    def upload_file(self, path, parent_id, name=None):
        self.n += 1
        return {"id": f"file-{self.n}", "name": name, "webViewLink": f"https://drive/file-{self.n}"}

    def upsert_text(self, name, text, parent_id, mime_type="text/plain"):
        self.n += 1
        return {"id": f"meta-{self.n}", "name": name}

    def append_product(self, values):
        assert len(values) == 11

    def append_asset(self, values):
        assert len(values) == 7

    def append_log(self, event, product_id, details):
        pass

    def trash_file(self, file_id):
        pass

    def update_asset_status(self, asset_id, status):
        pass

    def update_product(self, product_id, values):
        assert len(values) == 11


def main():
    with TemporaryDirectory() as directory:
        db = Database(Path(directory) / "archive.db")
        service = ArchiveService(db, FakeGoogle())
        a = Path(directory) / "one.mp4"
        b = Path(directory) / "two.jpg"
        a.write_bytes(b"video")
        b.write_bytes(b"photo")
        draft = ProductDraft("Demo", "Description", "https://shopee.co.id/x", "https://tiktok.com/x", [])
        result = service.archive_new_product(draft, [LocalFile(a, "one.mp4", "video"), LocalFile(b, "two.jpg", "photo")])
        assert result["asset_count"] == 2
        product = db.get_product(result["product_id"])
        assert product is not None
        assert len(db.list_assets(result["product_id"])) == 2
        service.update_product(result["product_id"], draft)
        print("logic-ok")


if __name__ == "__main__":
    main()
