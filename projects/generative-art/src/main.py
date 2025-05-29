import os
import uuid
import click
import random
import logging

from PIL import Image
from tqdm import tqdm
from datetime import datetime
from samila import GenerativeImage, GenerateMode, Projection, Marker
from samila.params import VALID_COLORS
from models.formula import Formula

LOG_FILE = "app.log"
OUTPUT_FOLDER = "output"
DATA_FOLDER = f"{OUTPUT_FOLDER}/data"
IMAGES_FOLDER = f"{OUTPUT_FOLDER}/images"

COLORS = VALID_COLORS.copy()
COLORS.remove("black")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE, mode="w"), logging.StreamHandler()],
)
logger = logging.getLogger("generative_art")


@click.group()
def cli():
    """
    Command-line interface for generating generative art.
    """
    pass


def log_metadata(metadata: dict) -> None:
    """
    Log metadata information about generated art.

    This function iterates through a dictionary of metadata, where each key is
    a UUID representing a generated image, and each value is the corresponding
    seed used for generation. It logs this information using the configured logger.

    Args:
        metadata (dict): A dictionary containing UUIDs as keys and seeds as values.

    Returns:
        None
    """
    for k, v in metadata.items():
        logger.info(f"UUID: {k} - Seed: {v}")


def get_file_modication_time(file_path: str) -> datetime:
    """
    Get the last modification date and time of a file.

    This function retrieves the last modified timestamp of the specified file
    and converts it to a human-readable datetime object.

    Args:
        file_path (str): The path to the file.

    Returns:
        datetime: The last modification date and time of the file.
    """
    mod_time = os.path.getmtime(file_path)
    readable_time = datetime.fromtimestamp(mod_time)
    return readable_time


def create_folders() -> None:
    """
    Create the output folder structure for storing generated art.

    This function creates the following folder structure:
    - 'output' folder
    - 'output/data' folder for storing generated data files
    - 'output/images' folder for storing generated image files

    Returns:
        None
    """
    # create output folder
    if os.path.isdir(OUTPUT_FOLDER) is False:
        os.makedirs(OUTPUT_FOLDER)
    if not os.path.isdir(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
    if not os.path.isdir(IMAGES_FOLDER):
        os.makedirs(IMAGES_FOLDER)


@cli.command()
@click.option(
    "--single-color",
    "-s",
    default=False,
    is_flag=True,
    show_default=True,
    help="Use a single color for the art.",
)
@click.option(
    "--total",
    "-t",
    default=1,
    show_default=True,
    help="Total number of images to generate.",
)
@click.option(
    "--using-formula",
    "-f",
    default=False,
    is_flag=True,
    show_default=True,
    help="Use custom formulas for generating art.",
)
def generate_art(single_color: bool, total: int, using_formula: bool) -> None:
    """
    Generate generative art images and save them along with their metadata.

    This function creates generative art images using the `samila` library.
    It generates a specified number of images, saves the image files and their
    corresponding data files, and logs metadata about the generated images.

    Args:
        single_color (bool, optional): If True, use a single color for the art. Defaults to False.
        total (int, optional): Total number of images to generate. Defaults to 5.
        using_formula (bool, optional): If True, use custom formulas for generating art. Defaults to False.

    Returns:
        None
    """
    create_folders()

    formula = Formula()
    metadata = {}

    for _ in tqdm(
        range(total), desc=f"Generating {total} Art", colour="green", ascii=" #"
    ):
        try:
            image_uuid = uuid.uuid4()
            data_path = f"{DATA_FOLDER}/{image_uuid}.json"
            image_path = f"{IMAGES_FOLDER}/{image_uuid}.png"

            g = GenerativeImage(
                function1=formula.calc_formula2_value if using_formula else None,
                function2=formula.calc_formula1_value if using_formula else None,
            )
            g.generate(
                start=-5, step=0.01, stop=3, mode=random.choice(list(GenerateMode))
            )
            g.plot(
                projection=random.choice(list(Projection)),
                color=(
                    COLORS[random.randrange(0, len(COLORS))]
                    if single_color
                    else g.data2
                ),
                cmap=[] if single_color else [random.choice(COLORS) for _ in range(10)],
                bgcolor="black",
                alpha=0.6,
                # marker=marker_mode,
                # spot_size=0.5,
            )
            # g.save_data(file_adr=data_path)
            g.save_image(image_path, depth=5)  # more depth more higher resolution

            # convert to webp format
            image_webp_path = image_path.replace(".png", ".webp")
            image = Image.open(image_path)
            image = image.convert("RGB")
            image.save(image_webp_path, "webp")

            os.remove(image_path)  # remove original png file
            metadata[str(image_uuid)] = g.seed
        except Exception as e:
            logger.error(f"Error generating image: {e}")

    log_metadata(metadata)


@cli.command()
@click.option(
    "--filename",
    "-f",
    required=True,
    multiple=True,
    help="The names of the files to delete (without folder path and file extension).",
)
def delete_art(filename: tuple) -> None:
    """
    Delete generated art image and its metadata.

    Args:
        filename (tuple): The names of the file to delete (without folder path and file extension).

    Returns:
        None
    """
    for file in filename:
        try:
            # data_file_path = os.path.join(DATA_FOLDER, f"{file}.json")
            image_file_path = os.path.join(IMAGES_FOLDER, f"{file}.webp")

            # Delete from data folder
            # if os.path.exists(data_file_path):
            #     os.remove(data_file_path)
            #     logger.info(f"Deleted data file: {data_file_path}")
            # else:
            #     logger.warning(f"Data file not found: {data_file_path}")

            # Delete image file
            if os.path.exists(image_file_path):
                os.remove(image_file_path)
                logger.info(f"Deleted image file: {image_file_path}")
            else:
                logger.warning(f"Image file not found: {image_file_path}")
        except:
            logger.error(f"Error deleting file: '{file}'")


@cli.command()
@click.option(
    "--display-latest",
    "-d",
    required=False,
    default=True,
    show_default=True,
    help="Display the latest generated image in the README.",
)
def generate_readme(display_latest: bool) -> None:
    """
    Generate a README file with a grid layout of generated images.

    This function collects all image files from the output/images directory,
    generates an HTML snippet for a grid layout, and appends it to the README.md file.
    """
    # Output file (README.md)
    readme_file = "README.md"

    # Collect all image files
    image_files = [
        f
        for f in os.listdir(IMAGES_FOLDER)
        if os.path.isfile(os.path.join(IMAGES_FOLDER, f))
    ]

    if display_latest:
        latest_image = max(
            image_files,
            key=lambda f: get_file_modication_time(os.path.join(IMAGES_FOLDER, f)),
        )
        image_files = [latest_image]
        html_snippet = '<div align="center">\n'
        html_snippet += f'  <img src="{IMAGES_FOLDER}/{latest_image}" alt="{latest_image}" width="350">\n'
        html_snippet += "</div>\n"
    else:
        # Generate HTML for grid layout
        html_snippet = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px;" align="center">\n'
        for image in image_files:
            html_snippet += (
                f'  <img src="{IMAGES_FOLDER}/{image}" alt="{image}" width="150">\n'
            )
        html_snippet += "</div>\n"

    with open(readme_file, "w") as readme:
        readme.write("\n<h1 align='center'>Generative Art</h1>\n")
        readme.write(html_snippet)

    logger.info(f"Added {len(image_files)} images to the grid layout in {readme_file}.")


def main():
    cli()


if __name__ == "__main__":
    main()
