# -- coding: utf-8 --
"""

"""


from collections import Counter
from functools import partial

# for file reading
import argparse
from pathlib import Path

# for testing
import os
import tempfile

#---------- PPM I/O ----------#

def write_ppm(filename, img):
    """
    Write a PPM image file.
    :param filename: str, the name of the output file
    :param img: list of list of tuples, the image data (each pixel is a tuple of (r, g, b))
    """
    height = len(img)
    width = len(img[0]) if height > 0 else 0
    with open(filename, 'wb') as f:
        f.write(f'P6\n{width} {height}\n255\n'.encode())
        for row in img:
            for pixel in row:
                f.write(bytes(pixel))

def read_ppm_old(filename):
    """
    Read a PPM image file.
    :param filename: str, the name of the input file
    :return: list of list of tuples, the image data (each pixel is a tuple of (r, g, b))

    pipeline:
    1. Open the file in binary mode.
    2. Read the header and check if it's a P6 PPM file.
        *  4  tokens：b"P6"、width、height、maxval;
              space-separated token;'#'  comment lines are ignored. 
    3. Read the dimensions (width and height) and the maximum color value. 
    4. Read the pixel data and store it in a list of lists.
    5. Return the image data.


    """
    with open(filename, 'rb') as f: #1
        header = f.readline().decode().strip()
        if header != 'P6':
            raise ValueError('Not a PPM P6 file')
        dimensions = f.readline().decode().strip()
        # Ignore comment lines
        while dimensions.startswith('#'):
            dimensions = f.readline().decode().strip()
        
        width, height = map(int, dimensions.split())
        maxval = int(f.readline().decode().strip())
        if maxval != 255:
            raise ValueError('Only maxval 255 is supported')
        img = []
        for _ in range(height):
            row = []
            for _ in range(width):
                pixel = tuple(f.read(3))
                row.append(pixel)
            img.append(row)
    return img


def read_ppm(filename):
    """
    Read a PPM image file.
    :param filename: str, the name of the input file
    :return: list of list of tuples, the image data (each pixel is a tuple of (r, g, b))

    pipeline:
    1. Open the file in binary mode.
    2. Read the header and check if it's a P6 PPM file.
        *  4  tokens：b"P6"、width、height、maxval;
              space-separated token;'#'  comment lines are ignored. 
    3. Read the dimensions (width and height) and the maximum color value. 
    4. Read the pixel data and store it in a list of lists.
    5. Return the image data.


    """
    with open(filename, 'rb') as f: #1
        header = f.readline().decode().strip()
        if header != 'P6':
            raise ValueError('Not a PPM P6 file')
        dimensions = f.readline().decode().strip()
        # Ignore comment lines
        while dimensions.startswith('#'):
            dimensions = f.readline().decode().strip()
        
        width, height = map(int, dimensions.split())
        maxval = int(f.readline().decode().strip())
        if maxval != 255:
            raise ValueError('Only maxval 255 is supported')
        
        data = f.read()
        expected = width * height * 3
        if len(data) != expected :
            raise ValueError(f"Pixel data size mismatch: expected {expected} bytes, got {len(data)}")

        # len(data) 是 6，expected 是 12，不相等，
        # 直接 raise ValueError，被測試的 except ValueError: pass 接住，測試通過。

        if width <= 0 or height <= 0:
            raise ValueError("Image dimensions must be positive integers.")

        row_bytes = width * 3
        img = [
            [tuple(data[i:i+3]) for i in range(start, start + row_bytes, 3)]
            for start in range(0, len(data), row_bytes)
        ]
    return img
    
#-----------------------#




#---------- helper functions ----------#

def get_block(img, x, y, bw, bh):
    """
    Get a block of pixels from the image.
    :param img: list of list of tuples, the image data
    :param x: int, the x-coordinate of the top-left corner of the block
    :param y: int, the y-coordinate of the top-left corner of the block
    :param bw: int, the width of the block
    :param bh: int, the height of the block
    :return: list of tuples, the block of pixels
    """
    return [px for row in img[y:y+bh] for px in row[x:x+bw]]


