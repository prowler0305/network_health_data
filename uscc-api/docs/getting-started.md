# Getting Started

From a high level the API follows the basic concepts of Representational State Transfer (REST) and is served over HTTP protocols using the standard verbs (GET, POST, PUT, DELETE). If you are unfamiliar with REST or APIs in general we suggest doing a quick search on the internet where you find many articles and documents covering REST APIs to get familiar before diving into the architecture of this API further.

## Development Environment
The core of the USCC ENG API was written, at the time this documentation was written, using Python 3.5.4. It was built using the following additional microframeworks and extensions to allow it to be a RESTful Web API.

* [Flask](http://flask.pocoo.org/docs/0.12/) - a micro web development framework for python
* [Flask RESTful](https://flask-restful.readthedocs.io/en/latest/) - An extension to Flask for building REST APIs.

## Directory Structure

The structure is organized into 3 high level directories.

1. URL Endpoints (a.k.a Resources)
2. Data Source Specific resources
3. Core

### Resources
The resources directory contains the python files that correlate to a URL endpoint. These files encapsulates the specific HTTP protocol verbs, i.e. GET, POST, DELETE, PUT, etc that provide the interface to the accesses available to a data source.

### Data Sources
The data_source_resources directory is a parent directory in which within contains sub directories. These subdirectories group together like python files that provide specific data source functionality.

### Core
This directory contains python files that provide core api functionality or common functionality that can be used across the API.