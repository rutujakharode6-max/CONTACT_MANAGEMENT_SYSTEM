import json
import csv
import os
from datetime import datetime

# --- Validation Functions ---

def validate_name(name: str) -> bool:
    if not name.strip():
        return False
    return all(char.isalpha() or char.isspace() for char in name)

def validate_phone(phone: str) -> bool:
    if phone is None:
        return True
    return phone.isdigit() and len(phone) == 10

def validate_email(email: str) -> bool:
    if email is None:
        return True
    return '@' in email and '.' in email

# --- Core Operations ---

def add_contact(contacts: dict, name: str, phone: str, email: str, address: str):
    try:
        if name in contacts:
            raise ValueError(f"Contact '{name}' already exists.")
        
        if not validate_name(name):
            raise ValueError("Invalid name. Must contain only letters and spaces.")
        if not validate_phone(phone):
            raise ValueError("Invalid phone number. Must be exactly 10 digits.")
        if not validate_email(email):
            raise ValueError("Invalid email format.")
            
        contacts[name] = {
            'phone': phone,
            'email': email,
            'address': address,
            'category': 'Uncategorized'
        }
        print(f"Successfully added '{name}'.")
    except Exception as e:
        print(f"Error adding contact: {e}")

def search_contact(contacts: dict, search_term: str) -> list:
    try:
        search_term_lower = search_term.lower()
        results = []
        for name, info in contacts.items():
            if search_term_lower in name.lower():
                results.append((name, info))
        return results
    except Exception as e:
        print(f"Error searching contacts: {e}")
        return []

def search_by_phone(contacts: dict, phone: str) -> list:
    """Searches contacts by phone number."""
    results = []
    for name, info in contacts.items():
        if phone in info.get('phone', ''):
            results.append((name, info))
    return results

def update_contact(contacts: dict, name: str, phone: str = None, email: str = None, address: str = None):
    try:
        if name not in contacts:
            raise KeyError(f"Contact '{name}' not found.")
            
        if phone is not None and not validate_phone(phone):
            raise ValueError("Invalid phone number. Must be exactly 10 digits.")
        if email is not None and not validate_email(email):
            raise ValueError("Invalid email format.")
            
        if phone is not None:
            contacts[name]['phone'] = phone
        if email is not None:
            contacts[name]['email'] = email
        if address is not None:
            contacts[name]['address'] = address
            
        print(f"Successfully updated '{name}'.")
    except Exception as e:
        print(f"Error updating contact: {e}")

def delete_contact(contacts: dict, name: str):
    try:
        if name not in contacts:
            raise KeyError(f"Contact '{name}' not found.")
            
        confirmation = input(f"Are you sure you want to delete '{name}'? (y/n): ")
        if confirmation.lower() == 'y':
            del contacts[name]
            print(f"Successfully deleted '{name}'.")
        else:
            print("Deletion cancelled.")
    except Exception as e:
        print(f"Error deleting contact: {e}")

def categorize_contacts(contacts: dict, name: str, category: str):
    """Adds category tag to contacts."""
    if name not in contacts:
        print(f"Contact '{name}' not found.")
        return
    contacts[name]['category'] = category
    print(f"Successfully categorized '{name}' as '{category}'.")

def list_by_category(contacts: dict, category: str):
    """Displays contacts filtered by category."""
    results = []
    for name, info in contacts.items():
        if info.get('category', '').lower() == category.lower():
            results.append((name, info))
    
    display_search_results(results, f"Category: {category}")

def get_statistics(contacts: dict) -> dict:
    """Returns total contacts, contacts with/without email."""
    total = len(contacts)
    with_email = sum(1 for info in contacts.values() if info.get('email'))
    without_email = total - with_email
    return {
        'total': total,
        'with_email': with_email,
        'without_email': without_email
    }

