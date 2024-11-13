import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time

# 定义要访问的 URL
base_url = 'https://fantastic-packages.github.io/packages/releases/23.05/'
packages_url = base_url + 'packages/'
targets_url = base_url + 'targets/'

def fetch_links(url):
    """从给定的 URL 中获取所有文件链接"""
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        file_links = []
        for link in links:
            href = link.get('href')
            if href and not href.startswith('#') and not href.endswith('/'):  # 排除锚链接和目录
                file_links.append(href)
        return file_links
    else:
        print(f"请求失败，状态码: {response.status_code}")
        return []

def download_file(url, save_path):
    """下载文件并显示进度条"""
    # 确保保存路径的目录存在
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(save_path, 'wb') as f, tqdm(total=total_size, unit='B', unit_scale=True, desc=save_path) as bar:
        for data in response.iter_content(chunk_size=1024):
            f.write(data)
            bar.update(len(data))

def search_and_download_files(base_url, subdir, keyword, main_directory):
    """搜索指定子目录中的文件，查找包含关键字的文件并下载"""
    subdir_url = base_url + subdir
    files = fetch_links(subdir_url)
    
    for file in files:
        if keyword in file:
            file_url = subdir_url + file
            save_path = os.path.join(main_directory, subdir.strip('/'), file)
            print(f"正在下载: {file_url}")
            download_file(file_url, save_path)
            print(f"下载完成: {save_path}")
            time.sleep(2)  # 等待 2 秒

# 创建保存文件的主目录
main_directory = 'opkg-file'
os.makedirs(main_directory, exist_ok=True)

# 获取 packages/ 中的子目录
packages_subdirs = [
    'aarch64_cortex-a53/',
    'aarch64_generic/',
    'arm_cortex-a15_neon-vfpv4/',
    'mips_24kc/',
    'mipsel_24kc/',
    'x86_64/'
]

# 查找并下载包含 'homeproxy' 的文件
keyword = 'passwall'

# 遍历 packages/ 中的子目录
for subdir in packages_subdirs:
    search_and_download_files(packages_url, subdir + 'luci/', keyword, main_directory)
    search_and_download_files(packages_url, subdir + 'packages/', keyword, main_directory)

# 遍历 targets/x86/ 中的文件
targets_subdirs = ['x86/']
for subdir in targets_subdirs:
    search_and_download_files(targets_url, subdir, keyword, main_directory)
