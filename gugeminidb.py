import google.generativeai as genai
import PIL.Image
import os
import sys

# 获取程序的运行路径（无论是打包还是开发环境）
exe_dir = os.path.dirname(os.path.abspath(sys.argv[0]))  # 获取exe所在的目录

# 从 api.txt 文件读取 API 密钥
def load_api_key(file_name):
    try:
        # 使用程序所在的路径来读取文件
        file_path = os.path.join(exe_dir, file_name)
        with open(file_path, 'r') as file:
            api_key = file.read().strip()
        return api_key
    except Exception as e:
        print(f"Error loading API key: {e}")
        return None


# 读取文本文件内容
def load_text_file(file_name):
    try:
        # 使用程序所在的路径来读取文件
        file_path = os.path.join(exe_dir, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except Exception as e:
        print(f"Error reading file {file_name}: {e}")
        return None


# 使用 Gemini 处理图像和文本
def process_image_with_gemini(image_path, prompt_text, prefix_text):
    try:
        # 加载图片
        img = PIL.Image.open(image_path)

        # 创建模型实例
        model = genai.GenerativeModel('gemini-1.5-flash')  # 更新为最新的模型版本

        # 生成内容（组合文本提示和图像）
        response = model.generate_content([prompt_text, img])

        # 获取生成的文本
        if not response.parts:
            print(f"No response generated for {image_path}")
            return

        generated_text = response.text

        # 生成输出文件名
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        txt_path = os.path.join(os.path.dirname(image_path), f"{base_name}.txt")

        # 写入文件
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(f"{prefix_text}\n{generated_text}")

        print(f"成功生成：{txt_path}")

    except Exception as e:
        print(f"处理失败 {image_path}: {e}")


if __name__ == "__main__":
    # 配置API密钥和文本文件路径
    api_key_path = 'api.txt'  # 确保文本文件与程序处于同一目录下
    prompt_file_path = '提示文本.txt'
    prefix_file_path = '前缀文本.txt'

    # 加载API密钥、提示文本和前缀文本
    api_key = load_api_key(api_key_path)
    prompt_text = load_text_file(prompt_file_path)
    prefix_text = load_text_file(prefix_file_path)

    if not api_key:
        print("缺少API密钥")
        sys.exit(1)  # 修改为 sys.exit 而不是 exit()

    if not prompt_text or not prefix_text:
        print("提示文本或前缀文本文件缺失或读取失败")
        sys.exit(1)  # 修改为 sys.exit 而不是 exit()

    # 配置API
    genai.configure(api_key=api_key)

    # 获取图片文件夹路径
    folder = input("请输入图片文件夹路径：")

    if not os.path.exists(folder):
        print("文件夹不存在")
        sys.exit(1)  # 修改为 sys.exit 而不是 exit()

    # 确保是支持的图片格式
    supported_formats = ('.png', '.jpg', '.jpeg', '.webp')

    # 遍历文件夹中的所有图片文件
    for file in os.listdir(folder):
        if file.lower().endswith(supported_formats):
            full_path = os.path.join(folder, file)
            process_image_with_gemini(full_path, prompt_text, prefix_text)
