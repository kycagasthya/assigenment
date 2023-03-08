import argparse

from utils.generation import get_latest_file


def run(bq_dir: str = None):
    """
    Print latest schema file name

    :param bq_dir: dir with BQ schema files
    """
    latest_file_name = get_latest_file(bq_dir)
    return latest_file_name if latest_file_name else None


if __name__ == "__main__":
    # Parse input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--bq_dir",
        required=True,
        help="Directory with BQ schema files",
    )
    args, other = parser.parse_known_args()

    print(run(args.bq_dir))
