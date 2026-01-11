from .config import Config
from pathlib import Path
import shutil
from .check_duplicate import CheckDuplicate


class Filter:
    @staticmethod
    def is_photo(file):
        return file.suffix.lower() in Config.PHOTO_EXTENSIONS

    @staticmethod
    def filter():
        if not Path(Config.OUTPUT_FOLDER).exists():
            Path(Config.OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)

        input_images = sorted(
            [
                f
                for f in sorted(Path(Config.INPUT_FOLDER).iterdir())
                if Filter.is_photo(f)
            ]
        )
        if not input_images:
            print("No images found in input folder.")
            return

        # First image always passes
        first_image = input_images[0]
        shutil.copy2(first_image, Path(Config.OUTPUT_FOLDER) / first_image.name)
        print(f"Copied {first_image.name} (first image)")

        # Process remaining
        for image in input_images[1:]:
            is_duplicate_found = False
            output_images = list(Path(Config.OUTPUT_FOLDER).iterdir())

            print(f"Checking {image.name}...")

            for output_img in output_images:
                # Skip non-image files in output if any (though we only put images there)
                if not Filter.is_photo(output_img):
                    continue

                response = CheckDuplicate.is_duplicate(image, output_img)
                if response.is_duplicate:
                    print(
                        f"  Duplicate of {output_img.name} (Reason: {response.reason}). Skipping."
                    )
                    is_duplicate_found = True
                    break

            if not is_duplicate_found:
                shutil.copy2(image, Path(Config.OUTPUT_FOLDER) / image.name)
                print(f"  No duplicate found. Copied {image.name}")
