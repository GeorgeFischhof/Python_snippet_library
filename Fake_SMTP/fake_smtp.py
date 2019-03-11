
import asyncore
import datetime
import os
import re
from smtpd import SMTPServer
import subprocess


def get_compact_canonical_time_stamp() -> str:
    now = datetime.datetime.now()
    time_stamp = now.strftime('%Y%m%d_%H%M%S')
    return time_stamp


def get_mac_from_ip(ip_address):
    try:
        output = subprocess.check_output(['arp', '-a', ip_address], encoding='utf-8')
        mac = re.search('([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', output).group()
        mac = mac.replace('-', '')
        mac = mac.replace(':', '')
    except:
        mac = 'NO_MAC_FOUND'
    return mac


def get_existing_folder_with_substring(root_folder, substring):
    existing_folder_name = ''
    for dir_path, dir_names, file_names in os.walk(root_folder):
        for name in dir_names:
            if substring.upper() in name.upper():
                existing_folder_name = dir_path + name
    return existing_folder_name


def create_dir(dir_name):
    dir_name = os.path.dirname(dir_name)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    return


class FakeSMTPServer(SMTPServer):

    def process_message(self, peer, mail_sender, recipients, data, *args, **kwargs):
        peer_address, peer_port = peer[0], peer[1]
        remote_mac = (get_mac_from_ip(peer_address)).upper()
        time_stamp = get_compact_canonical_time_stamp()

        base_path = self.calculate_base_path(remote_mac)
        file_name = base_path + time_stamp + '_' + remote_mac + '_' + mail_sender + '.eml'

        create_dir(base_path)
        self.write_email_to_file(data, file_name)
        return

    def calculate_base_path(self, remote_mac):
        base_path = get_existing_folder_with_substring(root_folder='/Samba/', substring=remote_mac)
        if base_path == '':
            base_path = '/Samba/' + remote_mac
        base_path += '/Email/'
        return base_path

    def write_email_to_file(self, data, file_name):
        with open(file_name, mode='w', encoding='utf-8') as email_file:
            email_file.write(data)


if __name__ == '__main__':
    smtp_server = FakeSMTPServer(('0.0.0.0', 25), None, decode_data=True)
    asyncore.loop()
