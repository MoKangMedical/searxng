# 贡献指南

感谢您对SearXNG Medical AI项目的关注！我们欢迎所有形式的贡献。

## 如何贡献

### 报告问题

1. 使用GitHub Issues报告bug
2. 提供详细的问题描述
3. 包含复现步骤
4. 附上错误日志

### 提交代码

1. Fork项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

### 代码规范

- Python代码遵循PEP 8规范
- 使用类型注解
- 编写文档字符串
- 添加单元测试

### 提交信息规范

使用Conventional Commits规范：

```
<type>(<scope>): <subject>

<body>

<footer>
```

类型：
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建/工具

### 开发环境

```bash
# 克隆项目
git clone https://github.com/MoKangMedical/searxng.git
cd searxng

# 启动服务
./manage.sh start

# 运行测试
./scripts/comprehensive-test.sh
```

### Pull Request检查清单

- [ ] 代码通过lint检查
- [ ] 添加/更新测试
- [ ] 更新文档
- [ ] 测试通过
- [ ] 提交信息规范

## 行为准则

- 尊重所有贡献者
- 接受建设性批评
- 专注于对社区最有利的事情
- 对他人表示同理心

## 联系方式

- GitHub Issues: 报告问题
- GitHub Discussions: 讨论功能
- Email: contact@example.com
