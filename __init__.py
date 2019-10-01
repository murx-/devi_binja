from binaryninja import PluginCommand
from binaryninja import interaction
from binaryninja import InstructionTextTokenType
from binaryninja import demangle
from binaryninja import log
import json

class binja_devi():

    def __init__(self, bv):
        self.bv = bv
        self.call_cnt = 0
        self.load_virtual_calls()


    def load_virtual_calls(self):
        json_file = interaction.get_open_filename_input("Load virtual calls", "*.json")
        with open(json_file.decode("utf-8")) as f:
            json_objects = json.load(f)
        self.devirtualize_calls(json_objects["calls"])

    def devirtualize_calls(self, call_list):
        for v_call in call_list:
            for call in v_call:
                to_addr = int(v_call[call])
                #print(hex(int(call)))
                #print(hex(to_addr))
                from_addr = int(call)
                self.caller = self.bv.get_functions_containing(from_addr)[0]
                self.caller.add_user_code_ref(from_addr, to_addr, from_arch=None)
                self.add_call_comment(from_addr, to_addr)
                self.call_cnt += 1
        log.log(1, "Devirtualized {} calls".format(self.call_cnt))
                

    def add_call_comment(self, from_addr, to_addr):
        to_func = self.bv.get_function_at(to_addr)
        _, name = demangle.demangle_gnu3(self.bv.arch, to_func.name)
        old_comment = self.caller.get_comment_at(from_addr)
        self.caller.set_comment_at(from_addr, demangle.get_qualified_name(name) + "\n" + old_comment)

PluginCommand.register("devi", "DEvirtualize VIrtual calls", binja_devi)