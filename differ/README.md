# Before running

```
  npm install
```

# Description

`differ` recursively captures the output of `git diff` throughout all changed
files in the tree; it does so according to the following rules:

First of all, go to a Git directory

```
  cd my_project
```

## With arguments

Usage:

```
  differ.js [file1] [file2] ...
```

- If a file is a directory, then recursively diff it [1]
- Otherwise, diff directly, as usual

## Without arguments

Usage:

```
  differ.js
```

- If some files are staged, then diff only them
- Otherwise, if some files are modified, then diff only them
- Otherwise, diff untracked files [1]

---

[1] Untracked files are diffed with `/dev/null`, thus their whole output is
pushed to stdout
