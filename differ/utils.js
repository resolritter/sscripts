const asyncPool = require("tiny-async-pool")
const os = require("os")
const cpuCount = os.cpus().length

module.exports = {
  processConcurrently: function(files, promiseIteratorFn) {
    return asyncPool(cpuCount, files, promiseIteratorFn)
  },
  getLinesFromOutput: function(str) {
    const lines = str
      .toString()
      .trim()
      .split("\n")
    if (!lines[0]) {
      return []
    } else {
      return lines
    }
  },
}
