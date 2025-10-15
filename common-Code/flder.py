import os

def create_folders():
    # Ask user for folder names (comma separated)
    folders = input("Enter folder names separated by commas: ").split(",")

    for folder in folders:
        folder_name = folder.strip()  # remove extra spaces
        if folder_name:
            try:
                os.makedirs(folder_name, exist_ok=True)  # create folder if it doesn’t exist
                print(f"Folder '{folder_name}' created successfully ✅")
            except Exception as e:
                print(f"Error creating folder '{folder_name}': {e}")

if __name__ == "__main__":
    create_folders()
