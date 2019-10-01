# devi_binja
Binary Ninja Plugin for devi. For a detailed description how devi works see its [repository](https://github.com/murx-/devi/). This plugin uses the newly introduced possibility to add cross-references in binary ninja to devirtualize virtual calls. 

## Minimal Example

### Disassembly

Before:

![Disassembly before devi](https://github.com/murx-/devi_binja/blob/master/images/main_before_devi.png)


After:

![Disassembly with devi](https://github.com/murx-/devi_binja/blob/master/images/main_after_devi.png)

### XRefs


Before:

![Xrefs before devi](https://github.com/murx-/devi_binja/blob/master/images/xrefs_before_devi.png)

After:

![Xrefs after devi](https://github.com/murx-/devi_binja/blob/master/images/xrefs_after_devi.png)