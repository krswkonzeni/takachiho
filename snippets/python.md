# Python
```
#! /usr/bin/python
# -*- coding: utf8 -*-
```

```
import time

started = time.time()
elapsed = time.time() - started // second


import datetime

datetime.datetime.now().strftime("%F %T")
```

```
import MySQLdb

db = MySQLdb.connect(host,user,pass,db)
cur = db.cursor()
cur.execute(sql)
res = cur.fetchall()
cur.close()
db.close()

```

```
if __name__ == "__main__":
    main()
```


https://www.python.org/
