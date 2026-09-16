# web_ua_checkin

- **分类**：Web
- **难度**：签到
- **题型**：HTTP 头认知与伪造 + base64编码还原

## 题面

Only iphone can do

## 部署

```bash
docker build -t ua_checkin ./src
docker run -d -p 8080:80 -e FLAG="hctf{xxx}" ua_checkin
```

