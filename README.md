# Docketter

A CLI for managing docker-compose files

## What it does

In the developing context, one can use one or more docker-compose files (even with different names) and sometimes is complex to start/stop the dockers not knowing directly the paths of the files.

Docketter store in a config file (`~/.config/docketter/`) all your dockers with a easy to remember name or alias, making the process of manage docker-compose files more human acceptable.

### Prerequisites
This CLI was built with no dependencies in mind, so it only require Python 3.x. Tested with 3.5 =<.

If you want to run the tests, you need at least Python 3.6, because `mock` was included as part of `unittest` in that version.

### Installing

The installing only needs cloning this repository and add an alias in your `.bashrc` or `.zshrc` just like in the next example.
```
alias docketter='python3 ~/Git/Docketter/main.py'
```

Then you can refresh your shell and using it with the command `docketter`

### Running

Trying to make it the most user friendly possible, all the commands follows this structure: `docketter COMMAND SUBJECT`, where the subject can be one or more depending the command.

Try it with 

```
docketter help
```

The available commands are:
* `run`/`stop`
* `add-docker`/`add-alias`
* `remove-docker`/`remove-alias`
* `info-dockers`/`info-aliases`
* `help`

## Built With

* Python 3. No dependencies :)


## Version

1.0.0 

## Authors

* **Michel Llorens** - [Michotastico](https://github.com/Michotastico)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details