def block_average_v2(block):
    """
    Calculate the average color of a block of pixels.
    :param block: list of list of tuples, the block of pixels
    :return: tuple, the average color (r, g, b)
    """
    r_total = g_total = b_total = 0
    count = 0
    for row in block:
        for pixel in row:
            r_total += pixel[0]
            g_total += pixel[1]
            b_total += pixel[2]
            count += 1
    return (r_total // count, g_total // count, b_total // count)


def block_average_rgb(block):
    """回傳區塊的平均色 tuple，各通道取 int。"""

    #r_values, g_values, b_values = zip(*[pixel for row in block for pixel in row])
    channel_values  = [pixel for row in block for pixel in row]

    if not channel_values:
        raise ValueError("區塊內沒有像素，無法計算平均色。")
    else:
        r_values = [pixel[0] for pixel in channel_values]
        g_values = [pixel[1] for pixel in channel_values]
        b_values = [pixel[2] for pixel in channel_values]

        r_avg = sum(r_values) // len(r_values) if r_values else 0
        g_avg = sum(g_values) // len(g_values) if g_values else 0
        b_avg = sum(b_values) // len(b_values) if b_values else 0

    return (r_avg, g_avg, b_avg)


def block_average(block):
    if not block:
        raise ValueError("區塊內沒有像素，無法計算平均色。")
    n = len(block)
    return tuple(sum(channel) // n for channel in zip(*block))


def mode_color(block):
    """回傳區塊內出現最多次的顏色。"""
    most_common_pixel, _ = Counter(block).most_common(1)[0]
    return most_common_pixel

#-----------------------------#




#-------------- file I/O & main function ---------------#

def positive_int(s):
    """Convert a string to a positive integer, raising an error if it's not valid."""
    try:
        value = int(s)
        if value <= 0:
            raise ValueError
        return value
    except ValueError:
        raise argparse.ArgumentTypeError(f"{s} is not a valid positive integer.")


def build_parser():
    parser = argparse.ArgumentParser(description="Compress a PPM image by averaging colors in blocks.")
    parser.add_argument("input_file", type=Path, help="Path to the input PPM file. (.ppm)")
    parser.add_argument("--output", "-o", type=Path, help="Path to the output compressed PPM file.")
    parser.add_argument("--bw", type=positive_int, required=True, help="block width")
    parser.add_argument("--bh", type=positive_int, required=True, help="block height")
    parser.add_argument("--c_method", choices=["quick", "normal", "sharp"], default="quick",
                        help="Method for determining block color: 'quick' (average), 'normal' (dominant cluster), or 'sharp' (mode) (default: quick).")
    parser.add_argument("-t", "--tol", type=int, default=10,
                        help="Tolerance for color clustering (used with 'normal' and 'sharp' methods) (default: 10).")
    return parser

def default_output(input_path: Path) -> Path:
    """ cat.ppm -> cat_compressed.ppm, put in the same directory as input_path. """
    return input_path.with_name(input_path.stem+"_compressed.ppm")


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    output_path = args.output if args.output else default_output(args.input_file)
    original_img = read_ppm(args.input_file)
    color_fn = make_color_fn(args.c_method, args.tol)
    compressed_img = compress_image(original_img, args.bw, args.bh, color_fn)
    write_ppm(output_path, compressed_img)

    print(f"Compressed image saved to {output_path} (original: {args.input_file})")
    print(f"Input dimensions: {len(original_img[0])}x{len(original_img)}\n Output dimensions: {len(compressed_img[0])}x{len(compressed_img)}")
#-----------------------------#

#---------- Main process: Compress image ----------#

def is_close(a, b, tol=10):
    """Check if two colors are close to each other within a tolerance."""
    return all(abs(x - y) <= tol for x, y in zip(a, b))

def dominant_cluster(pixels, tol=10):
    """
    Find the dominant color cluster in a list of pixels.
    Methods: Greedy clustering based on color proximity.
    Steps:
    1. Take the first pixel as the initial cluster center.
    2. For each subsequent pixel, check if it is close to any existing cluster center.
       If it is, add it to that cluster; otherwise, create a new cluster with this pixel as the center.
    3. After processing all pixels, find the cluster with the most members and return the pixel list.
    4. If there are no clusters with the size larger than 2, return None.
    5. If there are multiple clusters with the same size, return the first one found.
    """
    clusters = []
    for pixel in pixels:
        found_cluster = False
        for cluster in clusters:
            if is_close(pixel, cluster[0], tol):
                cluster.append(pixel)
                found_cluster = True
                break
        if not found_cluster:
            clusters.append([pixel])

    # Find the largest cluster
    largest_cluster = max(clusters, key=len, default=[])
    if len(largest_cluster) >= 2:
        return largest_cluster
    else:
        return None

def cluster_color(pixels, tol=10):
    """
    Return the average color of the dominant cluster of pixels.
    If no dominant cluster is found, return the average color of all pixels.
    """

    dominant = dominant_cluster(pixels, tol)
    if dominant:
        return block_average(dominant)
    else:
        return block_average(pixels)


def sharp_color(block, tol=10):
    """
    Return the average color of the dominant cluster of pixels in the block.
    If no dominant cluster is found, return the average color of all pixels in the block.
    """

    if len(block) == len(set(block)):
        # All pixels are unique, return the average color of the block
        return cluster_color(block, tol)
    else:
        return mode_color(block) 

def make_color_fn(method="quick", tol=10):
    """
    Return a color function based on the specified name.
    """

    if method == "quick":
        return block_average
    elif method == "normal":
        return partial(cluster_color, tol=tol)
    elif method == "sharp":
        return partial(sharp_color, tol=tol)
    else:
        raise ValueError(f"Unknown color function: {method}")


def compress_image(img, bw, bh, color_fn):
    """
    Compress the image by dividing it into blocks of size (bw, bh)
    and applying color_fn: list[tuple] -> tuple to each block.
    """

    if bw <= 0 or bh <= 0:
        raise ValueError("Block width and height must be positive integers.")
    if not img or not img[0]:
        raise ValueError("Image cannot be empty.")

    height = len(img)
    width = len(img[0])
    compressed_img = []

    for y in range(0, height, bh):
        row = []
        for x in range(0, width, bw):
            block = get_block(img, x, y, bw, bh)
            color = color_fn(block)
            row.append(color)
        compressed_img.append(row)

    return compressed_img




if __name__ == "__main__":

    #------------- test blocks ----------------#
    #------------- test block helper functions ----------------#
    # test file: 4x4 image (r,g,b)
    img = [[(10, 10, 10), (20, 20, 20), (200, 0, 0), (200, 0, 0)],
        [(30, 30, 30), (40, 40, 40), (200, 0, 0), (200, 0, 0)],
        [(0, 0, 255), (0, 0, 255), (50, 60, 70), (50, 60, 70)],
        [(0, 0, 255), (0, 0, 255), (50, 60, 70), (50, 60, 70)]
    ]
    assert block_average(get_block(img, 0, 0, 2, 2)) == (25, 25, 25)
    assert block_average(get_block(img, 2, 0, 2, 2)) == (200, 0, 0)
    assert block_average(get_block(img, 3, 3, 2, 2)) == (50, 60, 70)

    try:
        block_average([])
        assert False, "空區塊應該報錯"
    except (ValueError, IndexError, ZeroDivisionError):
        pass
    
    assert get_block(img, 3, 3, 2, 2) == [(50, 60, 70)]   # 邊界：只剩 1 個像素

    assert compress_image(img, 2, 2, block_average) == [[(25, 25, 25), (200, 0, 0)], [(0, 0, 255), (50, 60, 70)]]
    assert compress_image(img, 2, 2, mode_color) == [[(10, 10, 10), (200, 0, 0)], [(0, 0, 255), (50, 60, 70)]]

    # boundary test: 3x3 in 4x4 --> 2x2
    out = compress_image(img, 3, 3, block_average)
    assert len(out) == 2 and len(out[0]) == 2

    # 輸入驗證
    try:
        compress_image(img, 0, 2, block_average)
        assert False, "bw=0 應該報錯"
    except ValueError:
        pass


    assert is_close((100,), (110,), 10) == True   # 差剛好 = tol
    assert is_close((100,), (109,), 10) is True
    assert is_close((100,), (111,), 10) is False
    assert is_close((5, 5), (5, 5), 0) == True    # tol=0、完全相同


    px = [(100,100,100), (105,95,100), (200,0,0), (102,101,99)]
    assert make_color_fn("quick", 10)(px) == block_average(px)
    assert make_color_fn("normal", 10)(px) == (102, 98, 99)

    # sharp：有重複 → 眾數，不看 tol
    assert make_color_fn("sharp", 10)([(1,1,1), (1,1,1), (9,9,9)]) == (1, 1, 1)
    # sharp：全不同 → 退回 normal，三個像素互相接近 → 群大小 3 → 平均
    assert make_color_fn("sharp", 10)([(100,100,100), (105,95,100), (102,101,99)]) == (102, 98, 99)

    try:
        make_color_fn("nope", 10)
        assert False
    except ValueError:
        pass



    #------------- test the equivalence between cluster_color and original_approximate ----------------#

    import random
    from ex1_original_file import approximate as original_approximate
    
    for _ in range(2000):
        n = random.randint(1, 12)
        px = [tuple(random.randint(0, 255) for _ in range(3)) for _ in range(n)]
        tol = random.randint(1, 60)
        ref = original_approximate(tol, [list(p) for p in px])
        expected = tuple(ref) if ref else block_average(px)
        assert cluster_color(px, tol - 1) == expected, (px, tol)

    #------------- test PPM I/O ----------------#
    import os
    import tempfile

    def test_roundtrip():
        # 含 (10,10,10)：byte 值 10 就是 \n，32 就是空格，專門測像素資料裡的空白字元
        test = [[(x * 8 % 256, y * 8 % 256, 128) for x in range(32)] for y in range(32)]
        test[0][0] = (10, 10, 10)
        test[0][1] = (32, 32, 32)
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "t.ppm")
            write_ppm(path, test)
            assert read_ppm(path) == test

    def test_end_to_end():
        src = [[(x * 8 % 256, y * 8 % 256, 128) for x in range(30)] for y in range(20)]
        with tempfile.TemporaryDirectory() as d:
            a, b = os.path.join(d, "a.ppm"), os.path.join(d, "b.ppm")
            write_ppm(a, src)
            out = compress_image(read_ppm(a), 4, 4, make_color_fn("normal", 10))
            write_ppm(b, out)
            back = read_ppm(b)
            assert back == out
            assert len(back) == 5 and len(back[0]) == 8   # ceil(20/4)=5, ceil(30/4)=8

    test_roundtrip()
    test_end_to_end()

    def test_truncated():
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "bad.ppm")
            with open(path, "wb") as f:
                f.write(b"P6\n2 2\n255\n" + bytes(6))   # 需要 12 bytes，只給 6
            try:
                read_ppm(path)
                assert False, "截斷的檔案應該報錯"
            except ValueError:
                pass

    test_truncated()           

    #-------------- test CLI ---------------#

    def test_cli():
        src = [[(x * 8 % 256, y * 8 % 256, 128) for x in range(30)] for y in range(20)]
        with tempfile.TemporaryDirectory() as d:
            a = Path(d) / "a.ppm"
            write_ppm(a, src)
            main([str(a), "--bw", "4", "--bh", "4", "--c_method", "quick"])
            out = read_ppm(Path(d) / "a_compressed.ppm")
            assert len(out) == 5 and len(out[0]) == 8

        # 非法輸入：argparse 會呼叫 sys.exit(2)，所以接 SystemExit
        try:
            main([str(a), "--bw", "0", "--bh", "4"])
            assert False
        except SystemExit as e:
            assert e.code == 2

    test_cli()
    #-----------------------------#
    print("all tests passed")