(function () {
  function forEach(arr, f) {
    for (var i = 0, e = arr.length; i < e; ++i) f(arr[i]);
  }

  function arrayContains(arr, item) {
    if (!Array.prototype.indexOf) {
      var i = arr.length;
      while (i--) {
        if (arr[i] === item) {
          return true;
        }
      }
      return false;
    }
    return arr.indexOf(item) != -1;
  }

  function scriptHint(editor, _keywords, getToken) {
    // Find the token at the cursor
    var cur = editor.getCursor(), token = getToken(editor, cur), tprop = token;
    // If it's not a 'word-style' token, ignore the token.

    if (!/^[\w$_]*$/.test(token.string)) {
      token = tprop = {
        start: cur.ch, end: cur.ch, string: "", state: token.state,
        className: token.string == ":" ? "python-type" : null
      };
    }

    if (!context) var context = [];
    context.push(tprop);

    // Edited by CaptainChen. Adding the function of auto completion of variables and functions
    var keywordsCompletion = getCompletions(token, context);
    keywordsCompletion.sort();
    context.push(tprop);
    var customCompletion = getCustomCompletions(editor, token, context);
    customCompletion = customCompletion.sort();

    completionList = customCompletion.concat(keywordsCompletion);

    //prevent autocomplete for last word, instead show dropdown with one word
    if (completionList.length == 1) {
      completionList.push(" ");
    }

    return {
      list: completionList,
      from: CodeMirror.Pos(cur.line, token.start),
      to: CodeMirror.Pos(cur.line, token.end)
    };
  }

  CodeMirror.pythonHint = function (editor) {
    return scriptHint(editor, pythonKeywordsU, function (e, cur) { return e.getTokenAt(cur); });
  };

  var pythonKeywords = "and del from not while as elif global or with assert else if pass yield"
    + "break except import class in raise continue finally is return def for lambda try";
  var pythonKeywordsL = pythonKeywords.split(" ");
  var pythonKeywordsU = pythonKeywords.toUpperCase().split(" ");

  var pythonBuiltins = "abs divmod input open staticmethod all enumerate int ord str "
    + "any eval isinstance pow sum basestring execfile issubclass print super"
    + "bin file iter property tuple bool filter len range type"
    + "bytearray float list raw_input unichr callable format locals reduce unicode"
    + "chr frozenset long reload vars classmethod getattr map repr xrange"
    + "cmp globals max reversed zip compile hasattr memoryview round __import__"
    + "complex hash min set apply delattr help next setattr buffer"
    + "dict hex object slice coerce dir id oct sorted intern ";
  var pythonBuiltinsL = pythonBuiltins.split(" ").join("() ").split(" ");
  var pythonBuiltinsU = pythonBuiltins.toUpperCase().split(" ").join("() ").split(" ");

  function minDistance(s1, s2) {
    var len1 = s1.length
    var len2 = s2.length
    var dp = new Array(len1 + 1).fill(0).map(() => Array(len2 + 1).fill(0))
    for (var i = 0; i <= len1; i++) {
      dp[i][0] = i
    }
    for (var i = 0; i <= len2; i++) {
      dp[0][i] = i
    }
    for (var i = 1; i <= len1; i++) {
      for (var j = 1; j <= len2; j++) {
        if (s1[i - 1] == s2[j - 1]) {
          dp[i][j] = dp[i - 1][j - 1]
        } else {
          dp[i][j] = Math.min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + 1)
        }
      }
    }
    return dp[len1][len2]
  };

  function fuzzyCheck(word) {
    var builtins = pythonBuiltins.split(' ');
    for(var i in builtins) {
      if(minDistance(word,builtins[i])==1)
        return true;
    }
    for(var i in pythonKeywordsL) {
      if(minDistance(word,pythonKeywordsL[i])==1)
        return true;
    }
    return false;
  }

  CodeMirror.fuzzyCheck=fuzzyCheck;

  function getCompletions(token, context) {
    var found = [], start = token.string;
    function maybeAdd(str) {
      if (str.indexOf(start) == 0 && !arrayContains(found, str)) found.push(str);
    }

    function gatherCompletions(_obj) {
      forEach(pythonBuiltinsL, maybeAdd);
      forEach(pythonBuiltinsU, maybeAdd);
      forEach(pythonKeywordsL, maybeAdd);
      forEach(pythonKeywordsU, maybeAdd);
    }

    if (context) {
      // If this is a property, see if it belongs to some object we can
      // find in the current environment.
      var obj = context.pop(), base;

      if (obj.type == "variable")
        base = obj.string;
      else if (obj.type == "variable-3")
        base = ":" + obj.string;

      while (base != null && context.length)
        base = base[context.pop().string];
      if (base != null) gatherCompletions(base);
    }
    return found;
  }

  // Write by CaptainChen
  // Find completions of variables and functions
  function getCustomCompletions(editor, token, context) {
    var found = [], start = token.string;
    function maybeAdd(str) {
      if (str.indexOf(start) == 0 && !arrayContains(found, str)) found.push(str);
    }

    function gatherCompletions(_obj) {
      var n = editor.lineCount();
      for (var i = 0; i < n; i++) {
        var tokens = editor.getLineTokens(i);
        for (var j in tokens) {
          if (tokens[j].type == "variable" || tokens[j].type == "def") {
            maybeAdd(tokens[j].string);
          }
        }
      }
    }

    if (context) {
      // If this is a property, see if it belongs to some object we can
      // find in the current environment.
      var obj = context.pop(), base;

      if (obj.type == "variable")
        base = obj.string;
      else if (obj.type == "variable-3")
        base = ":" + obj.string;

      while (base != null && context.length)
        base = base[context.pop().string];
      if (base != null) gatherCompletions(base);
    }
    return found;
  }
})();