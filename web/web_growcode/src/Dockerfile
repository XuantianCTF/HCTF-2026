# web_growcode 部署镜像（内部，不对选手公开）
# 单文件 PHP 页面，纯脚本与 libc 无关，按仓库规则使用 alpine 运行时。
# PHP 内置服务器直出，主进程 root；选手命令经 su 降权到 www-data 执行，
# 配合源码 600 权限与进程内清除 FLAG，封死读源码与 /proc 环境两条泄露路径。
FROM php:8.3-cli-alpine

WORKDIR /app
COPY index.php .

# 题目源码仅 root 可读：选手降权后的 shell 无法读取引擎实现
RUN chmod 600 /app/index.php

# 诱饵 flag：选手用通配符拆词可读出，内容为假 flag 与指引提示
RUN printf 'flag{y0u_f0und_a_d3c0y_n0t_th3_r3al_0ne}\n这不是真正的通关凭证。\n它不在磁盘上，也不在环境变量里——\n它只存在于正在运行的那段代码的内存里。\n' > /flag

# 内置服务器默认单进程，开 worker 支持并发
ENV PHP_CLI_SERVER_WORKERS=8

# 动态 FLAG 由平台启动容器时注入；此处不设默认值，缺注入即可暴露。
# PHP 层禁用文件/目录/网络等高危函数（系统命令执行保留给题目逻辑），
# open_basedir 限制 PHP 自身文件访问范围。
EXPOSE 80
CMD ["php", "-d", "disable_functions=scandir,opendir,readdir,closedir,chdir,chroot,glob,file,file_get_contents,file_put_contents,fopen,fread,fwrite,fgets,fgetc,fgetss,fputcsv,fpassthru,popen,pfclose,readfile,readlink,link,symlink,unlink,rename,copy,mkdir,rmdir,touch,parse_ini_file,highlight_file,show_source,php_strip_whitespace,php_uname,phpinfo,disk_free_space,disk_total_space,stat,lstat,stream_socket_client,stream_socket_server,stream_socket_pair,fsockopen,pfsockopen,socket_create,socket_connect,curl_init,curl_exec,curl_multi_exec,proc_open,proc_close,proc_nice,proc_get_status,proc_terminate,pcntl_exec,pcntl_fork,dl,mail,posix_kill", "-d", "open_basedir=/app", "-S", "0.0.0.0:80"]
