import os

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from helpers.downloader import download_to_local


class Command(BaseCommand):
    """
    Command to download vendor static files from a given URL (custom filename can be specified).
    """

    help = 'Downloads vendor static files from the given URL'

    def add_arguments(self, parser):
        parser.add_argument(
            'url',
            type=str,
            help='The URL of the vendor static file to download'
        )
        parser.add_argument(
            '--output',
            type=str,
            default=None,
            help='The filename to save the downloaded file as'
        )

    def handle(self, *args, **options):
        url = options.get('url') or None
        output_filename = options.get('output') or None

        static_dir = settings.STATICFILES_VENDOR_DIR

        if output_filename:
            out_path = static_dir / output_filename
        else:
            output_filename = os.path.basename(url.split('?')[0])
            out_path = static_dir / output_filename

        self.stdout.write(f'Downloading: {url}...')

        success = download_to_local(url, out_path, parent_mkdir=True)

        if success:
            self.stdout.write(self.style.SUCCESS(f'Successfully downloaded: {output_filename}.'))
        else:
            raise CommandError(f'Failed to download: {url}.')
