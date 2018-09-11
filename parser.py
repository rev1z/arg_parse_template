import argparse
import socket
import sys


class CliParser:
    """
    Парсер аргументов командной строки.
    возвращает словарь вида

    {'command': 'command1', 'component': 'component2', 'target': 127.0.0.1}
    """
    __choices = ["all"
                 "component1",
                 "component2",
                 "component3"]

    def __get_parser(self):

        parser = argparse.ArgumentParser(description="Some fancy description", allow_abbrev=False)
        parser.add_argument('-c', dest='command', help="command type", choices=["command1", "command1", "command1"],
                            required=True)
        parser.add_argument('-p', dest="component", help="component to chose", choices=self.__choices, default="all")
        parser.add_argument('-t', dest="target", help="target IP address")

        if len(sys.argv) <= 1:
            sys.argv.append('-h')

        return parser

    def get_params(self):
        parser = self.__get_parser()
        dic_ = parser.parse_args().__dict__

        return dic_

    def process_params(self):
        params = self.get_params()
        err_msg_list = []

        def __check_ip(ip_str):
            try:
                socket.inet_aton(ip_str)
            except socket.error:
                err = f'Incorrect IP address string: {ip_str}'
                return err
            return None

        if not params['command']:
            err_msg_list.append("Need to specify command for execution")

        if not params['target']:
            err_msg_list.append("Need to provide target IP.")

        if params["target"]:
            msg = __check_ip(params["target"])
            if msg:
                err_msg_list.append(msg)

        if err_msg_list:
            err_msg_list.append("Use -h for help")
            print("\n".join(err_msg_list))
            quit()

        params_to_execute = {}
        for elem in params:
            if params[elem]:
                params_to_execute[elem] = params[elem]

        return params_to_execute
