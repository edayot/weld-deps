# Weld deps

> A datapack package manager using smithed API

PyPi: [https://pypi.org/project/weld-deps/](https://pypi.org/project/weld-deps/)

## Usage

This is a [beet](https://mcbeet.dev/) plugin.

It's placed in the require section of the beet config file. 

Example:

```yaml
id: test
require:
  - weld_deps

meta:
  weld_deps:
    deps:
      smithed.crafter.dev:
        version: "0.4.0"
      itemio:
        version: "1.0.0"

```
