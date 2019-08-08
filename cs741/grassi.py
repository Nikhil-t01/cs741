import random
import sys
sys.path.append('./')

from aes import AES_128

def get_goodpairs(key):
	crypt = AES_128(5)
	crypt.key = key

	x = [chr(i) for i in range(256)]
	var = chr(0)
	pl1 = [var for _ in range(16)]
	pl2 = [var for _ in range(16)]


	for i1 in range(1, 256):
		for i2 in range(i1+1, 256):
			for j1 in range(1, 256):
				for j2 in range(j1+1,256):
					for k1 in range(1, 256):
						for k2 in range(k1+1,256):
							for l1 in range(1, 256):
								for l2 in range(l1+1,256):
									pl2[0], pl2[5], pl2[10], pl2[15] = x[i2], x[j2], x[k2], x[l2]
									pl1[0], pl1[5], pl1[10], pl1[15] = x[i1], x[j1], x[k1], x[l1]
									
									c1 = crypt.cipher(''.join(pl1))
									c2 = crypt.cipher(''.join(pl2))

									if ((c1[0]==c2[0]) and (c1[7]==c2[7]) and (c1[10]==c2[10]) and (c1[13]==c2[13])):
										if pl1 == pl2:
											print("Something wrong")
											return None, None
										return pl1, pl2

key = "2b7e151628aed2a6abf7158809cf4f3c".decode('hex')
p1, p2 = get_goodpairs(key)
print(p1,p2)
print("Original ", key[0], key[5], key[10], key[15])


keys_0, keys_5, keys_10, keys_15 = [], [], [], []
for k in range(0, 256):
	keys_0.append(k)
	keys_5.append(k)
	keys_10.append(k)
	keys_15.append(k)

