from Robot import oRobot, baslangic, tum_eklentiler, bilgi

baslangic()

eklentiler = ""
j = 1
for i in tum_eklentiler:
    if j == 3:
        eklentiler += "| {:<18} |\n".format(i) if len(tum_eklentiler) != 3 else "| {:<18} |".format(i)
        j = 0
    else:
        eklentiler += "| {:<18}".format(i)
    j += 1

bilgi("+===============================================================+")
bilgi("|                       Eklentilerim                            |")
bilgi("+===============+===============+===============+===============+")
bilgi(f"{eklentiler}")
bilgi("+===============+===============+===============+===============+\n")

if __name__ == "__main__":
    oRobot.run()