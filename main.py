from gooey import Gooey, GooeyParser
import json
import os
import signal

from pull_updater import Updater

@Gooey(shutdown_signal=signal.CTRL_C_EVENT, show_stop_warning=False)
def main():
    # Clear older logs
    os.remove('logs.txt') if os.path.exists('logs.txt') else None
    # Load config
    defaults = {}
    try:
        if os.path.exists('.autopublish'):
            with open('.autopublish', 'r') as f:
                defaults = json.load(f)
        if os.path.exists(os.path.join("C:\\", "ProgramData", "autoupdater", ".autopublish.config")):
            with open(os.path.join("C:\\", "ProgramData", "autoupdater", ".autopublish.config"), 'r') as f:
                defaults.update(json.load(f))
    except Exception:
        pass
    parser = GooeyParser(description='Auto Publish')
    parser.add_argument('--URL', help='Remote Github URL', default=defaults.get('URL'))
    #parser.add_argument('--Wait', help='Wait duration (minutes)', type=int, default=defaults.get('Wait', 5))    
    parser.add_argument('Branch', help='Branch to watch', default=defaults.get('Branch', 'main'))
    parser.add_argument('Path', help='Project Folder', default=defaults.get('Path'), widget="FileChooser")
    # parser.add_argument('--Username', help='Git Username', default=defaults.get('Username'))
    # parser.add_argument('--Password', help='Git Password', default=defaults.get('Password'))
    args = parser.parse_args()
    for arg in args.__dict__:
        defaults[arg] = args.__dict__[arg]
    if "Path" in defaults:
        defaults["Path"] = os.path.abspath(defaults["Path"])
    os.makedirs(os.path.join("C:\\", "ProgramData", "autoupdater"), exist_ok=True)
    with open(os.path.join("C:\\", "ProgramData", "autoupdater", ".autopublish.config"), "w") as f:
        f.write(json.dumps({
            "URL": defaults.get("URL"),
            "Path": defaults.get("Path"),
            "Wait": defaults.get("Wait"),
            "Username": defaults.get("Username"),
            "Password": defaults.get("Password")
        }, indent=2))
    if defaults["Path"] == os.path.abspath(os.getcwd()):
        print("The updater can't update itself! Please select a different Path to download the files.")
        return
    
    Updater()

if __name__ == "__main__":
    main()