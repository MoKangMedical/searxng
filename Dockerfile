# SearXNG 自定义Dockerfile
# 用于构建包含中文优化配置的镜像

FROM ghcr.io/searxng/searxng:latest

# 设置工作目录
WORKDIR /usr/local/searxng

# 复制自定义配置
COPY config/settings.yml /etc/searxng/settings.yml
COPY config/limiter.toml /etc/searxng/limiter.toml

# 设置权限
RUN chown -R searxng:searxng /etc/searxng

# 暴露端口
EXPOSE 8080

# 启动命令
CMD ["/sbin/tini", "--", "/usr/local/searxng/dockerfiles/docker-entrypoint.sh"]
