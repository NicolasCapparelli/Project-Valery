from valerymain.responses import speechresponses
from valerymain.modules import module_windows

''' NOTE: All of the commands passed into here have their intent word taken out as it is redundant '''

# LOADS #
# installed_apps_path = "C:\\Users\\Nico\\PycharmProjects\\project-valery\\valerymain\\interpreters\\interdepends\\installed_apps.txt"
installed_apps_path = "interpreters\\interdepends\\programs"

SUB_INTENTS = {
    "open": {"paste": module_windows.paste_from_clipboard}
}

SEARCH_QUERY_TYPES = list(module_windows.GOOGLE_QUERY_TYPES.keys())

SEARCHABLE_SITES = list(module_windows.SEARCHABLE_WEBSITES.keys())

# INTERPRETERS #


# Updates a file with all the currently installed apps on the system
def update_apps_on_system():
    import os
    programs_directory_0 = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs"
    programs_directory_1 = "C:\\Users\\Nico\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs"

    program_name_list_0 = os.listdir(programs_directory_0)
    program_name_list_1 = os.listdir(programs_directory_1)

    # Open installed_apps.txt file and write
    with open(installed_apps_path, "r+") as file:

        # Delete all contents of the file
        file.seek(0)
        file.truncate()

        for program_name in program_name_list_0:

            clean_name = program_name.lower()
            file.write(clean_name)
            file.write("\n")

        for program_name in program_name_list_1:
            clean_name = program_name.lower()
            file.write(clean_name)
            file.write("\n")

        # Applications that can't found
        file.write("mail \n" + "calculator \n")


def main_windows_interpreter(intent_word, command, sub_intent):

    if sub_intent:

        # Split the command and the sub-command at the "and"
        command = command.split("and")

        # Remove whitespace from both
        command[0] = command[0].strip()
        command[1] = command[1].strip()

        # Run the main command
        response = INTENT_WORD_DICT[intent_word](command[0])

        # Run the sub-intent
        sub_intent_word = command[1].split(" ")[1]

        try:
            SUB_INTENTS[intent_word][sub_intent_word]()

        except KeyError:
            response = speechresponses.choose_random_response(speechresponses.subintent.SUB_INTENT_FAILED)

    else:
        # Run the main command
        response = INTENT_WORD_DICT[intent_word](command)

    return response


# Interprets the open command
def interpret_open(command):

    # Put every word in the command into a list
    command_split = command.split(" ")

    # The first word of the command, which should be the application
    application = command_split[0]

    # If the word where the name of the application is supposed to be is not "a" | "Open application" vs "Open a file"
    if application != "a" and application != "a ":

        app_exists = module_windows.open_application_v2(application)

        if app_exists:

            # Return SpeechResponse for Valery to say
            return speechresponses.choose_random_response(speechresponses.postaction.COMPLETE_ACTION)

        else:
            return speechresponses.choose_random_response(speechresponses.windows.APPLICATION_UNKNOWN)

    elif "file" in command or "document" in command:

        # Move the target index to the word after "in" or "with" if either of those are in the command
        if "in" in command_split or "with" in command_split:

            try:
                target_index = command_split.index("in") + 1

            except ValueError:
                target_index = command_split.index("with") + 1

        # If the user said new in the open command, such as: Open a new file
        elif "new" in command_split:

            # The supposed index of what it is the user is trying to open
            target_index = command_split.index("new") + 1

            # if the word at target index is "file" and the word "in" is in the command | Like: "Open a new file in Word"
            if (command_split[target_index] == "file" or command_split[target_index] == "document") and "in" in command_split[target_index]:
                target_index = command_split.index("in") + 1

            # If the word at target_index isn't "file" | Like in: "Open a new Word file"
            elif command_split[target_index] != "file" and command_split[target_index] != "document":

                # If the word at target index (the filetype) is in the FILE_TYPES dictionary keys
                if command_split[target_index].lower() in list(module_windows.FILE_TYPES.keys()):

                    # Open the new file in the correct application
                    module_windows.open_new_file(command_split[target_index].lower())
                    return speechresponses.choose_random_response(speechresponses.postaction.COMPLETE_ACTION)

                # If it isn't
                else:
                    return speechresponses.choose_random_response(speechresponses.windows.FILETYPE_UNKNOWN)

            else:
                return speechresponses.choose_random_response(speechresponses.postaction.INCOMPLETE_ACTION)

        else:
            return speechresponses.choose_random_response(speechresponses.postaction.INCOMPLETE_ACTION)

        target = command_split[target_index]

        if target.lower() in list(module_windows.FILE_TYPES.keys()):
            module_windows.open_new_file(target)
            return speechresponses.choose_random_response(speechresponses.postaction.COMPLETE_ACTION)

        else:
            return speechresponses.choose_random_response(speechresponses.windows.FILETYPE_UNKNOWN)

    # If the word after the intent word isn't a program or "a " (indicating wanting to open a new file)
    else:
        return speechresponses.choose_random_response(speechresponses.postaction.INCOMPLETE_ACTION)


