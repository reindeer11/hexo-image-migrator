# Hexo 图片迁移工具（Agent skill）

将外部图片链接（语雀/Yuque CDN）迁移到本地 Hexo 资源文件夹的自动化工具。<br>
author: "reindeer"<br>
github: https://github.com/reindeer11

## 功能特点

- 自动扫描 Markdown 文件中的外部图片链接
- 批量下载图片到文章同名资源文件夹
- 自动转换为 Hexo 兼容的图片格式
- 智能命名避免文件冲突
- 自动备份原始文件

## 快速开始

### 1. 启用文章资源文件夹

在 Hexo 根目录的 `_config.yml` 中设置：

```yaml
post_asset_folder: true
```

### 2. 安装依赖

```bash
pip install requests
```

### 3. 运行脚本

```bash
python migrate_images.py
```

### 4. 重新生成网站

```bash
hexo clean
hexo generate
hexo server
```

## 使用示例

### 迁移前

```markdown
![](https://cdn.nlark.com/yuque/0/2026/webp/abc123.webp)
![](https://cdn.nlark.com/yuque/0/2026/webp/def456.webp)
```

### 迁移后

```markdown
{% asset_img img_01_a1b2c3d4e5.webp %}
{% asset_img img_02_f6g7h8i9j0.webp %}
```

## 文件结构

```
source/_posts/
├── 我的第一篇文章.md
├── 我的第一篇文章/
│   ├── img_01_a1b2c3d4e5.webp
│   └── img_02_f6g7h8i9j0.webp
├── 我的第二篇文章.md
└── 我的第二篇文章/
    └── img_01_k1l2m3n4o5.png
```

## 支持的图片来源

| 来源     | 示例                        |
| -------- | --------------------------- |
| 语雀 CDN | `cdn.nlark.com`             |
| GitHub   | `raw.githubusercontent.com` |
| 其他     | 任何 HTTP/HTTPS 图片 URL    |

## 配置选项

修改脚本顶部的 `POSTS_DIR` 变量可以指定文章目录：

```python
POSTS_DIR = r"G:\blog\source\_posts"
```

## 注意事项

1. 运行前建议备份 `source/_posts/` 目录
2. 确保网络可以访问外部图片 URL
3. 下载失败的图片会跳过，不会修改对应链接
4. 原始文件会自动备份为 `.bak` 文件

## 常见问题

**Q: 为什么图片显示不出来？**

A: 确保使用 `{% asset_img %}` 格式，而不是标准 Markdown 的 `![]()` 格式。

**Q: 部分图片下载失败怎么办？**

A: 检查网络连接，部分 CDN 可能有访问限制。可以手动下载后放入资源文件夹。

**Q: 如何恢复原始文件？**

A: 脚本会自动创建 `.bak` 备份文件，可以手动恢复。

## 许可证

MIT License
