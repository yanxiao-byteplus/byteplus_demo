#  -*- coding: utf-8 -*-
import os
import sys
import json

sys.path.insert(0, "/Users/bytedance/byteplus/byteplus-sdk-python/")

from byteplus_sdk.cdn.service import CDNService

from cdn_rule_engine_sdk.rule_engine.Rule import Condition, Action, Rule
from cdn_rule_engine_sdk.rule_engine.Const import Const
from hsbc_demo_json import json_delivery_policy

class HSBCDemo:
    def __init__(self):
        self._svc = CDNService()
        ak = os.environ.get('HSBC_DEMO_ACCESSKEY', '')
        sk = os.environ.get('HSBC_DEMO_SECRETKEY', '')
        self._svc.set_ak(ak)
        self._svc.set_sk(sk)
        self._message = 'Byteplus SDK HSBC Demo'

     
    def list_cdn_domains(self) -> None:
        body = {}
        data = self._svc.list_cdn_domains(body)
        for seq, domain in enumerate(data["Result"]["Data"], start = 1):
            print(f"""
                  {seq} domain: {domain['Domain']}  cname: {domain['Cname']}  waf: {domain['Waf']} 
            """)
            
    def create_delivery_policy(self, title: str) -> str:
                
        json_policy_metadata = f"""
            "Title": "{title}",
            "Message": "{self._message}",
            "Project": "default",
        """
        
        json_full_str = "{" + json_policy_metadata + json_delivery_policy + "}"

        try:
            body = json.loads(json_full_str.strip().strip("\n"))
            resp = self._svc.create_service_template(body)
            template_id = resp['Result']['TemplateId']
            if template_id:
                print(f"""
                    delivery policy created as a success {title=} -> {template_id=}
                """)
                return template_id
        except KeyError:
            print(resp)
        except json.JSONDecodeError as e:
            print(f"json decoding exception {e=}")

    
    def describe_delivery_policy(self, template_id: str) -> None:
        
        if template_id:
            
            body = {
                "TemplateId": template_id
            }

            data = self._svc.describe_service_template(body)
            try:
                policy = data["Result"]
                template_id = policy['TemplateId']
                title = policy['Title']
                
                domains = []
                if policy['BoundDomains']:
                    domains = [x['Domain'] for x in policy['BoundDomains']]
                    
                print(f"""
                    {template_id=}  {title=} -> {domains=}
                """)
                
            except (KeyError):
                print(data)

    def create_cipher_policy(self, title: str) -> None:
        
        body = {
            "Title": title,
            "Message": self._message,
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
        
        try:
            data = self._svc.create_cipher_template(body)
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
            "TemplateId": template_id       
        }

        try:
            resp = self._svc.release_template(body)
            print(f"""
                    {template_id=}  {resp=}
            """)        
            
        except Exception as e:
            print(f"{e=}")
            
            

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
            
    
    def create_rule_engine(self, title: str) -> str:
        
        rule = Rule()
        rule.desc = self._message
        rule.if_block.condition = Condition({
            "IsGroup": True,
            "Connective": Const.ConnectiveAnd,
            "ConditionGroups": [
                {
                    "IsGroup": True,
                    "Connective": Const.ConnectiveAnd,
                    "ConditionGroups": [
                        {
                            "IsGroup": False,
                            "Connective": Const.ConnectiveAnd,
                            "Condition": {
                                "Object": Const.ConditionHTTPPath,
                                "Operator":Const.OperatorPrefixMatch,
                                "IgnoreCase":True,
                                "Value":["/stripheader/"]
                            }
                        }

                    ]
                }
            ]
        })
        rule.if_block.actions.append(Action({
            "Action": Const.ActionResponseHeader,
            "Groups":[
                {
                    "Dimension": Const.ActionResponseHeader,
                    "GroupParameters":[
                        {
                            "Parameters":[
                                {
                                    "Name":"action","Values":[Const.Delete]
                                },
                                {
                                    "Name":"header_name","Values":["server"]
                                }
                            ]
                        }
                    ]
                }
            ]
        }))

      
        try:
            data = self._svc.create_rule_engine_template({
                "Project": "default",
                "Title": title,
                "Message": self._message + ": delete response header server",
                "Rule": rule.encode_to_string()
            })
               
            policy = data["Result"]
            template_id = policy['TemplateId']
              
            print(f"""
                {template_id=} created for rule engine
            """)
            
            return template_id
        
        except (KeyError) as e:
            print(f"{e=}")
            print(data)
    

if __name__ == '__main__':
    
    byteplus_cdn_sdk = HSBCDemo()
    byteplus_cdn_sdk.list_cdn_domains()

    title_tpl_cipher = 'tpl_hsbc_sdk_cipher'
    id_tpl_cipher = byteplus_cdn_sdk.create_cipher_policy(title =  title_tpl_cipher)
    if id_tpl_cipher:
        byteplus_cdn_sdk.release_policy(template_id = id_tpl_cipher)
        # byteplus_cdn_sdk.update_cipher_template(template_id = id_tpl_cipher)
        byteplus_cdn_sdk.describe_cipher_policy(template_id = id_tpl_cipher)
        # byteplus_cdn_sdk.delete_policy(template_id = id_tpl_cipher)
    
    title_tpl_rule_engine = 'tpl_hsbc_sdk_rule_engine'
    id_tpl_rule_engine = byteplus_cdn_sdk.create_rule_engine(title = title_tpl_rule_engine)
    if id_tpl_rule_engine:
        byteplus_cdn_sdk.release_policy(template_id = id_tpl_rule_engine)
        byteplus_cdn_sdk.describe_rule_engine_policy(template_id = id_tpl_rule_engine)
        # byteplus_cdn_sdk.delete_policy(template_id = id_tpl_cipher)
    
    title_tpl_delivery_policy = 'tpl_hsbc_sdk_delivery_policy'    
    id_tpl_delivery_policy = byteplus_cdn_sdk.create_delivery_policy(title = title_tpl_delivery_policy)
    if id_tpl_delivery_policy:
        byteplus_cdn_sdk.release_policy(template_id = id_tpl_delivery_policy)
        byteplus_cdn_sdk.describe_delivery_policy(template_id = id_tpl_delivery_policy)
        # byteplus_cdn_sdk.delete_policy(template_id = id_tpl_cipher)







        
