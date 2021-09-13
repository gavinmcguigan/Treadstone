from pathlib import Path 

def launch():
    print("\nCurrent working directory")
    print(Path.cwd())

    print("\nAbsolute path to this file. ")
    print(Path(__file__).resolve())

    print("\nPath of directory where your script is located.")
    print(Path(__file__).resolve().parent)


if __name__ == "__main__":
    launch()