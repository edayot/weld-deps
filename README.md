# Weld deps

> A datapack package manager using smithed API

PyPi: [https://pypi.org/project/weld-deps/](https://pypi.org/project/weld-deps/)

## Usage

This is a [beet](https://mcbeet.dev/) plugin.

It's placed in the require section of the beet config file. 

See all examples here : https://github.com/edayot/weld-deps/tree/main/examples

## A quick introduction to the format
```yaml
require:
  - weld_deps
## The dict way
meta:
  weld_deps:
    default_source: "smithed" # This is not needed, smithed is the default for default_source
    deps:
      smithed.crafter.dev: # You can provide a version by a dict
        version: "0.4.0"
      itemio: "1.0.0" # Or by a string
## The list way
meta:
  weld_deps:
    default_source: "modrinth" # This is needed if you want to work with modrinth deps as default
    deps:
      - id: player_motion
        version: "1.3.1"
        source: "smithed"
      - id: code-of-copper # The source is automaticly to modrinth
        version: "0.3.0"
## Multiple sources
meta:
  weld_deps:
    deps:
      player_motion: "1.3.1"
      code-of-copper:
        version: "0.3.0"
        source: "modrinth"
      itemio:
        version: "1.2.6"
        source: "download"
        download:
          datapack: "https://github.com/edayot/ItemIO/releases/download/v1.2.6/ItemIO-v1.2.6-Datapack.zip"
```