def display_all(contacts: dict):
    try:
        if not contacts:
            print("No contacts found.")
            return
            
        print("-" * 90)
        print(f"{'Name':<20} | {'Phone':<12} | {'Email':<30} | {'Category':<15}")
        print("-" * 90)
        for name, info in contacts.items():
            cat = info.get('category', 'Uncategorized')
            print(f"{name:<20} | {info['phone']:<12} | {info['email']:<30} | {cat:<15}")
        print("-" * 90)
    except Exception as e:
        print(f"Error displaying contacts: {e}")

# --- File Operations ---

def save_to_file(contacts: dict, filename: str = 'contacts_data.json'):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(contacts, f, indent=4)
        print(f"Successfully saved contacts to '{filename}'.")
    except Exception as e:
        print(f"Error saving to file '{filename}': {e}")

def load_from_file(filename: str = 'contacts_data.json') -> dict:
    try:
        if not os.path.exists(filename):
            print(f"'{filename}' does not exist. Starting with an empty contact list.")
            return {}
        with open(filename, 'r', encoding='utf-8') as f:
            contacts = json.load(f)
        print(f"Successfully loaded contacts from '{filename}'.")
        return contacts
    except json.JSONDecodeError:
        print(f"Error: '{filename}' contains invalid JSON. Returning empty dictionary.")
        return {}
    except Exception as e:
        print(f"Error loading from file '{filename}': {e}")
        return {}

def backup_contacts(contacts: dict):
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"contacts_backup_{timestamp}.json"
        save_to_file(contacts, filename)
    except Exception as e:
        print(f"Error creating backup: {e}")

def export_to_csv(contacts: dict, filename: str = 'contacts.csv'):
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['Name', 'Phone', 'Email', 'Address', 'Category']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader()
            for name, info in contacts.items():
                writer.writerow({
                    'Name': name,
                    'Phone': info.get('phone', ''),
                    'Email': info.get('email', ''),
                    'Address': info.get('address', ''),
                    'Category': info.get('category', 'Uncategorized')
                })
        print(f"Successfully exported contacts to '{filename}'.")
    except Exception as e:
        print(f"Error exporting to CSV: {e}")

# --- UI Functions ---

def display_menu():
    print("\n" + "="*40)
    print("       CONTACT MANAGEMENT SYSTEM       ")
    print("="*40)
    print("1.  Add New Contact")
    print("2.  Search Contact (by Name)")
    print("3.  Search Contact (by Phone)")
    print("4.  Update Contact")
    print("5.  Delete Contact")
    print("6.  Categorize Contact")
    print("7.  List Contacts by Category")
    print("8.  Display All Contacts")
    print("9.  View Statistics")
    print("10. Save & Backup")
    print("11. Exit")
    print("="*40)

def get_menu_choice() -> int:
    while True:
        choice = input("Enter your choice (1-11): ").strip()
        if choice.isdigit():
            choice_num = int(choice)
            if 1 <= choice_num <= 11:
                return choice_num
        print("Invalid input. Please enter a number between 1 and 11.")

def get_contact_details() -> tuple:
    print("\n--- Enter Contact Details ---")
    while True:
        name = input("Enter Name: ").strip()
        if validate_name(name):
            break
        print("Invalid name. Must contain only letters and spaces, and cannot be empty.")
        
    while True:
        phone = input("Enter Phone (10 digits): ").strip()
        if validate_phone(phone):
            break
        print("Invalid phone number. Must be exactly 10 digits.")
        
    while True:
        email = input("Enter Email: ").strip()
        if validate_email(email):
            break
        print("Invalid email format. Must contain '@' and '.'.")
        
    address = input("Enter Address: ").strip()
    return name, phone, email, address

def display_contact(name: str, info: dict):
    print("\n--- Contact Details ---")
    print(f"Name:     {name}")
    print(f"Phone:    {info.get('phone', 'N/A')}")
    print(f"Email:    {info.get('email', 'N/A')}")
    print(f"Address:  {info.get('address', 'N/A')}")
    print(f"Category: {info.get('category', 'Uncategorized')}")
    print("-----------------------")

