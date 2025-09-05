import click
import pandas as pd

# ---------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------


def remove_duplicates(df):
    """Removes duplicate rows from the dataframe."""
    return df.drop_duplicates()


def clean_text(df, columns):
    """Strips whitespace and converts text columns to a consistent case"""
    for col in columns:
        df[col] = df[col].astype(str).str.strip().str.upper()
    return df


def standardize_dates(df, columns):
    """Converts specified columns to a standard YYYY-MM-DD date format."""
    for col in columns:
        df[col] = pd.to_datetime(df[col], errors='coerce').dt.date
    return df


def clean_cost(df, column):
    """Removes currency symbols and commas, converting the column to a numeric type."""
    df[column] = df[column].astype(str).replace(
        {'\$': '', ',': ''}, regex=True)
    df[column] = pd.to_numeric(df[column], errors='coerce')
    return df

# ---------------------------------------------------
# MAIN FUNCTION
# ---------------------------------------------------


@click.command()
@click.option('--input', required=True, help='Path to the messy input CSV file.')
@click.option('--output', required=True, help='Path to save the clean output CSV file.')
def clean_data(input, output):
    """
    This script cleans logistics data from a CSV file.
    """
    print(f"Loading data from {input}...")
    df = pd.read_csv(input)

    print("\n--- Starting Cleaning Process ---")

    # 1. Remove duplicate rows
    initial_rows = len(df)
    df_clean = remove_duplicates(df)
    print(f"Removed {initial_rows - len(df_clean)} duplicate rows.")

    # 2. Clean text fields
    text_cols = ['origin_port', 'destination_port', 'carrier', 'status']
    df_clean = clean_text(df_clean, text_cols)
    print(f"Cleaned and standardized text columns: {text_cols}")

    # 3. Standardize date formats
    date_cols = ['departure_date', 'arrival_date']
    df_clean = standardize_dates(df_clean, date_cols)
    print(f"Standardized date columns: {date_cols}")

    # 4. Clean the cost column
    df_clean = clean_cost(df_clean, 'cost')
    print("Cleaned cost column to numeric format.")

    # 5. Handle missing values (simple strategy: drop rows with any missing data)
    initial_rows = len(df_clean)
    df_clean = df_clean.dropna()
    print(f"Dropped {initial_rows - len(df_clean)} rows with missing values.")

    print("\n--- Cleaning Complete ---")
    print("\nFinal clean data sample:")
    print(df_clean.head())

    # Save the cleaned data
    df_clean.to_csv(output, index=False)
    print(f"\n✅ Success! Clean data saved to {output}")
    print(f"Total rows in clean file: {len(df_clean)}")


if __name__ == '__main__':
    clean_data()
