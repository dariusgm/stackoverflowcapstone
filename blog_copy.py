import os
from shutil import copyfile


blog_base = os.path.join("..", "blog")

if os.path.exists(blog_base):
    print("Copy Model")
    model_base = os.path.join("data", "model")
    model_path = os.listdir(model_base)[0]
    source_base = model_base + os.sep + model_path
    for f in os.listdir(source_base):
        source_path = source_base + os.sep + f
        target_path = os.path.join("..", "blog", "content", "js", f)
        print(f"{source_path} -> {target_path}")
        copyfile(source_path, target_path)

    print("Copy JavaScript")
    for f in os.listdir("js"):
        source_path = os.path.join("js", f)
        target_path = os.path.join("..", "blog", "content", "js", f)
        print(f"{source_path} -> {target_path}")
        copyfile(source_path, target_path)

    print("Copy HTML")
    source_path = os.path.join("capstone.html")
    target_path = os.path.join("..", "blog", "code", "capstone.html")
    print(f"{source_path} -> {target_path}")
    copyfile(source_path, target_path)
