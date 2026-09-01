from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, sync_playwright


def first_visible(page: Page, selectors: list[str], timeout_ms: int = 5_000):
    deadline = time.time() + timeout_ms / 1000
    while time.time() < deadline:
        for selector in selectors:
            locator = page.locator(selector).first
            try:
                if locator.is_visible():
                    return locator
            except Exception:
                pass
        page.wait_for_timeout(250)
    raise RuntimeError(f"Tidak menemukan elemen UI yang terlihat: {selectors}")


def wait_for_manual_login(page: Page, expected_channel: str, seconds: int) -> None:
    print(
        "Jika browser menampilkan login, MFA, atau security challenge, "
        "pemilik akun harus menyelesaikannya secara manual. "
        "Script tidak mengisi password dan tidak melewati challenge."
    )
    deadline = time.time() + seconds
    while time.time() < deadline:
        if expected_channel in page.url and "studio.youtube.com" in page.url:
            return
        page.wait_for_timeout(1_000)
    raise RuntimeError(
        "Sesi tidak mencapai URL Studio dengan channel ID target. "
        f"URL terakhir: {page.url}"
    )


def click_create_and_upload(page: Page) -> None:
    create = first_visible(
        page,
        [
            'button:has-text("Create")',
            'button:has-text("Buat")',
            '[aria-label*="Create"]',
            '[aria-label*="Buat"]',
        ],
        timeout_ms=20_000,
    )
    create.click()
    upload_menu = first_visible(
        page,
        [
            'text=/Upload videos|Upload video|Upload video baru|Upload video baru/i',
            '[aria-label*="Upload"]',
        ],
        timeout_ms=10_000,
    )
    upload_menu.click()


def fill_metadata(page: Page, title: str, description: str) -> None:
    title_box = first_visible(
        page,
        [
            "ytcp-video-title #textbox",
            'textarea[aria-label*="Title"]',
            'input[aria-label*="Title"]',
            'textarea[aria-label*="Judul"]',
        ],
        timeout_ms=30_000,
    )
    title_box.fill(title)

    description_box = first_visible(
        page,
        [
            "ytcp-video-description #textbox",
            'textarea[aria-label*="Description"]',
            'textarea[aria-label*="Deskripsi"]',
        ],
        timeout_ms=10_000,
    )
    description_box.fill(description)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fallback upload YouTube Studio dengan profile persisten khusus."
    )
    parser.add_argument("--file", type=Path, required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", default="")
    parser.add_argument("--expected-channel", required=True)
    parser.add_argument(
        "--profile",
        type=Path,
        default=Path("profiles") / "youtube-celine",
        help="Direktori profile khusus; jangan arahkan ke profile Chrome utama.",
    )
    parser.add_argument("--login-wait-seconds", type=int, default=180)
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Tidak disarankan untuk bootstrap; challenge harus tetap ditangani manual.",
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Lanjutkan ke visibility/publish setelah review; default hanya upload dan isi metadata.",
    )
    args = parser.parse_args()

    if not args.file.is_file():
        raise SystemExit(f"File video tidak ditemukan: {args.file}")
    args.profile.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        context = playwright.chromium.launch_persistent_context(
            user_data_dir=str(args.profile),
            headless=args.headless,
            viewport={"width": 1440, "height": 1000},
            accept_downloads=False,
        )
        page = context.pages[0] if context.pages else context.new_page()
        studio_url = (
            f"https://studio.youtube.com/channel/{args.expected_channel}/videos/upload"
        )
        page.goto(studio_url, wait_until="domcontentloaded")

        if args.expected_channel not in page.url:
            wait_for_manual_login(page, args.expected_channel, args.login_wait_seconds)

        if "accounts.google.com" in page.url:
            raise RuntimeError(
                "Masih berada di Google login. Selesaikan login manual lalu jalankan ulang."
            )
        if "Service unavailable" in page.content():
            raise RuntimeError(
                "YouTube/Google menampilkan Service unavailable. Hentikan proses; "
                "jangan mencoba bypass atau mengulang agresif."
            )

        # The exact Studio UI is subject to change. Use accessible text/roles and fail closed.
        click_create_and_upload(page)
        with page.expect_file_chooser(timeout=20_000) as chooser_info:
            page.get_by_text(
                re.compile(r"Select files|Pilih file|Choose files", re.IGNORECASE)
            ).click()
        chooser_info.value.set_files(str(args.file.resolve()))

        fill_metadata(page, args.title, args.description)
        screenshot = args.profile / "last_upload_review.png"
        page.screenshot(path=str(screenshot), full_page=True)
        print(f"REVIEW_SCREENSHOT={screenshot}")

        if not args.publish:
            print(
                "DRY_RUN_OK: file dan metadata sudah diisi. "
                "Review browser secara manual; tidak ada publish otomatis."
            )
            context.close()
            return 0

        confirmation = input(
            "Ketik PUBLISH setelah memeriksa channel, title, privacy, dan audience: "
        ).strip()
        if confirmation != "PUBLISH":
            print("Dibatalkan tanpa publish.")
            context.close()
            return 0

        # These controls vary by Studio locale/version. Fail closed if not found.
        for _ in range(3):
            next_button = first_visible(
                page,
                [
                    'button:has-text("Next")',
                    'button:has-text("Berikutnya")',
                    '[aria-label*="Next"]',
                    '[aria-label*="Berikutnya"]',
                ],
                timeout_ms=30_000,
            )
            next_button.click()
            page.wait_for_timeout(1_000)

        visibility = first_visible(
            page,
            [
                'text=/Private|Pribadi/i',
                'label:has-text("Private")',
                'label:has-text("Pribadi")',
            ],
            timeout_ms=20_000,
        )
        visibility.click()
        publish_button = first_visible(
            page,
            [
                'button:has-text("Publish")',
                'button:has-text("Publikasikan")',
                'button:has-text("Save")',
                'button:has-text("Simpan")',
            ],
            timeout_ms=20_000,
        )
        publish_button.click()
        print("PUBLISH_CLICKED: verifikasi hasil di Studio secara manual.")
        context.close()
        return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, PlaywrightTimeoutError) as exc:
        print(f"UI_AUTOMATION_STOPPED: {exc}", file=sys.stderr)
        raise SystemExit(2)
