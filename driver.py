
# File: driver.py
# This script demonstrates how to manipulate a matrix representation of activities
# Import necessary libraries
import pandas as pd
from remove_activity import remove_activity_function
from turn_direct_into_indirect_relationship import remove_direct_relationship_function
from remove_all_relationships import remove_all_relationships_function
from turn_exclusive_into_direct_relationship import exclusive_to_direct_relationship_function
from generate_declarative_constraints import generate_declarative_constraints_function
from add_true_exclusion_relationships import add_true_exclusion_relationships_function
import sys
import ast
import os

if __name__ == "__main__":
    

    """if len(sys.argv) != 2:
        print("Usage: python driver.py <txt_file_path>")
        sys.exit(1)
    
    txt_path = sys.argv[1]
    
    
    matrix=[['','CPRI','CPOI','ROC','CP','CQ','RGR','RIR','VCI','RPB','CI'],
            ['CPRI', '-', '→', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['CPOI', '←', '-', '→', '→', '→', '→', '→', '→', '-', '-'],
            ['ROC', '-', '←', '-', '-', '→', '→', '→', '→', '-', '-'],
            ['CP', '-', '←', '-', '-', '→', '→', '→', '→', '-', '-'],
            ['CQ', '-', '←', '←', '←', '-', '→', '→', '||', '-', '-'],
            ['RGR', '-', '←', '←', '←', '←', '-', '||', '||', '→', '→'],
            ['RIR', '-', '←', '←', '←', '←', '||', '-', '||', '→', '→'],
            ['VCI', '-', '←', '←', '←', '||', '||', '||', '-', '→', '→'],
            ['RPB', '-', '-', '-', '-', '-', '←', '←', '←', '-', '→'],
            ['CI', '-', '-', '-', '-', '-','←', '←', '←', '←','-']]"""

    if len(sys.argv) != 2:
        print("Usage: python driver.py <txt_file_path>")
        sys.exit(1)

    txt_path = sys.argv[1]

    # Check if file exists
    if not os.path.exists(txt_path):
        print(f"File not found: {txt_path}")
        sys.exit(1)

    # Read and parse the list from file
    with open(txt_path, 'r', encoding='utf-8') as file:
        try:
            content = file.read()
            matrix = ast.literal_eval(content)
        except Exception as e:
            print("Failed to parse the list from the file.")
            print("Error:", e)
            sys.exit(1)

    print("\nMatrix Representation:")
    df = pd.DataFrame(matrix[1:], columns=matrix[0])
    # Set first column as index
    df = df.set_index('')
    # Remove the name of the index
    df.index.name = None
    # Now you have a clean DataFrame
    # Add true exclusion relationships to the Matrix
    df=add_true_exclusion_relationships_function(df)
    print(df)
    # Store the original DataFrame for reference
    df_original = df.copy()
    while True:
        print("\nChoose a relaxation operation:")
        print("1. Remove Activity")
        print("2. Remove All Relationships Between Two Activities")
        print("3. Turn Exclusive (#) into Direct Relationship (→)")
        print("4. Turn Direct (→) into Indirect Relationship (≺)")
        print("5. Show Matrix")
        print("6. Reset to Original Matrix")
        print("7. Generate Declarative Constraints")
        #print("8. Evaluate")
        print("0. Exit")
        choice = input("Enter your choice (0-7): ")

        if choice == "1": #Remove activity
            activity = input("Enter activity to remove: ")
            df = remove_activity_function(df, activity)
            print(df)
        elif choice == "2": #Remove all relationships/activities between two activities
            from_activity = input("Enter from_activity: ")
            to_activity = input("Enter to_activity: ")
            df = remove_all_relationships_function(df, from_activity, to_activity)
            print(df)
        elif choice == "3": #Turn Exclusive (#) into Direct Relationship (→)
            from_activity = input("Enter from_activity: ")
            to_activity = input("Enter to_activity: ")
            df=exclusive_to_direct_relationship_function(df, from_activity, to_activity)
            print(df)
        elif choice == "4": #Turn Direct (→) into Indirect Relationship (≺)
            from_activity = input("Enter from_activity: ")
            to_activity = input("Enter to_activity: ")
            df = remove_direct_relationship_function(df, from_activity, to_activity)
            print(df)
        elif choice == "5": # Show Matrix
            print(df)
        elif choice == "6": # Reset to Original Matrix
            print("Reset to Original Matrix:")
            df= df_original.copy()
            df.index.name = None  # Reset index name
            print(df)
        elif choice == "7": # Generate Declarative Constraints
            print("Generating Declarative Constraints...")
            generate_declarative_constraints_function(df)
        #elif choice=="8":
            #print("Evaluate")
            #generate_declarative_constraints_function(df)
        elif choice == "0":
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please try again.") 






