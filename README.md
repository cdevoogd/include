# Include

A simple program that handles `#include` statements similar to the C preprocessor.

```
$ cat hello.txt
Hello

$ cat world.txt
World

$ cat include.txt
#include "hello.txt"
#include "world.txt"

$ include.py include.txt
Hello
World
```

The script can also handle includes inside of included files (up to a maximum depth).

```
$ cat hello.txt
Hello

$ cat world.txt
World

$ cat helloworld.txt
#include "hello.txt"
#include "world.txt"

$ cat include.txt
#include "helloworld.txt"

$ include.py include.txt
Hello
World
```
