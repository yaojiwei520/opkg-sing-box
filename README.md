# opkg-sing-box
`pip install requests beautifulsoup4`

------
`pip install tqdm`

-------
# keyword = 'homeproxy' 比如'passwall'


代码说明：
download_file 函数：负责下载文件并显示进度条。
search_and_download_files 函数：在给定的子目录中查找包含指定关键字的文件。如果找到匹配的文件，则调用 download_file 函数下载它，并在下载完成后等待 2 秒。
主目录创建：代码会创建一个名为 opkg-file 的主目录，以存放下载的文件。
遍历子目录：代码遍历 packages/ 和 targets/ 中的每个子目录，查找并下载包含 homeproxy 的文件。
运行结果：
运行这段代码后，程序会下载所有找到的文件，并在每个文件下载完成后等待 2 秒。您可以根据需要调整等待时间。
