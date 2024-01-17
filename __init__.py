from binaryninja import PluginCommand
from binaryninja import interaction
from binaryninja import InstructionTextTokenType
from binaryninja import demangle
from binaryninja import log
import json
import traceback
import os

class binja_devi():

    def __init__(self, bv):
        self.version = 0.2
        self.bv = bv
        self.call_cnt = 0
        self.load_virtual_calls()


    def load_virtual_calls(self):
        json_file = interaction.get_open_filename_input("Load virtual calls", "*.json")
        with open(json_file.decode("utf-8")) as f:
            devi_json_data = json.load(f)
                
        if self.version < devi_json_data["deviVersion"]:
            print("[!] devi JSON file has a more recent version than IDA plugin!")
            print("[!] we try parsing anyway!")
        if self.version > devi_json_data["deviVersion"]:
            print("[!] Your devi_ida and devi_frida versions are out of sync. Update your devi_ida!")

        if self.version == devi_json_data["deviVersion"]:
            self.devirtualize_calls(devi_json_data["calls"], devi_json_data["modules"])
        elif devi_json_data["deviVersion"] == 0.1:
            self.devirtualize_calls_v01(devi_json_data["calls"])


    def devirtualize_calls(self, call_list, modules):
        binja_filename = os.path.basename(self.bv.file.filename)

        for module in modules:
            if module["name"] == binja_filename:
                loaded_module = module
                break
        
        start = int(loaded_module["base"], 16)
        end = start + loaded_module["size"]

        print("[!] Adding virtual calls for {binja_filename}")

        for v_call in call_list:
            for call in v_call:
                if start <= int(call, 16) <= end:

                    src = int(call, 16) - start
                    dst = int(v_call[call]) - start

                    self.caller = self.bv.get_functions_containing(src)[0]
                    self.caller.add_user_code_ref(src, dst, from_arch=None)
                    found = self.add_call_comment(src, dst)

                    if not found:
                        log.log(2, f"Out of module call: {call} -> {hex(int(v_call[call]))}")
                    self.call_cnt += 1
        log.log(1, "Devirtualized {} calls".format(self.call_cnt))


    def devirtualize_calls_v01(self, call_list):
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
        if to_func is None:
            return False
        old_comment = self.caller.get_comment_at(from_addr)
        if to_func.name not in old_comment:
            self.caller.set_comment_at(from_addr, to_func.name + "\n" + old_comment)
        return True

PluginCommand.register("devi", "DEvirtualize VIrtual calls", binja_devi)
