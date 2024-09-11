import os
import pandas as pd
import numpy as np
import shutil
import platform

def clear_console():
    # Clear the console depending on the operating system
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def print_intro():
    clear_console()
    print("Welcome to Mrs. Plotts, your personal Data Cleaning Assistant!\n")
    print("Now, dear, before we get started, remember: while I’ll do my best to assist you in tidying up your data, it’s always a good idea to review the results yourself, just to be sure everything is in tip-top shape.\n")
    print("And don’t forget, love, always keep a backup of your original file—better safe than sorry!\n")

def get_csv_location():
    location = input("Be a dear and enter the full path to your CSV file, won't you? ")
    if not os.path.isfile(location):
        print("File not found! Please provide a valid file path.")
        return get_csv_location()
    return location

def copy_csv_file(file_path):
    file_dir, file_name = os.path.split(file_path)
    new_file_name = file_name.replace('.csv', '_cleaned.csv')
    new_file_path = os.path.join(file_dir, new_file_name)
    shutil.copy(file_path, new_file_path)
    print(f"\nLovely! I’ve made a nice little copy of your file here: {new_file_path}\n")
    return new_file_path

def overview(df):
    clear_console()
    print("\nHere’s a quick look at your data, love:")
    print("-" * 30)
    print(f"Shape: {df.shape}")
    print(f"Data Types:\n{df.dtypes}")
    print(f"Missing Values:\n{df.isna().sum()}")
    print("-" * 30)
    print(df.head())
    print("-" * 30)

def ask_to_proceed():
    return input("\nWould you like to go through the cleaning steps together? (y/n): ").strip().lower() == 'y'

def rename_columns(df):
    clear_console()
    print("\nLet’s take a quick peek at the first few rows of your data, shall we?")
    print(df.head())
    
    # Offer to replace spaces with underscores and lowercase column names
    if input("\nWould you like me to tidy up those column names by replacing spaces with underscores and making everything lowercase? (y/n): ").strip().lower() == 'y':
        df.columns = df.columns.str.replace(' ', '_').str.lower()
        print("\nThere we are! Spaces replaced with underscores, and your column names are all lowercase now.\n")
        print(df.head())

    print("\nHere are your column names, all neat and tidy:")
    for i, col in enumerate(df.columns, 1):
        print(f"{i}. {col}")
    
    if input("\nWould you like to rename any of these columns individually, dear? (y/n): ").strip().lower() == 'y':
        while True:
            col_num = input("Enter the number of the column you’d like to rename, or ‘n’ if you're happy to proceed: ")
            if col_num.lower() == 'n':
                break
            try:
                col_num = int(col_num) - 1
                old_name = df.columns[col_num]
                new_name = input(f"And what shall we call '{old_name}' now? Go ahead and enter the new name: ")
                df.rename(columns={old_name: new_name}, inplace=True)
                clear_console()
                print(f"Lovely! '{old_name}' has been renamed to '{new_name}'.\n")
                print(df.head())  # Reprint data head and columns after each renaming
                print("\nHere are your updated column names:")
                for i, col in enumerate(df.columns, 1):
                    print(f"{i}. {col}")
            except (ValueError, IndexError):
                print("Invalid input, please try again.")
    return df

def handle_duplicates(df):
    clear_console()
    duplicate_rows = df[df.duplicated()]
    if duplicate_rows.empty:
        print("\nGood news! No duplicates here, everything is in order.")
    else:
        print(f"\nOh dear, it seems we’ve found {len(duplicate_rows)} duplicate rows.")
        print(duplicate_rows.head())
        choice = input("Would you like to (d)rop the duplicates, (k)eep all of them, or (s)how the duplicates?").strip().lower()
        if choice == 's':
            print(duplicate_rows)
            choice = input("Do you want to (d)rop or (k)eep duplicates? ").strip().lower()
        if choice == 'd':
            df = df.drop_duplicates()
            print(f"Duplicates have been dropped! Your data now looks like this: {df.shape}")
    return df

def handle_data_types(df):
    clear_console()
    print("\nData Types and Conversion Options:")
    for col in df.select_dtypes(include=['object', 'int64', 'float64']).columns:
        print(f"\n'{col}' - First 5 entries:\n{df[col].head()}")
        print(f"Current Data Type: {df[col].dtype}")
        if input(f"Would you like to change the data type of '{col}'? (y/n): ").strip().lower() == 'y':
            new_type = input(f"And what data type shall we convert {col} to? Something like **int**, **float**, or **datetime**, perhaps?").strip()
            try:
                df[col] = df[col].astype(new_type)
                print(f"Column '{col}' converted to {new_type}")
            except ValueError:
                print(f"Oh dear, we couldn’t convert {col} to {new_type}. Let’s try something else, shall we?")
    return df

