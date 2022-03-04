# """
# Search for a specific wifi ssid and connect to it.
# written by kasramvd.
# """
# import os

# from wifi import Cell, Scheme



#    # process netsh.stdout.


# class Finder:
#     def __init__(self, *args, **kwargs):
#         self.server_name = kwargs['server_name']
#         self.password = kwargs['password']
#         self.interface_name = kwargs['interface']
#         self.main_dict = {}

#     def run(self):
#         command = """sudo iwlist wlp2s0 scan | grep -ioE 'ssid:"(.*{}.*)'"""
#         result = os.popen(command.format(self.server_name))
#         result = list(result)

#         if "Device or resource busy" in result:
#             return None
#         else:
#             ssid_list = [item.lstrip('SSID:').strip('"\n') for item in result]
#             print("Successfully get ssids {}".format(str(ssid_list)))

#         for name in ssid_list:
#             try:
#                 result = self.connection(name)
#             except Exception as exp:
#                 print("Couldn't connect to name : {}. {}".format(name, exp))
#             else:
#                 if result:
#                     print("Successfully connected to {}".format(name))

#     def connection(self, name):
#         try:
#             os.system("nmcli d wifi connect {} password {} iface {}".format(name,
#                                                                             self.password,
#                                                                             self.interface_name))
#         except:
#             raise
#         else:
#             return True


# if __name__ == "__main__":
#     # Server_name is a case insensitive string, and/or regex pattern which demonstrates
#     # the name of targeted WIFI device or a unique part of it.
#     #get all cells from the air
#     ssids = [cell.ssid for cell in Cell.all('wlan0')]

#     schemes = list(Scheme.all())
#     print(schemes)
#     # for scheme in schemes:
#     #     ssid = scheme.options.get('wpa-ssid', scheme.options.get('wireless-essid'))
#     #     if ssid in ssids:
#     #         print(f'Connecting to {ssid}')
#     #         scheme.activate()
#     #         break

#     # server_name = "example_name"
#     # password = "your_password"
#     # interface_name = "your_interface_name"  # i. e wlp2s0
#     # F = Finder(server_name=server_name,
#     #         password=password,
#     #         interface=interface_name)
#     # F.run()
import subprocess

process = subprocess.Popen(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport','-I'], stdout=subprocess.PIPE)
out, err = process.communicate()
process.wait()
print(out)