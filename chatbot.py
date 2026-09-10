from database import initialize_database, save_incident, list_incidents
import sqlite3


def main():

    try:
        initialize_database()
    except sqlite3.Error:
        print("Chatbot: The incident database could not be initialized.\n")
        return

    print("Simple Python Chatbot")
    print("Type 'quit' to exit.\n")

    while True:

        user_message_what_happened = get_user_input("What happened?")

        if user_message_what_happened.lower() == "quit":
            print("Chatbot: Goodbye!")
            break

        if user_message_what_happened.lower() == "list incidents":
            try:
                incidents = list_incidents()
            except sqlite3.Error:
                print("Chatbot: The incidents could not be retrieved.\n")
                continue
            if not incidents:
                print("Chatbot: No incidents found.")
            else:
                for incident in incidents:
                    print(f"\nIncident #{incident[0]}")
                    print(f"Description: {incident[1]}")
                    print(f"Affected Users: {incident[2]}")
                    print(f"Occurred At: {incident[3]}")
                    print(f"Created At: {incident[4]}")
                    print(f"Status: {incident[5]}")
                print()
            continue

        user_message_who_affected = get_user_input("Who was affected by the event")

        user_message_when = get_user_input("When did it happen?")

        incident = {
            "description": user_message_what_happened,
            "affected_users": user_message_who_affected,
            "occurred_at": user_message_when,
        }
        try:
            save_incident(
                incident["description"],
                incident["affected_users"],
                incident["occurred_at"],
            )

        except sqlite3.Error:
            print("Chatbot: The incident could not be saved. Please try again.\n")
            continue

        print(
            f"Chatbot: Thank you for the information. You said that '{incident['description']}' happened, affecting '{incident['affected_users']}' on '{incident['occurred_at']}'.\n"
        )


def get_user_input(question):

    print(f"Chatbot: {question}")
    user_input = input("You:").strip()

    while user_input == "":
        print("chatbot: Answer cannot be empty. Please try again.")
        print(f"Chatbot: {question}")
        user_input = input("You:").strip()

    return user_input


if __name__ == "__main__":
    main()
