# Simple HTTPS Auth Server

Let `key` be

``` bash
echo -n 'username:password' | base64
```

Let `port=443` be any port number you'd like,

Let certificate be `./site.crt`,

Let key be `./site.key`,

Let files be in `./files` folder,

Let logs be `./server.log`,

Let server header be anything you'd like,

Then execute `python3 server.py`.




