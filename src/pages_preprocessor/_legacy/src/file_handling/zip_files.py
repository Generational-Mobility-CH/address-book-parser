import shutil


def zip_file(input_path, output_path):
    shutil.make_archive(f"{output_path}", "zip", f"{input_path}")
