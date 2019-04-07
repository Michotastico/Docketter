import sys

from docketter import Docketter


class CLIException(Exception):
    pass


def help_message():
    message = """
    NAME
        docketter - manage multiple docker-compose file.
        
    SYNOPSYS
        docketter COMMAND SUBJECT
        
    COMMANDS
        run 
            - Start the docker compose name/alias defined as SUBJECT
        stop 
            - Stop the docker compose name/alias defined as SUBJECT.
        
        add-docker 
            - Add a new docker-compose file. 
              The SUBJECT are two required string and one optional:
                - NAME PATH ALIAS.
        add-alias 
            - Add a new alias for a stored docker-compose using his tag.
              The SUBJECT are two required string: 
                - NAME ALIAS
        
        remove-docker 
            - Remove a stored docker-compose using his name/alias. 
              The SUBJECT is the name/alias.
        remove-alias 
            - Remove an alias of a docker-compose. 
            The SUBJECT is the alias.
        
        info-dockers 
            - Display the information of the stored dockers.
        info-aliases 
            - Display the information of the stored aliases.
        
        help 
            - Display this information.
        
        """
    print(message)


def display_information(title, information):
    message = """
    {}
        {}
    """

    strings_to_be_joined = list()
    for info in information:
        name = info.get('name')
        alias = info.get('alias')
        docker = info.get('docker')

        if (name is None and alias is None) or docker is None:
            continue

        tag = name if name is not None else alias

        strings_to_be_joined.append(
            '-> {} \n                - {}'.format(tag, docker)
        )

    parsed_string = '\n        '.join(strings_to_be_joined)

    print(
        message.format(title, parsed_string)
    )


def raise_error(message=None):
    base_error = "[ERROR] Please use `help` to check the use of Docketter"
    if message is not None:
        base_error += '\n{}'.format(message)

    raise CLIException(base_error)


def check_arguments_size(arguments, length):
    received_arguments_length = len(arguments)
    if received_arguments_length < length:
        raise_error(
            "Expected {} arguments, received {}".format(
                length, received_arguments_length
            )
        )


def run(arguments):
    check_arguments_size(arguments, 1)

    action = arguments[0].lower()

    commands = [
        'run', 'stop', 'add-docker', 'add-alias',
        'remove-docker', 'remove-alias', 'help',
        'info-dockers', 'info-aliases'
    ]

    if action not in commands:
        raise_error()

    docketter = Docketter()

    if action in ['run']:
        check_arguments_size(arguments, 2)
        subject = arguments[1]
        docketter.run_docker(subject)

    elif action in ['stop']:
        check_arguments_size(arguments, 2)
        subject = arguments[1]
        docketter.stop_docker(subject)

    elif action in ['add-docker']:
        check_arguments_size(arguments, 2)
        subject_name = arguments[1]
        subject_path = arguments[2]
        subject_alias = arguments[3] if len(arguments) > 3 else None
        docketter.add_docker(subject_name, subject_path, subject_alias)

    elif action in ['add-alias']:
        check_arguments_size(arguments, 2)
        subject_name = arguments[1]
        subject_alias = arguments[2]
        docketter.add_alias(subject_name, subject_alias)

    elif action in ['remove-docker']:
        check_arguments_size(arguments, 1)
        subject = arguments[1]
        docketter.remove_docker(subject)

    elif action in ['remove-alias']:
        check_arguments_size(arguments, 1)
        subject = arguments[1]
        docketter.remove_alias(subject)

    elif action in ['info-dockers']:
        check_arguments_size(arguments, 0)
        information = docketter.get_dockers()
        display_information('Dockers', information)

    elif action in ['info-aliases']:
        check_arguments_size(arguments, 0)
        information = docketter.get_aliases()
        display_information('Aliases', information)

    elif action in ['help']:
        help_message()


if __name__ == "__main__":
    try:
        run(sys.argv[1:])
    except CLIException as error:
        print(error)
