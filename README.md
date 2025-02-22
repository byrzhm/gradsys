# gradsys
一个完整的评分系统


## 创建评分容器
```bash
mkdir var
git clone git@github.com:bupthpc/cs101-sp25-labs.git var/labs --depth=1
docker build -t grading-image -f ./docker/grading/Dockerfile .
```