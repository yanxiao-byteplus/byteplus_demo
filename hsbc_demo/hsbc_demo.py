#  -*- coding: utf-8 -*-
import os,sys

sys.path.insert(0, "/Users/bytedance/byteplus/byteplus-sdk-python/")
from byteplus_sdk.cdn.service import CDNService

from rule_engine.Rule import Condition, Action, Rule
from rule_engine.Const import Const

class HSBCDemo:
    def __init__(self):
        self._svc = CDNService()
        ak = os.environ.get('HSBC_DEMO_ACCESSKEY', '')
        sk = os.environ.get('HSBC_DEMO_SECRETKEY', '')
        self._svc.set_ak(ak)
        self._svc.set_sk(sk)


    # def create_delivery_policy(self, policy_name: str) -> str:
                
    #     body = {
    #         "Title": policy_name,
    #         "Message": "SDK Demo",
    #         "Project": "default",
    #         "OriginProtocol": "http",
    #         "Origin": [
    #             {
    #                 "OriginAction": {
    #                     "OriginLines": [
    #                         {
    #                             "OriginType": "primary",
    #                             "InstanceType": "domain",
    #                             "Address": "img.migrate.lcyice.top",
    #                             "Weight": "1",
    #                             "HttpPort": "80",
    #                             "HttpsPort": "443",
    #                             "OriginHost": "img.migrate.lcyice.top",
       
    #                         }
    #                     ]
    #                 }
    #             }
    #         ]
    #     }

    #     resp = self._svc.create_service_template(body)
        
    #     try:
    #         template_id = resp['Result']['TemplateId']
    #         if template_id:
    #             print(f"""
    #                 delivery policy created as a success {policy_name=} -> {template_id=}
    #             """)
    #             return template_id
    #     except KeyError:
    #         print(resp)
        
    
    def list_cdn_domains(self) -> None:
        body = {}
        data = self._svc.list_cdn_domains(body)
        for seq, domain in enumerate(data["Result"]["Data"], start = 1):
            print(f"""
                  {seq} domain: {domain['Domain']}  cname: {domain['Cname']}  waf: {domain['Waf']} 
            """)
    
    # def describe_delivery_policy(self, template_id: str) -> None:
        
    #     if template_id:
            
    #         body = {
    #             "TemplateId": template_id
    #         }

    #         data = self._svc.describe_service_template(body)
    #         try:
    #             policy = data["Result"]
    #             template_id = policy['TemplateId']
    #             title = policy['Title']
                
    #             domains = []
    #             if policy['BoundDomains']:
    #                 domains = [x['Domain'] for x in policy['BoundDomains']]
                    
    #             print(f"""
    #                 {template_id=}  {title=} -> {domains=}
    #             """)
    #         except (KeyError):
    #             print(data)

    def create_cipher_policy(self, title: str) -> None:
        
        body = {
            "Title": title,
            "Message": "hsbc demo",
            "Project": "default",
            "Quic": {
                "Switch": False
            },
            "HTTPS": {
                "CertCheck": None,
                "DisableHttp": False,
                "ForcedRedirect": {
                "EnableForcedRedirect": True,
                "StatusCode": "301"
                },
                "HTTP2": True,
                "Hsts": {
                "Subdomain": None,
                "Switch": False,
                "Ttl": 0
                },
                "OCSP": False,
                "TlsVersion": ["tlsv1.3"]
            },
            "HttpForcedRedirect": {
                "EnableForcedRedirect": False,
                "StatusCode": "301"
            },
        }
        
        data = self._svc.create_cipher_template(body)
        try:
            policy = data["Result"]
            template_id = policy['TemplateId']
              
            print(f"""
                {template_id=} created for cipher template
            """)
            
            return template_id
        
        except (KeyError) as e:
            print(f"{e=}")
            print(data)


    def describe_cipher_policy(self, template_id: str) -> None:
        
        body = {
            "TemplateId": template_id
        }

        try:
            resp = self._svc.describe_cipher_template(body)
            print(f"""
                    {template_id=}  {resp=}
            """)        
            
        except Exception as e:
            print(f"{e=}")
    
    def describe_rule_engine_policy(self, template_id: str) -> None:
        
        body = {
            "TemplateId": template_id
        }

        try:
            resp = self._svc.describe_rule_engine_template(body)
            print(f"""
                    {template_id=}  {resp=}
            """)        
            
        except Exception as e:
            print(f"{e=}")
            
    def update_cipher_template(self, template_id: str) -> None:
        
        body = {
            "TemplateId": template_id,
            "Title": "revised-tpl_hsbc_sdk_cipher"
        }
        
        try:
            resp = self._svc.update_cipher_template(body)
            print(f"""
                    {template_id=}  {resp=}
            """)        
        except Exception as e:
            print(f"{e=}")
    
    
    def release_policy(self, template_id: str) -> None:
        
        body = {
            "TemplateId": template_id        }

        try:
            resp = self._svc.release_template(body)
            print(f"""
                    {template_id=}  {resp=}
            """)        
            
        except Exception as e:
            print(f"{e=}")
            
            
        body = {
        "TemplateId": "tpl-example"
    }


    def delete_policy(self, template_id: str) -> None:
        
        body = {
            "TemplateId": template_id
        }

        try:
            resp = self._svc.delete_template(body)
            print(f"""
                    {template_id=}  {resp=}
            """)        
            
        except Exception as e:
            print(f"{e=}")
            
    
# tpl-ce9g3ro

if __name__ == '__main__':
    
    demo = HSBCDemo()
    # demo.list_cdn_domains()
    # template_id = demo.create_delivery_policy(policy_name = "hsbc-sdk-api-demo")
    # if template_id:
    #     demo.describe_delivery_policy(template_id =  template_id)
    
    # template_ciphers = 'tpl-ceqmklq'
    # if template_ciphers:
    #     demo.describe_cipher_policy(template_id =  template_ciphers)、

    title_tpl_cipher = 'tpl_hsbc_sdk_cipher'
    # id_tpl_cipher = demo.create_cipher_policy(title =  title_tpl_cipher)
    
    # if id_tpl_cipher:
    #     demo.release_policy(template_id = id_tpl_cipher)
    #     demo.update_cipher_template(template_id = id_tpl_cipher)
    #     demo.describe_cipher_policy(template_id = id_tpl_cipher)
    #     demo.delete_policy(template_id = id_tpl_cipher)





        
