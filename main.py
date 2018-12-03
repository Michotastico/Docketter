import sys


def help_command():
    text = """
    NAME
        docketter - manage multiple docker-compose file.
        
    SYNOPSYS
        docketter COMMAND SUBJECT
        
    COMMANDS
        run - Start the docker compose name/alias defined as SUBJECT
        stop - Stop the docker compose name/alias defined as SUBJECT.
        
        add-docker - Add a new docker-compose file. The SUBJECT are two required string and one optional in the following order: NAME PATH ALIAS.
        add-alias - Add a new alias for a stored docker-compose using his name/alias. The SUBJECT are t wo required string in the following order: NAME ALIAS
        
        remove-docker - Remove a stored docker-compose using his name/alias. The SUBJECT is the name/alias.
        remove-alias - Remove an alias of a docker-compose. The SUBJECT is the alias.
        
        help - Display this information.
        
        """
    print(text)


def run(arguments):
    if len(arguments) < 1:
        help_command()
        return
    action = arguments[0]

    if action in ['help', 'HELP']:
        help_command()
        return


if __name__ == "__main__":
    run(sys.argv[1:])