def display_search_results(results_list: list, title: str = "Search Results"):
    if not results_list:
        print(f"\nNo contacts found for {title.lower()}.")
        return
        
    print(f"\n--- {title} ({len(results_list)} found) ---")
    for idx, (name, info) in enumerate(results_list, start=1):
        print(f"\n[{idx}] {name} ({info.get('category', 'Uncategorized')})")
        print(f"    Phone:   {info.get('phone', '')}")
        print(f"    Email:   {info.get('email', '')}")
        print(f"    Address: {info.get('address', '')}")

# --- Main Program Loop ---

def main():
    print("Initializing Contact Management System...")
    contacts_db = load_from_file()
    
    try:
        while True:
            display_menu()
            choice = get_menu_choice()
            
            if choice == 1:
                print("\n[Add New Contact]")
                name, phone, email, address = get_contact_details()
                add_contact(contacts_db, name, phone, email, address)
                if name in contacts_db:
                    display_contact(name, contacts_db[name])
                    
            elif choice == 2:
                print("\n[Search Contact by Name]")
                term = input("Enter name to search: ").strip()
                results = search_contact(contacts_db, term)
                display_search_results(results)
                
            elif choice == 3:
                print("\n[Search Contact by Phone]")
                phone = input("Enter phone number to search: ").strip()
                results = search_by_phone(contacts_db, phone)
                display_search_results(results, "Phone Search Results")
                
            elif choice == 4:
                print("\n[Update Contact]")
                name = input("Enter exact name of contact to update: ").strip()
                if name in contacts_db:
                    print("Leave field blank to keep current value.")
                    
                    phone = input(f"Enter new phone [{contacts_db[name]['phone']}]: ").strip()
                    if phone == "": phone = None
                    
                    email = input(f"Enter new email [{contacts_db[name]['email']}]: ").strip()
                    if email == "": email = None
                    
                    address = input(f"Enter new address [{contacts_db[name]['address']}]: ").strip()
                    if address == "": address = None
                    
                    update_contact(contacts_db, name, phone, email, address)
                    if name in contacts_db:
                        display_contact(name, contacts_db[name])
                else:
                    print(f"Contact '{name}' not found.")
                    
            elif choice == 5:
                print("\n[Delete Contact]")
                name = input("Enter exact name of contact to delete: ").strip()
                delete_contact(contacts_db, name)
                
            elif choice == 6:
                print("\n[Categorize Contact]")
                name = input("Enter exact name of contact: ").strip()
                if name in contacts_db:
                    category = input("Enter category (e.g., Family, Work, Friend): ").strip()
                    if category:
                        categorize_contacts(contacts_db, name, category)
                else:
                    print(f"Contact '{name}' not found.")
                    
            elif choice == 7:
                print("\n[List by Category]")
                category = input("Enter category to list: ").strip()
                list_by_category(contacts_db, category)
                
            elif choice == 8:
                print("\n[Display All Contacts]")
                display_all(contacts_db)
                
            elif choice == 9:
                print("\n[View Statistics]")
                stats = get_statistics(contacts_db)
                print(f"Total Contacts:         {stats['total']}")
                print(f"Contacts with Email:    {stats['with_email']}")
                print(f"Contacts without Email: {stats['without_email']}")
                
            elif choice == 10:
                print("\n[Save & Backup]")
                save_to_file(contacts_db)
                backup_contacts(contacts_db)
                export_to_csv(contacts_db)
                
            elif choice == 11:
                print("\nSaving before exit...")
                save_to_file(contacts_db)
                print("Exiting Contact Management System. Goodbye!")
                break
                
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user.")
        print("Auto-saving contacts before exiting...")
        save_to_file(contacts_db)
        print("Goodbye!")
        
if __name__ == "__main__":
    main()
