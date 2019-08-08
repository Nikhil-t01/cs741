#My AES implementation
# By Daniel Miller
# https://gist.github.com/bonsaiviking/5571001

def xor(s1, s2):
    return tuple(a^b for a,b in zip(s1, s2))

class AES(object):
    class __metaclass__(type):
        def __init__(cls, name, bases, classdict):
            cls.Gmul = {}
            for f in (0x2, 0x3, 0xe, 0xb, 0xd, 0x9):
                cls.Gmul[f] = tuple(cls.gmul(f, x) for x in range(0,0x10))

# [1, 2, 4, 8, 3, 6, 12, 11, 5, 10, 7, 14, 15, 13, 9]
    Rcon = ( None, 0x1, 0x2, 0x4, 0x8, 0x3, 0x6, 0xc, 0xb, 0x5, 0xa, 0x7, 0xe, 0xf, 0xd, 0x9 )
    Sbox = (0x6, 0xb, 0x5, 0x4, 0x2, 0xe, 0x7, 0xa, 0x9, 0xd, 0xf, 0xc, 0x3, 0x1, 0x0, 0x8)
    Sbox_inv = (0xe, 0xd, 0x4, 0xc, 0x3, 0x2, 0x0, 0x6, 0xf, 0x8, 0x7, 0x1, 0xb, 0x9, 0x5, 0xa)

    def get_sbox(self, i):
        return AES.Sbox[i]

    def get_inv_sbox(self, i):
        return AES.Sbox_inv[i]

    @staticmethod
    def rot_word(word):
        return word[1:] + word[:1]

    @staticmethod
    def sub_word(word):
        return (AES.Sbox[b] for b in word)

    def key_schedule(self):
        expanded = []
        expanded.extend(map(ord, self.key))
        for i in range(self.nk, self.nb * (self.nr + 1)):
            t = expanded[(i-1)*4:i*4]
            if i % self.nk == 0:
                t = xor( AES.sub_word( AES.rot_word(t) ), (AES.Rcon[i // self.nk],0,0,0) )
            elif self.nk > 6 and i % self.nk == 4:
                t = AES.sub_word(t)
            expanded.extend( xor(t, expanded[(i-self.nk)*4:(i-self.nk+1)*4]))
        return expanded

    def add_round_key(self, rkey):
        for i, b in enumerate(rkey):
            self.state[i] ^= b

    def sub_bytes(self):
        for i, b in enumerate(self.state):
            self.state[i] = AES.Sbox[b]

    def inv_sub_bytes(self):
        for i, b in enumerate(self.state):
            self.state[i] = AES.Sbox_inv[b]

    def shift_rows(self):
        rows = []
        for r in range(4):
            rows.append( self.state[r::4] )
            rows[r] = rows[r][r:] + rows[r][:r]
        self.state = [ r[c] for c in range(4) for r in rows ]

    def inv_shift_rows(self):
        rows = []
        for r in range(4):
            rows.append( self.state[r::4] )
            rows[r] = rows[r][4-r:] + rows[r][:4-r]
        self.state = [ r[c] for c in range(4) for r in rows ]

    @staticmethod
    def gmul(a, b):
        p = 0
        for c in range(4):
            if b & 1:
                p ^= a
            a <<= 1
            if a & 0x10:
                a ^= 0x13
            b >>= 1
        return p

    def mix_columns(self):
        ss = []
        for c in range(4):
            col = self.state[c*4:(c+1)*4]
            ss.extend((
                        AES.Gmul[0x2][col[0]]  ^ AES.Gmul[0x3][col[1]] ^                col[2]  ^                col[3] ,
                                       col[0]  ^ AES.Gmul[0x2][col[1]] ^ AES.Gmul[0x3][col[2]]  ^                col[3] ,
                                       col[0]  ^                col[1] ^ AES.Gmul[0x2][col[2]]  ^  AES.Gmul[0x3][col[3]],
                        AES.Gmul[0x3][col[0]]  ^                col[1] ^                col[2]  ^  AES.Gmul[0x2][col[3]],
                    ))
        self.state = ss

    def inv_mix_columns(self):
        ss = []
        for c in range(4):
            col = self.state[c*4:(c+1)*4]
            ss.extend((
                        AES.Gmul[0xe][col[0]] ^ AES.Gmul[0xb][col[1]] ^ AES.Gmul[0xd][col[2]] ^ AES.Gmul[0x9][col[3]],
                        AES.Gmul[0x9][col[0]] ^ AES.Gmul[0xe][col[1]] ^ AES.Gmul[0xb][col[2]] ^ AES.Gmul[0xd][col[3]],
                        AES.Gmul[0xd][col[0]] ^ AES.Gmul[0x9][col[1]] ^ AES.Gmul[0xe][col[2]] ^ AES.Gmul[0xb][col[3]],
                        AES.Gmul[0xb][col[0]] ^ AES.Gmul[0xd][col[1]] ^ AES.Gmul[0x9][col[2]] ^ AES.Gmul[0xe][col[3]],
                    ))
        self.state = ss

    def cipher(self, block):
        n = self.nb * 4
        self.state = map(ord, block)
        keys = self.key_schedule()
        self.add_round_key(keys[0:n])
        for r in range(1, self.nr):

            self.sub_bytes()
            self.shift_rows()
            self.mix_columns()
            k = keys[r*n:(r+1)*n]
            self.add_round_key(k)

        self.sub_bytes()
        self.shift_rows()
        if self.mc: self.mix_columns()

        self.add_round_key(keys[self.nr*n:])
        return "".join(map(chr, self.state))

    def inv_cipher(self, block):
        n = self.nb * 4
        self.state = map(ord, block)
        keys = self.key_schedule()
        k = keys[self.nr*n:(self.nr+1)*n]
        self.add_round_key(k)
        if self.mc: self.inv_mix_columns()
        
        for r in range(self.nr-1, 0, -1):

            self.inv_shift_rows()
            self.inv_sub_bytes()
            k = keys[r*n:(r+1)*n]
            self.add_round_key(k)
            self.inv_mix_columns()

        self.inv_shift_rows()
        self.inv_sub_bytes()
        self.add_round_key(keys[0:n])

        return "".join(map(chr, self.state))



class AES_128(AES):
    def __init__(self, nr, mc=False):
        self.nb = 4
        self.nr = nr
        self.nk = 4
        self.mc = mc

if __name__=="__main__":
    # key = "2b7e151628aed2a6abf7158809cf4f3c".decode('hex')
    key = "000102030404060708090a0b000d0e0f".decode('hex')
    # check = (
    #         #("00112233445566778899aabbccddeeff", "69c4e0d86a7b0430d8cdb78070b4c55a"),
    #         ("6bc1bee22e409f96e93d7e117393172a", "3ad77bb40d7a3660a89ecaf32466ef97"),
    #         ("ae2d8a571e03ac9c9eb76fac45af8e51", "f5d3d58503b9699de785895a96fdbaaf"),
    #         ("30c81c46a35ce411e5fbc1191a0a52ef", "43b1cd7f598ece23881b00e3ed030688"),
    #         ("f69f2445df4f9b17ad2b417be66c3710", "7b0c785e27e8ad3f8223207104725dd4"),
    #         )
    crypt = AES_128(5)
    crypt.key = key
    print(len(crypt.key_schedule()))
    pl = "0f0e0d0c0a0a0908070a05040a02010a".decode('hex')
    cp = crypt.cipher(pl)
    print(pl.encode('hex'))
    print(crypt.inv_cipher(cp).encode('hex'))

    # for c in check:
    #     p = c[0].decode('hex')
    #     v = c[1].decode('hex')
    #     t = crypt.cipher(p)
    #     if t == v:
    #         print("yay!")
    #     else:
    #         print("{0} != {1}".format(t.encode('hex'), c[1]))
    #     t = crypt.inv_cipher(v)
    #     if t == p:
    #         print("yay!")
    #     else:
    #         print("{0} != {1}".format(t.encode('hex'), c[1]))