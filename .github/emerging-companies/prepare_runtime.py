"""Install checksum-pinned public CPU inference tools into the runner's temp folder."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tarfile
import time
import urllib.error
import urllib.request

RUNTIME_URL = 'https://github.com/ggml-org/llama.cpp/releases/download/b12032/llama-b12032-bin-ubuntu-x64.tar.gz'
RUNTIME_SHA256 = '9f10432ca3f66ef003a7a540aaffb9da0acadaefd05404521b9ab7a2436af304'
MODEL_REPO = 'Qwen/Qwen3-4B-GGUF'
MODEL_REVISION = 'bc640142c66e1fdd12af0bd68f40445458f3869b'
MODEL_FILE = 'Qwen3-4B-Q4_K_M.gguf'
MODEL_SHA256 = '7485fe6f11af29433bc51cab58009521f205840f5b4ae3a32fa7f92e8534fdf5'
MODEL_URL = f'https://huggingface.co/{MODEL_REPO}/resolve/{MODEL_REVISION}/{MODEL_FILE}'

def digest(path):
    value=hashlib.sha256()
    with path.open('rb') as file:
        for chunk in iter(lambda:file.read(8*1024*1024),b''):value.update(chunk)
    return value.hexdigest()

def download(url,target,expected,max_bytes):
    if target.exists() and digest(target)==expected:return
    temporary=target.with_suffix(target.suffix+'.part')
    size=0
    req=urllib.request.Request(url,headers={'User-Agent':'engineering-notes-public-model/1.0'})
    try:
        with urllib.request.urlopen(req,timeout=90) as response,temporary.open('wb') as output:
            while chunk:=response.read(8*1024*1024):
                size+=len(chunk)
                if size>max_bytes:raise ValueError('Download exceeded pinned artifact size budget')
                output.write(chunk)
        if digest(temporary)!=expected:raise ValueError('Artifact checksum mismatch')
        temporary.replace(target)
    finally:
        if temporary.exists():temporary.unlink()

def install(cache):
    cache.mkdir(parents=True,exist_ok=True)
    archive=cache/'llama-b12032.tar.gz'
    download(RUNTIME_URL,archive,RUNTIME_SHA256,30*1024*1024)
    runtime=cache/'llama-b12032'
    runtime.mkdir(exist_ok=True)
    with tarfile.open(archive,'r:gz') as tar:
        tar.extractall(runtime,filter='data')
    matches=list(runtime.rglob('llama-server'))
    if len(matches)!=1:raise RuntimeError('Pinned runtime has an unexpected server layout')
    model=cache/MODEL_FILE
    download(MODEL_URL,model,MODEL_SHA256,2_600_000_000)
    provenance={'runtime_url':RUNTIME_URL,'runtime_sha256':RUNTIME_SHA256,'model_repo':MODEL_REPO,'model_revision':MODEL_REVISION,'model_file':MODEL_FILE,'model_sha256':MODEL_SHA256,'mode':'CPU, no paid inference API'}
    (cache/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n',encoding='utf-8')
    return matches[0],model

def start(cache,binary,model):
    if os.name=='nt':raise RuntimeError('This pinned runtime targets the GitHub Ubuntu runner')
    log=(cache/'server.log').open('ab')
    env=dict(os.environ)
    env['LD_LIBRARY_PATH']=str(binary.parent)+os.pathsep+env.get('LD_LIBRARY_PATH','')
    command=[str(binary),'--model',str(model),'--host','127.0.0.1','--port','8080','--threads','4','--ctx-size','16384','--parallel','1','--n-gpu-layers','0','--chat-template-kwargs','{"enable_thinking":false}']
    process=subprocess.Popen(command,stdout=log,stderr=subprocess.STDOUT,env=env,start_new_session=True)
    log.close()
    (cache/'server.pid').write_text(str(process.pid),encoding='ascii')
    deadline=time.monotonic()+240
    while time.monotonic()<deadline:
        if process.poll() is not None:raise RuntimeError('CPU inference server stopped; inspect the runtime artifact log')
        try:
            with urllib.request.urlopen('http://127.0.0.1:8080/health',timeout=3) as response:
                if response.status==200:return
        except (urllib.error.URLError,TimeoutError):pass
        time.sleep(2)
    process.terminate()
    raise RuntimeError('CPU inference server did not become ready')

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--cache-dir',type=Path,required=True)
    parser.add_argument('--serve',action='store_true')
    args=parser.parse_args()
    binary,model=install(args.cache_dir.resolve())
    if args.serve:start(args.cache_dir.resolve(),binary,model)
    print(json.dumps({'runtime':'llama.cpp b12032','model':MODEL_REPO,'ready':args.serve,'cache':str(args.cache_dir)},ensure_ascii=False))

if __name__=='__main__':main()
