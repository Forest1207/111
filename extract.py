import re
import os
import base64
from pathlib import Path

def extract_base64_images(html_path, output_folder="images"):
    """
    将 HTML 中的 Base64 图片提取为外部文件，并替换为 <img src> 引用
    """
    # 读取 HTML 文件
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 创建图片输出目录
    img_dir = os.path.join(os.path.dirname(html_path), output_folder)
    os.makedirs(img_dir, exist_ok=True)
    
    # 匹配所有 Base64 图片: data:image/xxx;base64,AAAA...
    pattern = r'data:image/([a-zA-Z]+);base64,([A-Za-z0-9+/=]+)'
    
    img_count = 0
    total_saved = 0
    
    def replace_base64(match):
        nonlocal img_count, total_saved
        
        ext = match.group(1)  # png, jpeg, gif 等
        base64_data = match.group(2)
        
        # 生成文件名
        img_count += 1
        filename = f"image_{img_count:03d}.{ext}"
        filepath = os.path.join(img_dir, filename)
        
        # 解码并保存图片
        try:
            img_bytes = base64.b64decode(base64_data)
            with open(filepath, 'wb') as img_file:
                img_file.write(img_bytes)
            
            file_size = len(img_bytes)
            total_saved += file_size
            print(f"  ✓ 提取: {filename} ({file_size/1024:.1f} KB)")
            
            # 返回替换后的相对路径
            return f"{output_folder}/{filename}"
            
        except Exception as e:
            print(f"  ✗ 失败: {filename} - {e}")
            return match.group(0)  # 失败时保留原样
    
    # 替换所有 Base64 为文件路径
    new_content = re.sub(pattern, replace_base64, content)
    
    # 保存新的 HTML 文件
    new_html_path = html_path.replace('.html', '_external.html')
    with open(new_html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"\n{'='*50}")
    print(f"处理完成!")
    print(f"  提取图片数: {img_count}")
    print(f"  图片总大小: {total_saved/1024/1024:.1f} MB")
    print(f"  新HTML文件: {new_html_path}")
    print(f"  图片文件夹: {img_dir}")
    print(f"{'='*50}")
    
    return new_html_path, img_dir

# ===== 使用方法 =====
if __name__ == "__main__":
    # 把你的 HTML 文件路径填在这里
    html_file = "建川博物馆.html"  # ← 修改为你的文件名
    
    extract_base64_images(html_file)