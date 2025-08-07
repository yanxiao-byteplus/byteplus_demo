# -*- coding: utf-8 -*-
import os
import sys
import json
import logging
from datetime import datetime
from requests.exceptions import RequestException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("hsbc_cdn_demo.log"),  # Log to file
        logging.StreamHandler()                    # Log to console
    ]
)
logger = logging.getLogger(__name__)

sys.path.insert(0, "/Users/bytedance/byteplus/byteplus-sdk-python/")

from byteplus_sdk.cdn.service import CDNService
from cdn_rule_engine_sdk.rule_engine.Rule import Condition, Action, Rule
from cdn_rule_engine_sdk.rule_engine.Const import Const
from hsbc_demo_json import json_delivery_policy  # Import base delivery policy template


class HSBCDemo:
    def __init__(self):
        """Initialize Byteplus CDN service with authentication
        
        Input:
            - Environment variables: HSBC_DEMO_ACCESSKEY, HSBC_DEMO_SECRETKEY
        
        Output:
            - Initialized CDN service instance with credentials
            - Raises ValueError if credentials are missing
        """
        self._svc = CDNService()
        
        # Get credentials from environment variables
        self._ak = os.environ.get('HSBC_DEMO_ACCESSKEY', '')
        self._sk = os.environ.get('HSBC_DEMO_SECRETKEY', '')
        
        # Validate credentials
        if not self._ak or not self._sk:
            error_msg = "Environment variables HSBC_DEMO_ACCESSKEY and HSBC_DEMO_SECRETKEY must be set"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Configure service with credentials
        self._svc.set_ak(self._ak)
        self._svc.set_sk(self._sk)
        self._message = 'Byteplus SDK HSBC Demo'
        self._cert_id = "cert-9fe8c4d8bf2746469eb0050c4812698b"

        logger.info("Byteplus CDN service initialized successfully")

    def _call_sdk_method(self, method, body, success_msg) -> dict:
        """Generic wrapper for SDK method calls with error handling
        
        Input:
            - method: SDK method to call (e.g., self._svc.create_service_template)
            - body: Dictionary containing request parameters
            - success_msg: Message to log on successful call
        
        Output:
            - Dictionary containing API response if successful
            - None if call fails
        """
        try:
            logger.debug(f"Calling SDK method with parameters: {json.dumps(body, indent=2)}")
            resp = method(body)
            logger.info(success_msg)
            logger.debug(f"API response: {json.dumps(resp, indent=2)}")
            return resp
        except RequestException as e:
            logger.error(f"API request failed: {str(e)}")
        except KeyError as e:
            logger.error(f"Response format error - missing field: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
        return None

    def create_domain(self, domain: str, id_rule: str, id_delivery: str, id_cipher) -> None:
    
        resp = self._call_sdk_method(
            self._svc.add_template_domain,
            {
                "Domain": domain,
                "RuleTemplateIds": [id_rule],
                "ServiceTemplateId": id_delivery,
                "CipherTemplateId": id_cipher,
                "HTTPSSwitch": "on",
                "CertId": self._cert_id,
                "ServiceRegion": "outside_chinese_mainland"
            },
            f" Creating CDN domains {domain}"
        )
          # Print and log domain details if response is valid
        if resp and "Result" in resp and "ResourceIds" in resp["Result"]:
            for seq, domain in enumerate(resp["Result"]["ResourceIds"], start=1):
                domain_info = f"[{seq}]. Domain: [{domain.get('Domain')}] is created"
                logger.info(domain_info)
        else:
            logger.warning(f"Failed in creating new {domain=} {resp=}")
        

    def list_cdn_domains(self) -> None:
        """Retrieve and display list of CDN domains
        
        Input:
            - None
        
        Output:
            - Prints domain details to console
            - Logs results to log file
        """
        resp = self._call_sdk_method(
            self._svc.list_cdn_domains,
            {},
            "Successfully retrieved CDN domains"
        )
        
        # Print and log domain details if response is valid
        if resp and "Result" in resp and "Data" in resp["Result"]:
            for seq, domain in enumerate(resp["Result"]["Data"], start=1):
                domain_info = (f"{seq}. Domain: {domain.get('Domain')}, "
                              f"CNAME: {domain.get('Cname')}, "
                              f"WAF Status: {domain.get('Waf')}")
                logger.info(domain_info)
        else:
            logger.warning("No CDN domains found or invalid response format")

    def create_delivery_policy(self, title: str) -> str:
        """Create a new delivery policy by merging metadata with base template
        
        Input:
            - title: String containing policy title
        
        Output:
            - String containing template ID if successful
            - None if creation fails
        """
        try:
            # Parse base policy template from JSON string
            base_policy = json.loads(json_delivery_policy)
            logger.debug(f"Successfully parsed base delivery policy: {json_delivery_policy[:100]}...")
            
            # Merge metadata with base policy (avoids JSON syntax errors)
            full_policy = {
                "Title": title,
                "Message": self._message,
                "Project": "default",
                **base_policy  # Merge base policy fields
            }
            logger.debug(f"Full delivery policy: {json.dumps(full_policy, indent=2)[:5000]}...")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse base policy JSON: {str(e)}")
            return None

        # Call SDK to create policy
        resp = self._call_sdk_method(
            self._svc.create_service_template,
            full_policy,
            f"Delivery policy creation initiated: {title}"
        )

        # Extract and return template ID if successful
        if resp and "Result" in resp and "TemplateId" in resp["Result"]:
            template_id = resp["Result"]["TemplateId"]
            logger.info(f"Delivery policy created successfully: {title} -> {template_id}")
            return template_id
        
        logger.error(f"Failed to create delivery policy: {title}")
        return None

    def describe_delivery_policy(self, template_id: str) -> None:
        """Retrieve and display details of a specific delivery policy
        
        Input:
            - template_id: String containing policy template ID
        
        Output:
            - Prints policy details to console
            - Logs results to log file
        """
        if not template_id:
            logger.warning("Template ID cannot be empty for describe_delivery_policy")
            return

        resp = self._call_sdk_method(
            self._svc.describe_service_template,
            {"TemplateId": template_id},
            f"Successfully retrieved details for policy: {template_id}"
        )

        # Extract and display policy details
        if resp and "Result" in resp:
            policy = resp["Result"]
            domains = []
            policy_info = (f"Delivery Policy - ID: {policy.get('TemplateId')}, "
                          f"Title: {policy.get('Title')}, "
                          f"Bound Domains: {domains}")
            logger.info(policy_info)
            logger.debug(f"Full policy details: {json.dumps(policy, indent=2)}")
        else:
            logger.warning(f"No details found for delivery policy: {template_id}")

    def create_cipher_policy(self, title: str) -> str:
        """Create a new cipher policy (HTTPS configuration)
        
        Input:
            - title: String containing policy title
        
        Output:
            - String containing template ID if successful
            - None if creation fails
        """
        # Define cipher policy configuration
        body = {
            "Title": title,
            "Message": self._message,
            "Project": "default",
            "Quic": {"Switch": False},
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
        logger.debug(f"Cipher policy configuration: {json.dumps(body, indent=2)}")

        # Call SDK to create policy
        resp = self._call_sdk_method(
            self._svc.create_cipher_template,
            body,
            f"Cipher policy creation initiated: {title}"
        )

        # Extract and return template ID if successful
        if resp and "Result" in resp and "TemplateId" in resp["Result"]:
            template_id = resp["Result"]["TemplateId"]
            logger.info(f"Cipher policy created successfully: {template_id}")
            return template_id
        
        logger.error(f"Failed to create cipher policy: {title}")
        return None

    def describe_cipher_policy(self, template_id: str) -> None:
        """Retrieve and display details of a specific cipher policy
        
        Input:
            - template_id: String containing policy template ID
        
        Output:
            - Prints policy details to console
            - Logs results to log file
        """
        if not template_id:
            logger.warning("Template ID cannot be empty for describe_cipher_policy")
            return

        resp = self._call_sdk_method(
            self._svc.describe_cipher_template,
            {"TemplateId": template_id},
            f"Successfully retrieved details for cipher policy: {template_id}"
        )

        if resp:
            logger.debug(f"Cipher policy {template_id} details: {json.dumps(resp, indent=2)}")
        else:
            logger.warning(f"No details found for cipher policy: {template_id}")

    def describe_rule_engine_policy(self, template_id: str) -> None:
        """Retrieve and display details of a specific rule engine policy
        
        Input:
            - template_id: String containing policy template ID
        
        Output:
            - Prints policy details to console
            - Logs results to log file
        """
        if not template_id:
            logger.warning("Template ID cannot be empty for describe_rule_engine_policy")
            return

        resp = self._call_sdk_method(
            self._svc.describe_rule_engine_template,
            {"TemplateId": template_id},
            f"Successfully retrieved details for rule engine policy: {template_id}"
        )

        if resp:
            logger.debug(f"Rule engine policy {template_id} details: {json.dumps(resp, indent=2)}")
        else:
            logger.warning(f"No details found for rule engine policy: {template_id}")

    def update_cipher_template(self, template_id: str) -> None:
        """Update an existing cipher policy
        
        Input:
            - template_id: String containing policy template ID
        
        Output:
            - Prints update response to console
            - Logs results to log file
        """
        if not template_id:
            logger.warning("Template ID cannot be empty for update_cipher_template")
            return

        resp = self._call_sdk_method(
            self._svc.update_cipher_template,
            {"TemplateId": template_id, "Title": "revised-tpl_hsbc_sdk_cipher"},
            f"Cipher policy update initiated: {template_id}"
        )

        if resp:
            logger.info(f"Cipher policy {template_id} updated successfully")
        else:
            logger.error(f"Failed to update cipher policy: {template_id}")

    def release_policy(self, template_id: str) -> None:
        """Release a policy (make it active)
        
        Input:
            - template_id: String containing policy template ID
        
        Output:
            - Logs release status
        """
        if not template_id:
            logger.warning("Template ID cannot be empty for release_policy")
            return

        self._call_sdk_method(
            self._svc.release_template,
            {"TemplateId": template_id},
            f"Policy released successfully: {template_id}"
        )

    def delete_policy(self, template_id: str) -> None:
        """Delete a policy
        
        Input:
            - template_id: String containing policy template ID
        
        Output:
            - Logs deletion status
        """
        if not template_id:
            logger.warning("Template ID cannot be empty for delete_policy")
            return

        self._call_sdk_method(
            self._svc.delete_template,
            {"TemplateId": template_id},
            f"Policy deleted successfully: {template_id}"
        )

    def create_rule_engine(self, title: str) -> str:
        """Create a rule engine policy (header modification rules)
        
        Input:
            - title: String containing policy title
        
        Output:
            - String containing template ID if successful
            - None if creation fails
        """
        # Initialize rule object
        rule = Rule()
        rule.desc = self._message
        logger.debug("Initialized rule engine object")
        
        # Define condition: match paths starting with /stripheader/
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
                                "Operator": Const.OperatorPrefixMatch,
                                "IgnoreCase": True,
                                "Value": ["/stripheader/"]
                            }
                        }
                    ]
                }
            ]
        })
        logger.debug("Rule engine condition defined")
        
        # Define action: delete "server" response header
        rule.if_block.actions.append(Action({
            "Action": Const.ActionResponseHeader,
            "Groups": [
                {
                    "Dimension": Const.ActionResponseHeader,
                    "GroupParameters": [
                        {
                            "Parameters": [
                                {"Name": "action", "Values": [Const.Delete]},
                                {"Name": "header_name", "Values": ["server"]}
                            ]
                        }
                    ]
                }
            ]
        }))
        logger.debug("Rule engine action defined")

        # Call SDK to create rule engine policy
        resp = self._call_sdk_method(
            self._svc.create_rule_engine_template,
            {
                "Project": "default",
                "Title": title,
                "Message": f"{self._message}: delete response header server",
                "Rule": rule.encode_to_string()
            },
            f"Rule engine policy creation initiated: {title}"
        )

        # Extract and return template ID if successful
        if resp and "Result" in resp and "TemplateId" in resp["Result"]:
            template_id = resp["Result"]["TemplateId"]
            logger.info(f"Rule engine policy created successfully: {template_id}")
            return template_id
        
        logger.error(f"Failed to create rule engine policy: {title}")
        return None


