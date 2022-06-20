# XClip
Usage:
- Start on docker
  ```bash
  docker run -p 8080:8080 -v /opt/config:/config --name xclip -d ryosetsu/xclip
  ```
- Add user 
  - by AddUser.py script ( *It's not packed in the image,use wget/curl/docker cp/volume to send it in to the container* )
    ```bash
    AddUser.py [username] [password]
    ```
  - by other sqlite tool

    columns:
    - id: md5 hash of username
    - name: username
    - passowrd: md5 hash of raw password
    - flag: set 1 meaning enable
- Set value
  ```
  POST /id  // md5(username)
  header: 
  - token   // md5(md5(RAW PASSWORD) + str(timestamp/10))    allow ±10s timestamp offset,so make sure that your server&client's clock are synchronized
  form:
  - value   // message
  ```
- Get value
  ```
  GET /id   // md5(username)
  header: 
  - token   // md5(md5(RAW PASSWORD) + str(timestamp/10))    allow ±10s timestamp offset,so make sure that your server&client's clock are synchronized
