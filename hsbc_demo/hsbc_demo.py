import os
import sys
import json
import time
from typing import Optional

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from byteplus_sdk.cdn.service import CDNService

class HSBCDemo:
    def __init__(self):
        self._svc = CDNService()
        ak = os.environ.get('BYTEPLUS_ACCESSKEY', '')
        sk = os.environ.get('BYTEPLUS_SECRETKEY', '')
        self._svc.set_ak(ak)
        self._svc.set_sk(sk)


    def create_delivery_policy(self, policy_name: str) -> Optional[str]:
                
        body = {
            "Title": policy_name,
            "Message": "SDK Demo",
            "Project": "default",
            "OriginProtocol": "http",
            "Origin": [
                {
                    "OriginAction": {
                        "OriginLines": [
                            {
                                "OriginType": "primary",
                                "InstanceType": "domain",
                                "Address": "img.migrate.lcyice.top",
                                "Weight": "1",
                                "HttpPort": "80",
                                "HttpsPort": "443",
                                "OriginHost": "img.migrate.lcyice.top",
       
                            }
                        ]
                    }
                }
            ]
        }

        resp = self._svc.create_service_template(body)
        
        try:
            template_id = resp['Result']['TemplateId']
            if template_id:
                print(resp)
                return template_id
            
        except KeyError:
            print(resp)

    
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

    def delete_delivery_policy(self, template_id: str) -> None:

        if template_id:
            body = {
                "TemplateId": template_id
            }

            data = self._svc.delete_template(body)
            try:
                request_id = data["ResponseMetadata"]["RequestId"]
                if request_id:
                    print(data)

            except KeyError:
                print(data)
        

    def publish_delivery_policy(self, template_id: str) -> None:

        if template_id:

            data = self._svc.lock_template({
                "TemplateId": template_id,
            })
                
            print(data)
    
    def create_domain_from_delivery_policy(self, template_id: str, domain: str) -> None:
        
        if template_id and domain:
            body = {
                "ServiceRegion": "outside_chinese_mainland",
                "Project": "default",
                "ServiceTemplateId": template_id,
                "CertId": "cert-101be04b745e4233ba7cc0e013bff6d9",
                # "CipherTemplateId": "tpl-example",
                "Domain": domain,
                "HTTPSSwitch": "on"
            }

            resp = self._svc.add_template_domain(body)
            print(resp)
    
    def delete_cdn_domain(self, domain: str) -> None:
        
        if domain:
            body = {
                "Domain": domain,
            }

            resp = self._svc.stop_cdn_domain(body)
            print(resp)
            
            time.sleep(5)
            
            resp = self._svc.delete_cdn_domain(body)
            print(resp)
            
            time.sleep(5)

    
    def list_cdn_domains(self, domain: str) -> None:
        
        if domain:
            body = {
                "Domain": domain,
            }
            
            data = self._svc.list_cdn_domains(body)
            formatted_data = json.dumps(data, indent=4, sort_keys=True)
            print(formatted_data)


if __name__ == '__main__':
    
    demo_domain = "hsbc-demo101.migrate.lcyice.top"
    demo = HSBCDemo()
    
    template_id = demo.create_delivery_policy(policy_name = "hsbc-sdk-api-demo")
    if template_id:
        demo.publish_delivery_policy(template_id = template_id)
        # demo.describe_delivery_policy(template_id = template_id)
        demo.create_domain_from_delivery_policy(template_id = template_id, domain = demo_domain)
        demo.list_cdn_domains(domain = demo_domain)
        demo.delete_cdn_domain(domain = demo_domain)
        demo.delete_delivery_policy(template_id = template_id)




        
