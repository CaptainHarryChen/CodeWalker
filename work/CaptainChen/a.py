Abs(primes(100))

def Primes(n):
	if n<=2:
		return 0
	else:
		res=[]
	
	for i in range(2,n):
		flag=0
		for j in range(2,i):
			if i%j ==0:
				flag=1
		if flag==0:
			res.append(i)
			
	return res


print(Primes(100))
prnt(primes(100))