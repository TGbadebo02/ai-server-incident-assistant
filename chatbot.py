from database import initialize_database, save_incident


def main():
    initialize_database()

    print("Simple Python Chatbot")
    print("Type 'quit' to exit.\n")

    while True:

        user_message_what_happened = get_user_input("What happened?")
        if user_message_what_happened.lower() == "quit":
            print("Chatbot: Goodbye!")
            break

        user_message_who_affected = get_user_input("Who was affected by the event")

        user_message_when = get_user_input("When did it happen?")

        incident = {
            "description": user_message_what_happened,
            "affected_users": user_message_who_affected,
            "occurred_at": user_message_when,
        }

        save_incident(
            incident["description"], incident["affected_users"], incident["occurred_at"]
        )

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
