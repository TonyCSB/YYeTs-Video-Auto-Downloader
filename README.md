# 人人影视视频自动下载器

本程序旨在自动下载**人人影视**最新更新视频，免去不断查看视频更新情况的烦恼。本作者将不定期更新程序。

`目录编辑器.py` 和 `index.txt` 分别为目录编辑器和目录列表。
- 其中所指的影视剧代码为下图红框中的5位数字：

![代码示意图](https://user-images.githubusercontent.com/21008477/34857630-ce7bd964-f719-11e7-8b9c-dc1f11570572.png)

`下载器.pyw` 为自动下载器，启动后可在计算机后台运行，每隔1-15分钟对 `index.txt` 中的所有影视剧进行扫描，如果发现更新，即会启动下载器。

建议将 `下载器.pyw` 的快捷方式保存在 `%AppData%\Microsoft\Windows\Start Menu\Programs\Startup` 文件夹内以实现开机自启动。

本程序采用磁力链接进行下载，推荐使用[μTorrent](https://www.utorrent.com/)。

- 可通过取消勾选 `在 Torrent 数据中显示更改名称和位置的选项` 跳过下载确认框
![μTorrent使用指南](https://user-images.githubusercontent.com/21008477/34857898-4a899dc4-f71b-11e7-895e-56e62e0e8ae4.png)

### 依赖库
- 使用 `pip install -r requirements.txt` 安装所需的依赖库
