from temperature import is_overheating

temp = float(input("Ingrese temperatura: "))

if is_overheating(temp):
	print("⚠️ ALARMA: Temperatura alta")
else:
	print("✅ Temperatura normal")
