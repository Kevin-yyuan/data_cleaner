import click
import pandas as pd


@click.command()
@click.option('--input', required=True, help='Path to the messy input CSV file.')
@click.option('--output', required=True, help='Path to save the clean output CSV file.')
def clean_data(input, output):
    """
    This script cleans logistics data from a CSV file.
    """
    print(f"Loading data from {input}...")
    df = pd.read_csv(input)

    print("Initial data:")
    print(df.head())
    print(df.info())

    # --- Cleaning functions will be called here ---

    # Save the cleaned data
    # df.to_csv(output, index=False)
    # print(f"\nClean data saved to {output}")


if __name__ == '__main__':
    clean_data()
