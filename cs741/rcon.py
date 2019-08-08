def rc(i):
	if i == 1: return 1
	else:
		k = rc(i-1)
		if k < 8: return 2*k
		else: return (2*k)^(3+16)

rcon = [rc(i) for i in range(1, 16)]
print("Round constants when 4 bits used instead of 1 byte, with irreducible polynomial 0x13")
print(rcon)
