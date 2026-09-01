from pathlib import Path
from tempfile import TemporaryDirectory

from ziyan_bot.db import Database
from ziyan_bot.parser import parse_caption


def main() -> None:
    draft = parse_caption(
        "Nama produk: Lampu tidur minimalis\n"
        "Deskripsi: Tiga tingkat warna untuk kamar.\n"
        "Shopee: https://shopee.co.id/example\n"
        "TikTok: https://vt.tiktok.com/example"
    )
    assert draft.title == "Lampu tidur minimalis"
    assert draft.shopee_url == "https://shopee.co.id/example"
    assert draft.tiktok_url == "https://vt.tiktok.com/example"
    with TemporaryDirectory() as directory:
        db = Database(Path(directory) / "test.db")
        assert not db.message_seen(1, 2)
        db.mark_message(1, 2)
        assert db.message_seen(1, 2)
    print("smoke-ok")


if __name__ == "__main__":
    main()
