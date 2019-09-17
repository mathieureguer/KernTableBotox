import os
import glob


def walk_input_path(input_path, target_extentions=[".otf"], recursive=False):
    fonts = []
    if os.path.isdir(input_path):
        input_dir = input_path
        if recursive:
            inputs = [root for root, dir, files in os.walk(input_path)]
        else:
            inputs = [input_path]
        for p in inputs:
            for ext in target_extentions:
                fonts.extend(
                    glob.glob(os.path.join(p, "*%s" % (ext))))
    elif input_path.endswith(tuple(target_extentions)):
        input_dir = os.path.dirname(input_path)
        fonts = [input_path]
    assert len(
        fonts) > 0, "The input path does not contain any fonts (%s)" % target_extentions
    return(input_dir, fonts)


def suffix_file(file_path, suffix):
    file_name, ext = os.path.splitext(file_path)
    return file_name + suffix + ext


def output_file_to_another_folder(file_path, output_dir):
    dir_, file_name = os.path.split(file_path)
    out_path = os.path.join(output_dir, file_name)
    return out_path
