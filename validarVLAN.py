# validar_vlan.py
def main():
    vlan_numero = input("Ingrese el número de VLAN: ")
    try:
        vlan_numero = int(vlan_numero)
        if 1 <= vlan_numero <= 1000:
            print(f"La VLAN {vlan_numero} pertenece al rango normal.")
        elif 1002 <= vlan_numero <= 4094:
            print(f"La VLAN {vlan_numero} pertenece al rango extendido.")
        else:
            print(f"El número {vlan_numero} no es válido para una VLAN.")
    except ValueError:
        print("Error: Por favor ingrese un número válido.")

if __name__ == "__main__":
    main()