for k0 in keys_0:
	for k5 in keys_5:
		for k10 in keys_10:
			for k15 in keys_15:
				key_guess = [chr(k0)] + [chr(0)]*4 + [chr(k5)] + [chr(0)]*4 + [chr(k10)] + [chr(0)]*4 + [chr(k15)]
				one_round_crypt = AES_128(1, True)
				one_round_crypt.key = key_guess
				xp = one_round_crypt.cipher(''.join(p1))
				yp = one_round_crypt.cipher(''.join(p2))

				crypt = AES_128(5)
				crypt.key = key_guess

				flag = 1

				if flag:
					zp = list(xp[:])
					wp = list(yp[:])
					zp[4]  = yp[4]
					zp[12] = yp[12]
					wp[4]  = xp[4]
					wp[12] = xp[12]

					p3 = one_round_crypt.inv_cipher(''.join(zp))
					p4 = one_round_crypt.inv_cipher(''.join(wp))
					c3 = crypt.cipher(''.join(p3))
					c4 = crypt.cipher(''.join(p4))

					flag = ((c3[0]==c4[0]) and (c3[7]==c4[7]) and (c3[10]==c4[10]) and (c3[13]==c4[13])) or ((c3[1]==c4[1]) and (c3[4]==c4[4]) and (c3[11]==c4[11]) and (c3[14]==c4[14])) or ((c3[2]==c4[2]) and (c3[5]==c4[5]) and (c3[8]==c4[8]) and (c3[15]==c4[15])) or	((c3[3]==c4[3]) and (c3[6]==c4[6]) and (c3[9]==c4[9]) and (c3[12]==c4[12]))

				if flag:
					zp = list(xp[:])
					wp = list(yp[:])
					zp[4]  = yp[4]
					zp[8]  = yp[8]
					wp[4]  = xp[4]
					wp[8]  = xp[8]

					p3 = one_round_crypt.inv_cipher(''.join(zp))
					p4 = one_round_crypt.inv_cipher(''.join(wp))
					c3 = crypt.cipher(''.join(p3))
					c4 = crypt.cipher(''.join(p4))

					flag = ((c3[0]==c4[0]) and (c3[7]==c4[7]) and (c3[10]==c4[10]) and (c3[13]==c4[13])) or ((c3[1]==c4[1]) and (c3[4]==c4[4]) and (c3[11]==c4[11]) and (c3[14]==c4[14])) or ((c3[2]==c4[2]) and (c3[5]==c4[5]) and (c3[8]==c4[8]) and (c3[15]==c4[15])) or	((c3[3]==c4[3]) and (c3[6]==c4[6]) and (c3[9]==c4[9]) and (c3[12]==c4[12]))

				if flag:
					zp = list(xp[:])
					wp = list(yp[:])
					zp[8]  = yp[8]
					zp[12] = yp[12]
					wp[8]  = xp[8]
					wp[12] = xp[12]

					p3 = one_round_crypt.inv_cipher(''.join(zp))
					p4 = one_round_crypt.inv_cipher(''.join(wp))
					c3 = crypt.cipher(''.join(p3))
					c4 = crypt.cipher(''.join(p4))

					flag = ((c3[0]==c4[0]) and (c3[7]==c4[7]) and (c3[10]==c4[10]) and (c3[13]==c4[13])) or ((c3[1]==c4[1]) and (c3[4]==c4[4]) and (c3[11]==c4[11]) and (c3[14]==c4[14])) or ((c3[2]==c4[2]) and (c3[5]==c4[5]) and (c3[8]==c4[8]) and (c3[15]==c4[15])) or	((c3[3]==c4[3]) and (c3[6]==c4[6]) and (c3[9]==c4[9]) and (c3[12]==c4[12]))

				if flag:
					zp = list(xp[:])
					wp = list(yp[:])
					zp[0]  = yp[0]
					wp[0]  = xp[0]

					p3 = one_round_crypt.inv_cipher(''.join(zp))
					p4 = one_round_crypt.inv_cipher(''.join(wp))
					c3 = crypt.cipher(''.join(p3))
					c4 = crypt.cipher(''.join(p4))

					flag = ((c3[0]==c4[0]) and (c3[7]==c4[7]) and (c3[10]==c4[10]) and (c3[13]==c4[13])) or ((c3[1]==c4[1]) and (c3[4]==c4[4]) and (c3[11]==c4[11]) and (c3[14]==c4[14])) or ((c3[2]==c4[2]) and (c3[5]==c4[5]) and (c3[8]==c4[8]) and (c3[15]==c4[15])) or	((c3[3]==c4[3]) and (c3[6]==c4[6]) and (c3[9]==c4[9]) and (c3[12]==c4[12]))

				if flag:
					zp = list(xp[:])
					wp = list(yp[:])
					zp[8]  = yp[8]
					wp[8]  = xp[8]

					p3 = one_round_crypt.inv_cipher(''.join(zp))
					p4 = one_round_crypt.inv_cipher(''.join(wp))
					c3 = crypt.cipher(''.join(p3))
					c4 = crypt.cipher(''.join(p4))

					flag = ((c3[0]==c4[0]) and (c3[7]==c4[7]) and (c3[10]==c4[10]) and (c3[13]==c4[13])) or ((c3[1]==c4[1]) and (c3[4]==c4[4]) and (c3[11]==c4[11]) and (c3[14]==c4[14])) or ((c3[2]==c4[2]) and (c3[5]==c4[5]) and (c3[8]==c4[8]) and (c3[15]==c4[15])) or	((c3[3]==c4[3]) and (c3[6]==c4[6]) and (c3[9]==c4[9]) and (c3[12]==c4[12]))

				if flag:
					zp = list(xp[:])
					wp = list(yp[:])
					zp[4]  = yp[4]
					wp[4]  = xp[4]

					p3 = one_round_crypt.inv_cipher(''.join(zp))
					p4 = one_round_crypt.inv_cipher(''.join(wp))
					c3 = crypt.cipher(''.join(p3))
					c4 = crypt.cipher(''.join(p4))

					flag = ((c3[0]==c4[0]) and (c3[7]==c4[7]) and (c3[10]==c4[10]) and (c3[13]==c4[13])) or ((c3[1]==c4[1]) and (c3[4]==c4[4]) and (c3[11]==c4[11]) and (c3[14]==c4[14])) or ((c3[2]==c4[2]) and (c3[5]==c4[5]) and (c3[8]==c4[8]) and (c3[15]==c4[15])) or	((c3[3]==c4[3]) and (c3[6]==c4[6]) and (c3[9]==c4[9]) and (c3[12]==c4[12]))

				if flag:
					zp = list(xp[:])
					wp = list(yp[:])
					zp[12] = yp[12]
					wp[12] = xp[12]

					p3 = one_round_crypt.inv_cipher(''.join(zp))
					p4 = one_round_crypt.inv_cipher(''.join(wp))
					c3 = crypt.cipher(''.join(p3))
					c4 = crypt.cipher(''.join(p4))

					flag = ((c3[0]==c4[0]) and (c3[7]==c4[7]) and (c3[10]==c4[10]) and (c3[13]==c4[13])) or ((c3[1]==c4[1]) and (c3[4]==c4[4]) and (c3[11]==c4[11]) and (c3[14]==c4[14])) or ((c3[2]==c4[2]) and (c3[5]==c4[5]) and (c3[8]==c4[8]) and (c3[15]==c4[15])) or	((c3[3]==c4[3]) and (c3[6]==c4[6]) and (c3[9]==c4[9]) and (c3[12]==c4[12]))

				if flag:
					print("Found ", key_guess[0], key_guess[5], key_guess[10], key_guess[15])
				# 					break