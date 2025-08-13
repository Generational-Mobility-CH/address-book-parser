from modules.address_books.pages_downloader.src.constants.paths import PDF_OUTPUT_PATH
from modules.address_books.pages_downloader.src.create_folders import create_folders


def main():
    create_folders()
    # TODO: Put pipeline steps into main function


if __name__ == "__main__":
    PDF_OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

    main()
