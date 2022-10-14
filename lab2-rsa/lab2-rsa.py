import math
import random

# random.seed(1024)

# 对密文进行编、解码处理时的ascii码值偏移量
offset = 90


# 对字符串s进行编码，将结果转换为int列表
# 每个字符对应一个int，将其转化为一个4位十进制数
# 转化的具体方法是将每个字符的ascii码值乘上10再加上原来的个位数字
def encode_text(s):
    res = []
    for ch in s:
        ascii_code = ord(ch)
        res.append(ascii_code * 10 + ascii_code % 10)
    return res


# 解码，将int列表转换回字符串s
# 每个int对应一个字符，直接忽略个位数将其值除以10，找到对应ascii码值的字符
def decode_text(int_list):
    ch_list = []
    for num in int_list:
        ch_list.append(chr(int(num // 10)))
    return "".join(ch_list)


# 将字符串s(应当全部由0-9组成)转换为int列表
# 先切割成长度相等的若干组，每组长度为group_size
# 将得到每组字符串转化为int，最终构成int列表
def string2int(s, group_size):
    string_size = len(s)
    int_list = []
    group_num = string_size // group_size
    for i in range(group_num):
        num_str = s[i * group_size:(i + 1) * group_size]
        int_list.append(int(num_str))
    remainder = string_size % group_size
    if remainder != 0:
        num_str = s[group_num * group_size:]
        int_list.append(int(num_str))
    return int_list


# 将int列表转换为字符串s(应当全部由0-9组成)
# 每个int对应的字符串长度为group_size
# 若不足group_size个，则在前面补0
def int2string(int_list, group_size):
    string_list = []
    for num in int_list:
        string = str(num)
        string_size = len(string)
        rest = group_size - string_size
        new_string = "0" * rest + string
        string_list.append(new_string)
    return "".join(string_list)


# 快速幂算法求解a的b次方模c
def pow_mod(a, b, c):
    ans = 1
    a = a % c
    while b > 0:
        if b & 1 == 1:
            ans = (ans * a) % c
        b = b >> 1
        a = (a * a) % c
    return ans


# Miller-Rabin算法
# 返回True，很可能为素数
# 返回False，不是素数
def miller_rabin(n):
    if n == 2:
        return True
    elif n == 1 or n & 1 == 0:
        return False
    else:
        # 先找出正整数k和奇数q，使得2的k次方乘上q等于n-1
        k = 0
        q = n - 1
        while q & 1 == 0:
            k += 1
            q = q >> 1
        a = random.randint(2, n - 2)
        temp = pow_mod(a, q, n)
        if temp == 1 or temp == (n - 1):
            return True
        for j in range(1, k):
            if pow_mod(a, q * 2 ** j, n) == n - 1:
                return True
        return False


# 生成一个大数(不一定是质数，有待后续判断)
# 所生成大数的二进制长度默认为1024bit
def generate_big_num(digit=1024):
    num = 0
    for i in range(digit):
        num = num * 2 + random.randint(0, 1)
    return num


# 欧几里得算法
# 求出a和b的最大公因数
def euclid(a, b):
    x = a
    y = b
    while y != 0:
        r = x % y
        x = y
        y = r
    return x


# 寻找公钥(e, n)中的e
def calculate_e(phi):
    num = random.randint(2, phi - 1)
    while euclid(num, phi) != 1 or miller_rabin(num) is False:
        num += 1
    return num


# 扩展欧几里得算法
# 求出b在模a下的乘法逆元
def extended_euclid(a, b):
    x1, x2, x3 = 1, 0, a
    y1, y2, y3 = 0, 1, b
    while True:
        m = x3 // y3
        t1, t2, t3 = x1 - m * y1, x2 - m * y2, x3 - m * y3
        x1, x2, x3 = y1, y2, y3
        y1, y2, y3 = t1, t2, t3
        if y3 == 1:
            break
    if y2 < 0:
        y2 += a
    return y2


# 使用公钥进行加密
def encrypt(m_list, e, n):
    c_list = []
    for m in m_list:
        c = pow_mod(m, e, n)
        c_list.append(c)
    return c_list


# 使用私钥进行解密
def decrypt(c_list, d, n):
    p_list = []
    for c in c_list:
        p = pow_mod(c, d, n)
        p_list.append(p)
    return p_list


if __name__ == "__main__":
    with open("lab2-Plaintext.txt") as fin1:
        plain_text = fin1.read()
        fin1.close()

    p = generate_big_num()
    while not miller_rabin(p):
        p += 1
    print("使用Miller-Rabin算法生成一个二进制位数为1024bit的大素数p:")
    print("p =", p)

    q = generate_big_num()
    while not miller_rabin(q):
        q += 1
    print("使用Miller-Rabin算法生成一个二进制位数为1024bit的大素数q:")
    print("q =", q)

    n = p * q
    print("求出大素数p与大素数q的乘积n:")
    print("n =", n)

    phi_n = (p - 1) * (q - 1)
    print("求出n的欧拉函数φ(n):")
    print("φ(n) =", phi_n)

    e = calculate_e(phi_n)
    print("求出公钥(e, n)中的e:")
    print("e =", e)

    d = extended_euclid(phi_n, e)
    print("求出私钥(d, n)中的d:")
    print("d =", d)

    # 密文进行分组时每组的大小
    # 保险起见，设定为一个大于log2(n)的整数
    cipher_group_size = int(math.log(n) / math.log2(2)) + 1

    # 对明文进行编码，得到全为4位十进制数的列表
    plain_int_list = encode_text(plain_text)

    # 加密过程
    print("正在根据公钥(e, n)对明文进行加密......")
    cipher_int_list = encrypt(plain_int_list, e, n)
    # 将加密得到的cipher_int_list转化为一个只包含0-9的字符串
    cipher_string = int2string(cipher_int_list, cipher_group_size)
    # 1个字符对应1个ascii值进行解码，得到密文字符串cipher_text
    cipher_text = "".join([chr(num + offset) for num in string2int(cipher_string, 1)])
    print("加密成功！得到密文如下:")
    print(cipher_text)
    with open("encrypted-text.txt", "w", encoding="utf-8") as fout1:
        fout1.write(cipher_text)
        fout1.close()
    print("该密文已经被同时写入到文件encrypted-text.txt中")

    # 解密过程
    print("现在开始解密，从文件encrypted-text.txt中读入密文")
    with open("encrypted-text.txt", "r", encoding="utf-8") as fin2:
        cipher_text_from_file = fin2.read()
        fin2.close()
    cipher_string_from_file = int2string([(ord(ch) - offset) for ch in cipher_text_from_file], 1)
    cipher_int_list_from_file = string2int(cipher_string_from_file, cipher_group_size)
    # 根据私钥(d, n)对密文进行解密，得到decipher_int_list
    print("正在根据私钥(d, n)对密文进行解密......")
    decipher_int_list = decrypt(cipher_int_list_from_file, d, n)
    decipher_text = decode_text(decipher_int_list)
    print("解密成功！得到明文如下:")
    print(decipher_text)
    with open("decrypted-text.txt", "w", encoding="utf-8") as fout2:
        fout2.write(decipher_text)
        fout2.close()
    print("该明文已经被同时写入到文件decrypted-text.txt中")
