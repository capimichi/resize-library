import click

from resizelibrary.command.resize_folder_command import resize_folder_command
from resizelibrary.command.resize_file_command import resize_file_command
from resizelibrary.command.resize_profile_command import resize_profile_command

@click.group()
def cli():
    pass

cli.add_command(resize_folder_command)
cli.add_command(resize_file_command)
cli.add_command(resize_profile_command)

def main():
    cli()

if __name__ == '__main__':
    main()