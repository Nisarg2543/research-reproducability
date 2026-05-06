from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("research-reproducability")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"
