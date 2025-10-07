# 将NBS音符间距由1倍扩展为3倍 / stretch NBS note spacing from 1× to 3×
import pynbs

def stretch_nbs_file(input_path, output_path):
    # 读取已有的NBS文件
    nbs_file = pynbs.read(input_path)

    # 调整歌曲速度
    nbs_file.header.tempo = nbs_file.header.tempo * 3

    # 调整音符的时间位置
    for note in nbs_file.notes:
        note.tick = note.tick * 3

    # 保存扩展后的NBS文件
    nbs_file.save(output_path)

# 示例调用
input_nbs_path = "input.nbs"
output_nbs_path = "output.nbs"
stretch_nbs_file(input_nbs_path, output_nbs_path)
