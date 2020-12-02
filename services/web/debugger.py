from os import getenv, environ

def initialize_flask_server_debugger_if_needed():
    if (getenv("DEBUGGER") == "True") and (getenv("ALREADY_DEBUGGING") == "False"):
        import multiprocessing
        try:
            if multiprocessing.current_process().pid > 1:
                print("import debugpy")
                import debugpy
                debugpy.listen(("0.0.0.0", 10001))
                print("VS Code debugger can now be attached, press F5 in VS Code..", flush=True)
                environ["ALREADY_DEBUGGING"] = "True"
                debugpy.wait_for_client()
                print("VS Code debugger attached, enjoy debugging", flush=True)
            else:
                print("Debugger: This has process.id == 1.")
        except Exception as e:
            print("Couldn't start debugger because of:")
            print(e)
            print("ALREADY_DEBUGGING: " + str(getenv("ALREADY_DEBUGGING")))
    else:
        print(getenv("DEBUGGER"))
        print(getenv("ALREADY_DEBUGGING"))
        print("No debugging. Alrighty..")