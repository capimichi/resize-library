import click
from resizelibrary.container.DefaultContainer import DefaultContainer
from resizelibrary.service.ResizeService import ResizeService

@click.command(
    name='resize:profile'
)
@click.argument('profile_path', type=click.Path(exists=True, file_okay=True, dir_okay=False))
def resize_profile_command(profile_path):
    default_container: DefaultContainer = DefaultContainer.getInstance()
    resize_service: ResizeService = default_container.get(ResizeService)
    
    resize_service.resize_with_profile(profile_path)