def interpret_search(command):

    # Put every word in the command into a list
    command_split = command.split(" ")

    # If the first word in the command isn't "for"
    if command_split[0] != "for" and command_split[0] != "for ":

        if command_split[0] in SEARCHABLE_SITES and command_split[1] == "for":

            site = command_split[0]

            query = command.split("for")[1]

            module_windows.open_browser_site_search(site, query)
            return speechresponses.choose_random_response(speechresponses.postaction.COMPLETE_ACTION)

        else:
            # Search for what's in the command with a normal query type
            module_windows.open_browser_search(command, main_focus=False)
            return speechresponses.choose_random_response(speechresponses.postaction.COMPLETE_ACTION)

    else:
        command_split.remove("for")

        # If the first word, now that "for" is removed, is a query type, i.e. images, books, etc...
        if command_split[0] in SEARCH_QUERY_TYPES:

            # If the third word in the command is "of" or "about"
            if "of" in command_split[1] or "about" in command_split[1]:

                # Get the query type by getting the word after "for"
                query_type = command_split[0]

                # Get the actual query by splitting the command by "of" or "about" (whichever is in command_split[2]) and grabbing everything after the split
                query = command.split(command_split[1])[1].strip()

                # Use the parameters to run the search
                module_windows.open_browser_search(query=query, query_type=query_type, main_focus=True)

                return speechresponses.choose_random_response(speechresponses.postaction.COMPLETE_ACTION)

            else:
                return speechresponses.choose_random_response(speechresponses.postaction.INCOMPLETE_ACTION)

        else:

            # If there are no query types in the command
            if not any(word in SEARCH_QUERY_TYPES for word in command_split):

                # Get the actual query by removing "for" from it
                query = command.replace("for", "").strip()

                # Search with no particular query type
                module_windows.open_browser_search(query=query)
                return speechresponses.choose_random_response(speechresponses.postaction.COMPLETE_ACTION)

            # If the logic reaches here, it means that the command is something like: "Search for electrons in atoms in images"
            # This means that we have to build the query by iterating every word so that we can find the ACTUAL query type
            else:

                # The query that we will build
                query = ""
                query_type = None

                index_tracker = 0

                # Iterate over every word in the command, checking if it should be added to they query we're building
                for word in command_split:

                    # If the word being iterated over is not "in" and it is not a SEARCH_QUERY_TYPE
                    if word != "in" and word not in SEARCH_QUERY_TYPES:

                        # Add to the query with a space after
                        query += word + " "

                    elif word == "in":

                        # If the index of the iterated word + 2 is greater than or equal to the total length of the command
                        if index_tracker + 2 >= len(command_split):

                            # Since this is the last instance of the word "in", the query type will be the word after this iterated word
                            query_type = command_split[index_tracker + 1]

                            break

                        else:
                            query += word + " "

                    # If the word being iterated over is a SEARCH_QUERY_TYPES
                    elif word in SEARCH_QUERY_TYPES:

                        # If it's index + 1 is greater than or equal to the length of the command
                        if index_tracker + 1 >= len(command_split):

                            # The query type is the word being iterated over
                            query_type = command_split[index_tracker]

                            break

                        else:
                            query += word + " "

                    else:
                        print("Something really strange has happened, check interpreter_windows -> interpret_search query builder")
                        raise Exception

                    index_tracker += 1

                # Run the search using the query we built with the query_type we found
                module_windows.open_browser_search(query=query, query_type=query_type)
                return speechresponses.choose_random_response(speechresponses.postaction.COMPLETE_ACTION)

    # TODO: Figure out a good way to determine whether to return focus or not
    # TODO: Search in specific websites: "Search Youtube for..." "Search Amazon for..." SORT OF IMPLEMENTED
    # TODO: Flights to orlando
    # TODO: WIKI

INTENT_WORD_DICT = {"open": interpret_open,
                    "search": interpret_search}

# TODO: Save the last command done for context? Check discord for idea maybe?

if __name__ == "__main__":
    update_apps_on_system()
