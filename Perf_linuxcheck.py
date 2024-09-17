# -*- coding: utf-8 -*-
import subprocess

# chkrootkit taramasi
def run_chkrootkit():
    print("chkrootkit taramasi baslatiliyor...")
    try:
        result = subprocess.run(['sudo', 'chkrootkit'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout

        # Kotu amacli yazilim tespitlerini detayli goster
        infected_lines = [line for line in output.splitlines() if "INFECTED" in line or "PACKET SNIFFER" in line]
        
        if infected_lines:
            print("Kotu amacli yazilim bulundu!")
            for line in infected_lines:
                print(f"supheli bulgu: {line}")
        else:
            print("chkrootkit sonucu temiz.")
    except Exception as e:
        print(f"chkrootkit calistirilirken bir hata olustu: {str(e)}")

# rkhunter taramasi
def run_rkhunter():
    print("rkhunter taramasi baslatiliyor...")
    try:
        result = subprocess.run(['sudo', 'rkhunter', '--checkall', '--nocolors'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout
        
        # rkhunter uyarilari varsa goster
        if "Warning" in output:
            print("rkhunter uyarilari mevcut!")
            print(f"rkhunter tarama sonucu:\n{output}")
        else:
            print("rkhunter sonucu temiz.")
    except Exception as e:
        print(f"rkhunter calistirilirken bir hata olustu: {str(e)}")

# Potansiyel kotu yazilim tespiti (Silme yok, sadece uyari)
def detect_malware():
    print("Potansiyel kotu yazilimlar tespit ediliyor...")
    try:
        result = subprocess.run(['sudo', 'dpkg', '-l', 'apache2'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout
        if "apache2" in output:
            print("Uyari: Apache2 yuklu. Potansiyel bir risk olabilir.")
        else:
            print("Apache2 bulunamadi.")
    except Exception as e:
        print(f"Kotu yazilim tespiti sirasinda hata olustu: {str(e)}")

# Ag erisimleri ve portlari kontrol etme
def check_network_connections():
    print("Ag baglantilari ve acik portlar kontrol ediliyor...")
    
    try:
        result = subprocess.run(['sudo', 'ss', '-tuln'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout
        print("Aktif baglantilar (Portlar ve IP'ler):\n", output)
        
        # Potansiyel riskli portlar icin kontrol
        suspicious_ports = ['23', '2323', '8080']
        for line in output.splitlines():
            for port in suspicious_ports:
                if f":{port}" in line:
                    print(f"Uyari: Port {port} acik. Bu port zararli yazilim tarafindan kullanilabilir.")
    except Exception as e:
        print(f"Ag baglantilari kontrol edilirken hata olustu: {str(e)}")

# calisan servisleri kontrol etme
def check_running_services():
    print("calisan servisler kontrol ediliyor...")
    
    try:
        result = subprocess.run(['systemctl', 'list-units', '--type=service', '--state=running'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout
        print("calisan servisler:\n", output)
    except Exception as e:
        print(f"calisan servisleri kontrol ederken hata olustu: {str(e)}")

# Ana fonksiyon
def main():
    run_chkrootkit()
    run_rkhunter()
    check_network_connections()
    detect_malware()
    check_running_services()

if __name__ == "__main__":
    main()
