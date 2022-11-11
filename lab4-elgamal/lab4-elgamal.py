import random


def pow_mod(a, b, c):
    """
    快速幂算法求解a的b次方模c
    :param a: 底数
    :param b: 指数
    :param c: 模数
    :return: a的b次方模c
    """
    ans = 1
    a = a % c
    while b > 0:
        if b & 1 == 1:
            ans = (ans * a) % c
        b = b >> 1
        a = (a * a) % c
    return ans


def miller_rabin(n):
    """
    Miller-Rabin算法
    :param n: 需要判定的数
    :return: 返回True，很可能为素数；返回False，不是素数
    """
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


def generate_big_num(digit):
    """
    生成一个大数(不一定是质数，有待后续判断)，所生成大数的二进制长度为digit
    :param digit: 二进制位数
    :return: 生成的大数
    """
    num = 0
    for i in range(digit):
        num = num * 2 + random.randint(0, 1)
    return num


def generate_big_prime_num(digit):
    """
    生成一个大质数(使用Miller-Rabin算法判断)，所生成大数的二进制长度为digit
    :param digit: 二进制位数
    :return: 生成的大质数
    """
    p = generate_big_num(digit)
    while not miller_rabin(p):
        p += 1
    return p


def calc_primitive_root(digit=256):
    """
    随机生成一个大质数p，并求出其本原根g
    :param digit: 二进制位数，默认为256
    :return: (p, g)
    """
    while True:
        q = generate_big_prime_num(digit)
        p = 2 * q + 1
        if miller_rabin(p):
            break
    g = random.randint(2, p - 2)
    while (pow_mod(g, 2, p) == 1) or (pow_mod(q, 2, p) == 1):
        q = random.randint(2, p - 2)
    return p, g


def euclid(a, b):
    """
    欧几里得算法，求出a和b的最大公因数
    :param a: 数a
    :param b: 数b
    :return: a和b的最大公因数
    """
    x = a
    y = b
    while y != 0:
        r = x % y
        x = y
        y = r
    return x


def generate_k(p):
    """
    为每次签名生成随机整数k
    :param p: 签名所用的大素数p
    :return: 本次签名生成的随机整数k
    """
    k = random.randint(1, p - 1)
    # k应当满足gcd(k, p-1) = 1
    while euclid(k, p - 1) != 1:
        k += 1
    return k


def extended_euclid(a, b):
    """
    扩展欧几里得算法，求出b在模a下的乘法逆元
    :param a: 数a
    :param b: 数b
    :return: b在模a下的乘法逆元
    """
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


def sign_message(p, g, x, k, m):
    """
    对消息m进行签名
    :param p: 随机生成的大素数
    :param g: p对应的本原根
    :param x: 私钥
    :param k: 本次签名所用的随机整数k
    :param m: 待签名的消息
    :return: 消息m的签名(r, s)
    """
    r = pow_mod(g, k, p)
    # 求出k mod (p - 1)的逆
    k_inverse = extended_euclid(p - 1, k)
    s = k_inverse * (m - x * r) % (p - 1)
    return r, s


def verify_signature(p, g, y, r, s, m):
    """
    对数字签名进行验证
    :param p: 随机生成的大素数
    :param g: p对应的本原根
    :param y: 公钥(p, g, y)中的y
    :param r: 签名(r, s)中的r
    :param s: 签名(r, s)中的s
    :return: 是否通过验证(True: 通过验证, False: 不通过验证)
    """
    lhs = pow_mod(y, r, p) * pow_mod(r, s, p) % p
    rhs = pow_mod(g, m, p)
    print(f"(y的r次方)乘以(r的s次方)模p的结果为{lhs}")
    print(f"g的m次方模p的结果为{rhs}")
    if lhs == rhs:
        return True
    else:
        return False


def run_once(x, p, g, y, m):
    """
    进行一轮签名及验证，并考虑消息m被篡改的情况
    :param x: 私钥
    :param p: 公钥(p, g, y)中的p
    :param g: 公钥(p, g, y)中的g
    :param y: 公钥(p, g, y)中的y
    :param m: 待签名的消息m
    :return: 无返回值，会在控制台打印运行信息
    """
    k = generate_k(p)
    print(f"本次签名所使用的随机整数k为{k}")
    r, s = sign_message(p, g, x, k, m)
    print(f"消息m = {m}的签名为:\n(r, s) = ({r}, {s})")
    print(f"现在对上述消息m、签名(r, s)进行验证:")
    if verify_signature(p, g, y, r, s, m):
        print("两者相等，签名验证通过！")
    else:
        print("两者不相等，签名验证不通过！")
    m_new = m // 2 + random.randint(0, m)
    print(f"现在假设消息m由{m}被篡改为{m_new}，重新对消息m、签名(r, s)进行验证:")
    if verify_signature(p, g, y, r, s, m_new):
        print("两者相等，签名验证通过！")
    else:
        print("两者不相等，签名验证不通过！由此可见通过验证签名的方式确实能检测到消息m被篡改的情况。")
    print("")


if __name__ == "__main__":
    print("正在生成二进制位数为256的质数p及其本原根g......")
    p, g = calc_primitive_root()
    print("生成完毕！\np = {}, g = {}".format(p, g))
    # 随机选择一个x作为私钥(1 < x < p - 1)
    x = random.randint(2, p - 1)
    # y为g的x次方模p
    y = pow_mod(g, x, p)
    print(f"私钥为x = {x}, 公钥为(p, g, y) = ({p}, {g}, {y})")
    m = 200110119
    print(f"待签名的消息为m = {m}")
    print("-----------------------------------第一次签名及验证签名-----------------------------------")
    run_once(x, p, g, y, m)
    print("-----------------------------------第二次签名及验证签名-----------------------------------")
    run_once(x, p, g, y, m)
