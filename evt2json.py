#!/usr/bin/env python3 -tt
import argparse, json, os, re, shutil, subprocess, sys

parser = argparse.ArgumentParser()
parser.add_argument("directory", nargs="+", help="Source directory where EVT/EVTX files are located.")
parser.add_argument("-v", "--verbose", help="Show logging", action='store_const', const=True, default=False)
args = parser.parse_args()
directory, verbose = args.directory, args.verbose
d = directory[0]


def main():
    evtxdumppath = str(subprocess.Popen(["locate", "evtx_dump.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate())[3::].split("evtx_dump.py")[0]
    if evtxdumppath != "":
        if not os.path.exists(d):
            print("\n    '{}' is not a valid directory. Please try again.\n\n")
            sys.exit()
        else:
            print("\n")
            for root, dirs, files in os.walk(d):
                for eachfile in files:
                    evtfile, jsondict, jsonlist, evtjsonlist = os.path.join(root, eachfile), {}, [], []
                    if evtfile.endswith(".evtx"):
                        if verbose:
                            print("  Processing '{}'...".format(eachfile))
                        else:
                            pass
                        with open(os.path.join(root, eachfile)+".json", "a") as evtjson:
                            evtout = str(subprocess.Popen([os.path.join(evtxdumppath, "evtx_dump.py"), evtfile], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate())[3:-9]
                            for event in evtout.split("\\r\\n"):
                                if event != "<?xml version=\"1.1\" encoding=\"utf-8\" standalone=\"yes\" ?>\\n\\n<Events>\\n</Events>":
                                    for evtrow in event.split("\\n"):
                                        for eachkv in re.findall(r"(?:\ (?P<k1>(?!Name)[^\=]+)\=\"(?P<v1>[^\"]+)\"|\<(?P<k2>[^\>\/\=\ ]+)(?:\ \D+\=\"\"\>|\=\"|\>)(?P<v2>[^\"\>]+)(?:\"\>)?\<\/[^\>]+\>|\<Data\ Name\=\"(?P<k3>[^\"]+)\"\>(?P<v3>[^\<]+)\<\/Data\>)", evtrow):
                                            kv = list(filter(None, eachkv))
                                            if len(kv) > 0:
                                                jsondict[kv[0]] = kv[1]
                                            else:
                                                pass
                                    if len(jsondict) > 0:
                                        jsonlist.append(json.dumps(jsondict))
                                    else:
                                        pass
                                else:
                                    pass
                            for eachjson in jsonlist:
                                try:
                                    eachjson = str(eachjson).replace("\"\"","\"-\"")
                                    if "\"RegistryKey\"" in eachjson:
                                        insert = ", \"Registry{}".format(str(str(re.findall(r"RegistryKey(\"\: \"[^\"]+\")", eachjson)[0]).lower()).replace(" ","_").replace("\":_\"","\": \""))
                                        evtjsonlist.append(json.dumps(eachjson[0:-1]+insert+"}"))
                                    else:
                                        evtjsonlist.append(json.dumps(eachjson))
                                except:
                                    pass
                            if len(evtjsonlist) > 0:
                                evtjson.write(str(evtjsonlist).replace("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\","/").replace("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\","/").replace("\\\\\\\\\\\\\\\\","/").replace("\\\\\\\\","/").replace("\\\\","/").replace("\\","/").replace("/\"","\"").replace("                                                                "," ").replace("                                "," ").replace("                "," ").replace("        "," ").replace("    "," ").replace("  "," ").replace("  ","").replace("\" ","\"").replace(" \"","\"").replace("//'","'").replace("\":\"","\": \"").replace("\",\"","\", \"").replace("\"}\"', '\"{\"","\"}, {\"").replace("['\"{\"","[{\"").replace("\"}\"']","\"}]"))
                            else:
                                pass
                            evtjsonlist.clear()
                            jsonlist.clear()
                    else:
                        pass
                    if verbose:
                        print("   Completed '{}'.\n".format(eachfile))
                    else:
                        pass
            for doneroot, donedirs, donefiles in os.walk(d):
                for donefile in donefiles:
                    if os.path.exists(os.path.join(doneroot, donefile)):
                        if os.stat(os.path.join(doneroot, donefile)).st_size <= 10:
                            try:
                                os.remove(os.path.join(doneroot, donefile))
                            except:
                                pass
                        else:
                            pass
                    else:
                        pass
    else:
        print("\n\n\n\n")

if __name__ == '__main__':
	main()
