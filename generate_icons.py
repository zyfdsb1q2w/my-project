from PIL import Image
import os

def generate_png_icons(ico_path, output_dir="icons"):
    """从ICO文件生成各种尺寸的PNG图标"""
    
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 需要生成的尺寸
    sizes = [72, 96, 128, 144, 152, 192, 384, 512]
    
    try:
        # 打开ICO文件
        print(f"打开ICO文件: {ico_path}")
        ico_image = Image.open(ico_path)
        
        # ICO文件可能包含多个尺寸，我们选择最大的一个
        # 获取所有尺寸
        ico_images = []
        try:
            while True:
                ico_images.append(ico_image.copy())
                ico_image.seek(ico_image.tell() + 1)
        except EOFError:
            pass
        
        if not ico_images:
            print("错误：ICO文件中没有找到图像")
            return False
        
        # 选择最大的图像作为源
        source_image = max(ico_images, key=lambda img: img.size[0])
        print(f"使用源图像尺寸: {source_image.size}")
        
        # 转换为RGBA模式（支持透明度）
        if source_image.mode != 'RGBA':
            source_image = source_image.convert('RGBA')
        
        # 生成各种尺寸的PNG
        print("\n生成PNG图标...")
        for size in sizes:
            output_path = os.path.join(output_dir, f"icon-{size}x{size}.png")
            print(f"  生成 {size}x{size} -> {output_path}")
            
            # 调整尺寸
            resized = source_image.resize((size, size), Image.Resampling.LANCZOS)
            
            # 保存为PNG
            resized.save(output_path, format='PNG', optimize=True)
            
            # 验证文件
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                print(f"    大小: {file_size} 字节")
            else:
                print(f"    错误：文件未创建")
        
        print("\n图标生成完成！")
        return True
        
    except Exception as e:
        print(f"错误: {str(e)}")
        return False

def create_fallback_icons(output_dir="icons"):
    """创建简单的备用图标（如果ICO文件有问题）"""
    
    from PIL import Image, ImageDraw
    
    print("创建备用图标...")
    
    sizes = [72, 96, 128, 144, 152, 192, 384, 512]
    
    for size in sizes:
        # 创建新图像
        img = Image.new('RGBA', (size, size), color=(74, 134, 232, 255))  # 蓝色背景
        draw = ImageDraw.Draw(img)
        
        # 添加文字
        from PIL import ImageFont
        try:
            # 尝试使用默认字体
            font = ImageFont.load_default()
        except:
            font = None
        
        # 绘制简单的AI图标
        # 绘制圆形
        margin = size // 10
        circle_bbox = (margin, margin, size - margin, size - margin)
        draw.ellipse(circle_bbox, fill=(255, 255, 255, 255), outline=(255, 255, 255, 255))
        
        # 绘制AI文字
        text = "AI"
        if font:
            # 计算文字位置
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            text_position = ((size - text_width) // 2, (size - text_height) // 2)
            
            draw.text(text_position, text, fill=(74, 134, 232, 255), font=font)
        else:
            # 简单绘制
            draw.text((size//3, size//3), "AI", fill=(74, 134, 232, 255))
        
        # 保存
        output_path = os.path.join(output_dir, f"icon-{size}x{size}.png")
        img.save(output_path, format='PNG', optimize=True)
        print(f"  创建备用图标 {size}x{size}")
    
    print("备用图标创建完成！")
    return True

def main():
    print("=" * 50)
    print("美霖个人助手 - 图标生成器")
    print("=" * 50)
    
    ico_path = "app_icon.ico"
    output_dir = "icons"
    
    # 检查ICO文件是否存在
    if not os.path.exists(ico_path):
        print(f"警告：ICO文件不存在 - {ico_path}")
        print("将创建备用图标...")
        success = create_fallback_icons(output_dir)
    else:
        print(f"ICO文件: {ico_path}")
        print(f"输出目录: {output_dir}")
        print("=" * 50)
        
        # 尝试从ICO生成PNG
        success = generate_png_icons(ico_path, output_dir)
        
        # 如果失败，创建备用图标
        if not success:
            print("\nICO转换失败，创建备用图标...")
            success = create_fallback_icons(output_dir)
    
    if success:
        print("\n" + "=" * 50)
        print("图标生成成功！")
        print("=" * 50)
        
        # 列出生成的文件
        print("生成的图标文件：")
        for size in [72, 96, 128, 144, 152, 192, 384, 512]:
            file_path = os.path.join(output_dir, f"icon-{size}x{size}.png")
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                print(f"  ✓ icon-{size}x{size}.png ({file_size} 字节)")
            else:
                print(f"  ✗ icon-{size}x{size}.png (未找到)")
        
        print("\nPWA图标已准备就绪！")
    else:
        print("\n图标生成失败")

if __name__ == "__main__":
    main()