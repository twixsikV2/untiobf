import marshal, base64, zlib, sys, os, ctypes, time, random

XOR_KEY = 0xAA
LAYERS = 3  # количество слоёв упаковки

def xor_bytes(data: bytes, key: int) -> bytes:
    return bytes(b ^ key for b in data)

def anti_analysis():
    try:
        if hasattr(ctypes, "windll") and ctypes.windll.kernel32.IsDebuggerPresent():
            os._exit(1)
        start = time.perf_counter()
        time.sleep(0.002)
        if time.perf_counter() - start > 0.05:
            os._exit(1)
        if "PYCHARM_HOSTED" in os.environ or "pythonDebug" in sys.argv[0]:
            os._exit(1)
    except Exception:
        pass

def layer_encrypt(code: bytes, key: int) -> str:
    payload = base64.b64encode(xor_bytes(zlib.compress(code, 9), key)).decode()
    return f'''import marshal,base64,zlib,os,ctypes,time,sys
k={key}
def a():
 try:
  if hasattr(ctypes,"windll")and ctypes.windll.kernel32.IsDebuggerPresent():os._exit(1)
  t=time.perf_counter();time.sleep(0.001)
  if time.perf_counter()-t>0.05:os._exit(1)
 except:...
a()
exec(marshal.loads(zlib.decompress(bytes(b^k for b in base64.b64decode("{payload}")))))'''

def obfuscate_file(input_path: str, output_path: str):
    anti_analysis()
    with open(input_path, 'r', encoding='utf-8') as f:
        code = compile(f.read(), input_path, 'exec')
    blob = marshal.dumps(code)

    for _ in range(LAYERS):
        blob = marshal.dumps(compile(layer_encrypt(blob, XOR_KEY), "<layer>", "exec"))

    final_payload = base64.b64encode(xor_bytes(zlib.compress(blob, 9), XOR_KEY)).decode()

    final_loader = f'''import marshal,base64,zlib,os,ctypes,time,sys
k={XOR_KEY}
def a():
 try:
  if hasattr(ctypes,"windll")and ctypes.windll.kernel32.IsDebuggerPresent():os._exit(1)
  s=time.perf_counter();time.sleep(0.001)
  if time.perf_counter()-s>0.05:os._exit(1)
 except:...
a()
exec(marshal.loads(zlib.decompress(bytes(b^k for b in base64.b64decode("{final_payload}")))))
'''

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_loader)

    print(f"Успешно: {input_path} → {output_path}")
    print(f"{LAYERS} уровней упаковки, длина payload: {len(final_payload)}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python ultra_obf.py input.py output.py")
        sys.exit(1)
    obfuscate_file(sys.argv[1], sys.argv[2])
