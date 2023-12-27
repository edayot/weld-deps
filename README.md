# Weld deps

> A datapack package manager using smithed & modrinth sources


## Usage

This is a [beet](https://mcbeet.dev/) plugin that manage smithed/modrinth dependencies.

It's placed in the require section of the beet config file. 

Example:

```yaml
id: test
require:
  - weld_deps

data_pack:
  load: src

pipeline:
  - mecha

output: dist

meta:
  weld_deps:
    enable_weld_merging: False
    clean_load_tag: False
    include_prerelease: False
    deps:
      - id: "custom-block"
        match: ">0.0.0"
        source: "smithed"
      - id: "itemio"
        match: ">0.9.0"
        source: "smithed"
      - id: "code-of-copper"
        match: ">0.1.0"
        source: "modrinth"
```
