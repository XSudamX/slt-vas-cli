import argparse
from sltcli.summary import main as summary_main
from sltcli.report import main as report_main
from sltcli.utils import banner


def menu():
    """Prints out the main menu for the program, and handles user input"""

    def option_1():
        summary_main()

    def option_2():
        report_main()

    while True:
        print("1. View current month summary")
        print("2. View previous month consolidated detailed report")
        choice = input("Enter your choice (1 or 2): ")
        if not choice:
            print("Invalid input. Please enter a value.")
            continue
        try:
            choice = int(choice)
            if choice == 1:
                option_1()
                break
            elif choice == 2:
                option_2()
                break
            else:
                print("Invalid input. Please enter 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
        except OverflowError:
            print("Invalid input. The value is too large.")


def main():
    parser = argparse.ArgumentParser(
        description="CLI Utility for SLT Value added Services"
    )

    # Arguments
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print the summary directly without CLI menu",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate the report directly without CLI menu",
    )

    args = parser.parse_args()

    # Call the appropriate function based on the arguments
    print(banner)
    if args.summary:
        summary_main()
    elif args.report:
        report_main()
    else:
        menu()


if __name__ == "__main__":
    main()
