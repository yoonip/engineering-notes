"""Exercise actual local inference, distinct from mocked parser tests."""
import json,time,urllib.request
request_body={'model':'local','messages':[{'role':'system','content':'Return the requested JSON object only. /no_think'},{'role':'user','content':'Return {"ok":true,"message":"공개 모델 실행을 확인합니다."}'}],'temperature':0,'max_tokens':128,'chat_template_kwargs':{'enable_thinking':False},'response_format':{'type':'json_schema','json_schema':{'name':'runtime_smoke','schema':{'type':'object','properties':{'ok':{'type':'boolean'},'message':{'type':'string'}},'required':['ok','message'],'additionalProperties':False}}}}
start=time.monotonic()
req=urllib.request.Request('http://127.0.0.1:8080/v1/chat/completions',data=json.dumps(request_body).encode(),headers={'Content-Type':'application/json'})
with urllib.request.urlopen(req,timeout=240) as response:result=json.load(response)
value=json.loads(result['choices'][0]['message']['content'])
assert value['ok'] is True and value['message']
print(json.dumps({'test':'actual CPU structured inference','result':value,'seconds':round(time.monotonic()-start,2),'usage':result.get('usage')},ensure_ascii=False))