if __name__ == '__main__':
    try:
        logger.info("Starting HSBC CDN Demo..")
        # Initialize CDN demo client
        byteplus_cdn_sdk = HSBCDemo()
        
        # List all CDN domains
        logger.info(f"..............................................................")  
        byteplus_cdn_sdk.list_cdn_domains()

        # Create and manage cipher policy
        title_tpl_cipher = 'tpl_hsbc_sdk_cipher'
        logger.info(f"..............................................................")   
        logger.info(f"Starting creation of cipher policy: {title_tpl_cipher}")
        id_tpl_cipher = byteplus_cdn_sdk.create_cipher_policy(title=title_tpl_cipher)
        if id_tpl_cipher:
            byteplus_cdn_sdk.release_policy(template_id=id_tpl_cipher)
            # byteplus_cdn_sdk.update_cipher_template(template_id=id_tpl_cipher)  # Uncomment to test update
            byteplus_cdn_sdk.describe_cipher_policy(template_id=id_tpl_cipher)
            # byteplus_cdn_sdk.delete_policy(template_id=id_tpl_cipher)  # Uncomment to test deletion

        # Create and manage rule engine policy
        title_tpl_rule_engine = 'tpl_hsbc_sdk_rule_engine'
        logger.info(f"..............................................................")   
        logger.info(f"Starting creation of rule engine policy: {title_tpl_rule_engine}")
        id_tpl_rule_engine = byteplus_cdn_sdk.create_rule_engine(title=title_tpl_rule_engine)
        if id_tpl_rule_engine:
            byteplus_cdn_sdk.release_policy(template_id=id_tpl_rule_engine)
            byteplus_cdn_sdk.describe_rule_engine_policy(template_id=id_tpl_rule_engine)
            # byteplus_cdn_sdk.delete_policy(template_id=id_tpl_rule_engine)  # Uncomment to test deletion

        # Create and manage delivery policy
        title_tpl_delivery_policy = 'tpl_hsbc_sdk_delivery_policy'   
        logger.info(f"..............................................................")   
        logger.info(f"Starting creation of delivery policy: {title_tpl_delivery_policy}")
        id_tpl_delivery_policy = byteplus_cdn_sdk.create_delivery_policy(title=title_tpl_delivery_policy)
        if id_tpl_delivery_policy:
            byteplus_cdn_sdk.release_policy(template_id=id_tpl_delivery_policy)
            byteplus_cdn_sdk.describe_delivery_policy(template_id=id_tpl_delivery_policy)
            # byteplus_cdn_sdk.delete_policy(template_id=id_tpl_delivery_policy)  # Uncomment to test deletion

        domain = "hsbc-demo-sdk.security.lcyice.top"
        logger.info(f"..............................................................")  
        logger.info(f"Starting creation new domain: {domain}")
        byteplus_cdn_sdk.create_domain(
            domain=domain,
            id_rule=id_tpl_rule_engine,
            id_delivery=id_tpl_delivery_policy,
            id_cipher=id_tpl_cipher
        )   
        
        logger.info(f"..............................................................")

        
    except Exception as e:
        logger.error(f"Script failed: {str(e)}", exc_info=True)
        sys.exit(1)