def handle_categorical_data(df):
    clear_console()
    for col in df.select_dtypes(include=['object']).columns:  # Skip numeric columns
        unique_values = df[col].unique()
        num_unique = len(unique_values)
        print(f"\n'{col}' has {num_unique} unique categories.")
        
        user_choice = input(f"Would you like to (1) display the first 10 unique categories, (2) skip this column, or (3) proceed with renaming? Enter 1, 2, or 3: ").strip()

        if user_choice == '2':
            print(f"Skipping column '{col}'.")
            continue
        elif user_choice == '1':
            print(f"\nFirst 10 unique values in '{col}': {sorted(unique_values)[:10]}")
        
        if user_choice == '1' or user_choice == '3':
            if input(f"Do you want to proceed with renaming the categories in '{col}'? (y/n): ").strip().lower() == 'y':
                # Loop through the categories and offer renaming
                while True:
                    print(f"\nEnumerated categories in '{col}':")
                    for i, value in enumerate(sorted(unique_values), 1):
                        print(f"{i}. {value}")
                    
                    category_num = input("Enter the number of the category you'd like to rename, or 'n' to proceed: ").strip().lower()
                    if category_num == 'n':
                        break
                    try:
                        category_num = int(category_num) - 1
                        old_value = sorted(unique_values)[category_num]
                        new_value = input(f"Enter new value for '{old_value}': ").strip()
                        df[col] = df[col].replace(old_value, new_value)
                        unique_values = df[col].unique()  # Update unique values after renaming
                        print(f"'{old_value}' renamed to '{new_value}' in column '{col}'.")
                        
                        # Reprint the updated list of categories
                        print(f"\nUpdated categories in '{col}':")
                        for i, value in enumerate(sorted(unique_values), 1):
                            print(f"{i}. {value}")
                    except (ValueError, IndexError):
                        print("Invalid input. Please try again.")
    return df

def handle_missing_data(df):
    clear_console()
    print("\nHere’s an overview of the missing data in your dataset, love:")
    print(df.isna().sum())
    
    strategy = input("How would you like to handle the missing data? You can (d)rop rows, (i)mpute with the mean, median, or mode, or use (l)inear interpolation:").strip().lower()
    
    if strategy == 'd':
        df = df.dropna()
        print(f"Dropped rows with missing data. New shape: {df.shape}")
    
    elif strategy == 'i':
        for col in df.columns[df.isna().any()]:
            method = input(f"Choose imputation for '{col}' - (mean/median/mode): ").strip().lower()
            if method == 'mean':
                df[col].fillna(df[col].mean(), inplace=True)
            elif method == 'median':
                df[col].fillna(df[col].median(), inplace=True)
            elif method == 'mode':
                df[col].fillna(df[col].mode()[0], inplace=True)
            print(f"Missing values in '{col}' filled using {method}.")
    
    elif strategy == 'l':
        df = df.interpolate(method='linear')
        print("Missing values interpolated.")
    
    return df

def finalize_and_save(df, file_path):
    clear_console()
    print("\nHere’s a preview of your updated dataset, all neat and tidy:")
    print(df.head())
    
    if input("Would you like to apply all these lovely changes and save the cleaned dataset? (y/n): ").strip().lower() == 'y':
        df.to_csv(file_path, index=False)
        print(f"All done, love! Your cleaned file has been saved as: {file_path}")
    else:
        print("No changes have been saved, love. Perhaps another time.")

def main():
    print_intro()
    
    # Get CSV location and copy the file
    file_path = get_csv_location()
    new_file_path = copy_csv_file(file_path)
    
    # Load the data
    df = pd.read_csv(new_file_path)
    
    # Overview of the data
    overview(df)
    
    # Ask to proceed with cleaning
    if not ask_to_proceed():
        print("Exiting...")
        return
    
    # Cleaning steps
    df = rename_columns(df)
    df = handle_duplicates(df)
    df = handle_data_types(df)
    df = handle_categorical_data(df)
    df = handle_missing_data(df)
    
    # Finalize and save
    finalize_and_save(df, new_file_path)

if __name__ == '__main__':
    main()
