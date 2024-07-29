# Weld deps

> A datapack package manager using smithed API


## Usage

This is a [beet](https://mcbeet.dev/) plugin.

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
        version: "0.0.3"
      - id: "itemio"
        version: "0.9.0"
```
