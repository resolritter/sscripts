#!/bin/node

const cp = require("child_process");
const utils = require("./utils");
const getLinesFromOutput = utils.getLinesFromOutput;
const processConcurrently = utils.processConcurrently;
const fs = require("fs");

const gitTopLevel = getLinesFromOutput(
  cp.execSync("git rev-parse --show-toplevel")
)[0];

if (!gitTopLevel.length) {
  process.exit(1);
}

const files = process.argv.slice(2);
const stopFurtherFlag = "STOP_FURTHER";

function handleDiffOutputResolve(resolve) {
  return function handleDiffOutput(err, data) {
    if (!err?.code || (data && err?.code === 1)) {
      process.stdout.write(data);
    } else {
      console.log(err, err?.code, data);
      throw new Error(stopFurtherFlag);
    }
    resolve();
  };
}

let promiseCallbackPool = [[]];
if (files.length) {
  const gitStatusFiles = getLinesFromOutput(
    cp.execFileSync("git", "status --short".split(" "))
  );

  if (!gitStatusFiles.length) {
    process.exit(0);
  }

  toNextFile: for (const f of files) {
    toNextLine: for (const line of gitStatusFiles) {
      const file = line.split(" ")[1];
      if (file !== f && file !== `${f}/`) {
        continue toNextLine;
      }

      // file is staged
      if (line.match(/^A\s/) || line.match(/^M\s/)) {
        promiseCallbackPool[0].push(function() {
          return new Promise(function(resolve) {
            cp.execFile(
              "git",
              ["diff", "--no-pager", "--staged", file],
              handleDiffOutputResolve(resolve)
            );
          });
        });
        // file is untracked
      } else if (line.match(/^\?\?/)) {
        if (line.endsWith("/")) {
          promiseCallbackPool[0].push(function() {
            return new Promise(function(resolve) {
              cp.execFile(
                "git",
                ["ls-files", "--others", "--exclude-standard", f],
                function(err, data) {
                  if (err) {
                    throw new Error(stopFurtherFlag);
                  }
                  const folderFiles = getLinesFromOutput(data);
                  if (!promiseCallbackPool[1]) {
                    promiseCallbackPool[1] = [];
                  }
                  for (const ff of folderFiles) {
                    promiseCallbackPool[1].push(function() {
                      return new Promise(function(resolve) {
                        cp.execFile(
                          "git",
                          ["diff", "/dev/null", ff],
                          handleDiffOutputResolve(resolve)
                        );
                      });
                    });
                  }
                  resolve();
                }
              );
            });
          });
        } else {
          promiseCallbackPool[0].push(function() {
            return new Promise(function(resolve) {
              cp.execFile(
                "git",
                ["diff", "/dev/null", file],
                handleDiffOutputResolve(resolve)
              );
            });
          });
        }
        // file has been modified, but not staged
      } else if (line.match(/\sM/)) {
        promiseCallbackPool[0].push(function() {
          return new Promise(function(resolve) {
            cp.execFile(
              "git",
              ["diff", "--no-pager", file],
              handleDiffOutputResolve(resolve)
            );
          });
        });
      }

      continue toNextFile;
    }
  }
} else {
  let inputFiles = getLinesFromOutput(
    cp.execFileSync("git", "diff --name-only --staged".split(" "))
  );
  let diffCommand = ["diff", "--staged"];

  if (!inputFiles.length) {
    inputFiles = getLinesFromOutput(
      cp.execFileSync("git", "diff --name-only".split(" "))
    );
    diffCommand = ["diff"];

    if (!inputFiles.length) {
      diffCommand = ["diff", "/dev/null"];
      inputFiles = getLinesFromOutput(
        cp.execFileSync(
          "git",
          "ls-files --others --exclude-standard".split(" ")
        )
      );
    }
  }

  if (inputFiles.length) {
    try {
      utils.processConcurrently(inputFiles, function(file) {
        return new Promise(function(resolve, reject) {
          cp.execFile(
            "git",
            [...diffCommand, file],
            handleDiffOutputResolve(resolve)
          );
        });
      });
    } catch (e) {
      if (e.message !== stopFurtherFlag) {
        throw e;
      }
    }
  }
}

(async function() {
  let i = 0;
  for (let i = 0; i < promiseCallbackPool.length; i++) {
    await processConcurrently(promiseCallbackPool[i], async function(callback) {
      await callback();
    });
  }
})();
