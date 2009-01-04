
from distutils.core import setup

setup(
    name = "queue_engine",
    version = "0.1.0pre",
    author = "Brian Rosner",
    author_email = "brosner@gmail.com",
    description = "Queue management and code deferment",
    long_description = open("README").read(),
    url = "http://github.com/brosner/engine/tree/master",
    packages = [
        "engine",
    ],
)
