import sys
from time import sleep
from shutil import copy
from os.path import expanduser

import click
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class NewPngHandler(FileSystemEventHandler):
	def __init__(self, destination):
		self.destination = destination


	def on_any_event(self, event):
		if event.is_directory: return
		if not event.event_type == 'created': return
		if not event.src_path.endswith('.png'): return
		print("Copying {} to {}".format(event.src_path, self.destination))
		copy(event.src_path, self.destination)


@click.command()
@click.argument('source', type=click.Path(), default=expanduser("~")+'/Documents')
@click.argument('destination', type=click.Path(), default='images')
def main(source, destination):
	event_handler = NewPngHandler(destination)
	observer = Observer()
	observer.schedule(event_handler, source, recursive=True)
	observer.start()
	print('Watching {}, press Ctrl+C to quit...'.format(source))
	try:
		while True:
			sleep(1)	
	except KeyboardInterrupt:
		observer.stop()
	observer.join()


if __name__ == '__main__':
	main()	
	