# -*- coding: utf-8 -*-
"""
HSBC Demo Delivery Policy JSON Template

This file defines the JSON configuration for delivery policy in a clear,
efficient and professional format. The configuration is stored as a Python
multi-line string for direct consumption or further serialization.
"""

json_delivery_policy = """
{
  "AreaAccessRule": {
    "Area": ["HKG", "MYS", "THA", "IDN", "USA", "RUS", "SGP"],
    "RuleType": "allow",
    "Switch": true
  },
  "BrowserCache": [],
  "Cache": [
    {
      "CacheAction": {
        "Action": "cache",
        "DefaultPolicy": "force_cache",
        "IgnoreCase": false,
        "Ttl": 1209600
      },
      "Condition": {
        "ConditionRule": [
          {
            "Object": "filetype",
            "Operator": "match",
            "Type": "url",
            "Value": "html;htm;7z;avi;avif;apk;bin;bmp;bz2;class;css;csv;doc;docx;dmg;ejs;eot;eps;exe;flac;gif;gz;ico;iso;jar;jpg;jpeg;js;mid;midi;mkv;mp3;mp4;ogg;otf;pdf;pict;pls;png;ppt;pptx;ps;rar;sh;shtml;svg;swf;tar;tga;tif;tiff;ttf;txt;wav;webp;woff;woff2;xls;xlsx;xml;zip"
          }
        ],
        "Connective": "OR"
      }
    },
    {
      "CacheAction": {
        "Action": "cache",
        "DefaultPolicy": "origin_first_Replenish",
        "IgnoreCase": false,
        "Ttl": 0
      },
      "Condition": {
        "ConditionRule": [
          {
            "Object": "path",
            "Operator": "match",
            "Type": "url",
            "Value": "/"
          }
        ],
        "Connective": "OR"
      }
    }
  ],
  "CacheKey": [
    {
      "CacheKeyAction": {
        "CacheKeyComponents": [
          {
            "Action": "include",
            "IgnoreCase": true,
            "Object": "queryString",
            "Subobject": "*"
          }
        ]
      },
      "Condition": {
        "ConditionRule": [
          {
            "Object": "directory",
            "Operator": "match",
            "Type": "url",
            "Value": "/"
          }
        ],
        "Connective": "OR"
      }
    }
  ],
  "Compression": {
    "CompressionRules": [
      {
        "CompressionAction": {
          "CompressionFormat": "all",
          "CompressionTarget": "*",
          "CompressionType": ["gzip", "br"],
          "MaxFileSizeKB": null,
          "MinFileSizeKB": 1
        },
        "Condition": {
          "ConditionRule": [
            {
              "Object": "directory",
              "Operator": "match",
              "Type": "url",
              "Value": "/hugefile/"
            }
          ],
          "Connective": "OR"
        }
      }
    ],
    "Switch": true
  },
  "ConditionalOrigin": {
    "OriginRules": [],
    "Switch": false
  },
  "CreateTime": 1753410831,
  "CustomErrorPage": {
    "ErrorPageRule": [
      {
        "ErrorPageAction": {
          "Action": "redirect",
          "RedirectCode": "302",
          "RedirectUrl": "https://hsbc-demo-101.migrate.lcyice.top/error_page.php?error_code=401&error_message=Oops...%20Something%20goes%20wrong...",
          "StatusCode": "401"
        }
      },
      {
        "ErrorPageAction": {
          "Action": "redirect",
          "RedirectCode": "302",
          "RedirectUrl": "https://hsbc-demo-101.migrate.lcyice.top/error_page.php?error_code=402&error_message=Oops...%20Something%20goes%20wrong...",
          "StatusCode": "402"
        }
      },
      {
        "ErrorPageAction": {
          "Action": "redirect",
          "RedirectCode": "302",
          "RedirectUrl": "https://hsbc-demo-101.migrate.lcyice.top/error_page.php?error_code=403&error_message=Oops...%20Something%20goes%20wrong...",
          "StatusCode": "403"
        }
      },
      {
        "ErrorPageAction": {
          "Action": "redirect",
          "RedirectCode": "302",
          "RedirectUrl": "https://hsbc-demo-101.migrate.lcyice.top/error_page.php?error_code=404&error_message=Oops...%20Something%20goes%20wrong...",
          "StatusCode": "404"
        }
      },
      {
        "ErrorPageAction": {
          "Action": "redirect",
          "RedirectCode": "302",
          "RedirectUrl": "https://hsbc-demo-101.migrate.lcyice.top/error_page.php?error_code=500&error_message=Oops...%20Something%20goes%20wrong...",
          "StatusCode": "5xx"
        }
      }
    ],
    "Switch": true
  },
  "Exception": false,
  "FollowRedirect": false,
  "IPv6": {
    "Switch": true
  },
  "MethodDeniedRule": {
    "Methods": "POST,DELETE,PUT,PATCH,CONNECT,OPTIONS",
    "Switch": true
  },
  "NegativeCache": null,
  "Origin": [
    {
      "Condition": null,
      "OriginAction": {
        "OriginLines": [
          {
            "Address": "34.124.182.199",
            "BucketName": null,
            "HttpPort": "80",
            "HttpsPort": "443",
            "InstanceType": "ip",
            "OriginHost": "",
            "OriginType": "primary",
            "PrivateBucketAccess": false,
            "PrivateBucketAuth": null,
            "Region": "",
            "Weight": "1"
          }
        ]
      }
    }
  ],
  "OriginAccessRule": {
    "AllowEmpty": true
  },
  "OriginArg": [
    {
      "Condition": {
        "ConditionRule": [
          {
            "Object": "directory",
            "Operator": "match",
            "Type": "url",
            "Value": "/"
          }
        ],
        "Connective": "OR"
      },
      "OriginArgAction": {
        "OriginArgComponents": [
          {
            "Action": "include",
            "Object": "queryString",
            "Subobject": "*"
          }
        ]
      }
    }
  ],
  "OriginCertCheck": {
    "Switch": false
  },
  "OriginHost": "",
  "OriginIPv6": "followclient",
  "OriginProtocol": "http",
  "OriginRange": false,
  "Project": "default",
  "RemoteAuth": {
    "Switch": false
  },
  "RequestHeader": [
    {
      "Condition": null,
      "RequestHeaderAction": {
        "RequestHeaderInstances": [
          {
            "Action": "set",
            "Key": "x-byteplus-demo-client-ip",
            "Value": "client_ip",
            "ValueType": "variable"
          },
          {
            "Action": "set",
            "Key": "x-cdn-origin-server",
            "Value": "origin_srv_addr",
            "ValueType": "variable"
          }
        ]
      }
    }
  ],
  "ResponseHeader": [
    {
      "Condition": null,
      "ResponseHeaderAction": {
        "ResponseHeaderInstances": [
          {
            "AccessOriginControl": false,
            "Action": "set",
            "Key": "Pragma",
            "Value": "request_uri",
            "ValueType": "variable"
          }
        ]
      }
    }
  ],
  "SignedUrlAuth": {
    "SignedUrlAuthRules": [
      {
        "Condition": {
          "ConditionRule": null,
          "Connective": null
        },
        "SignedUrlAuthAction": null
      }
    ]
  },
  "Type": "service",
  "UaAccessRule": {
    "AllowEmpty": true
  },
  "UrlNormalize": {
    "NormalizeObject": ["back_slashes", "successive_slashes", "dot_segments"],
    "Switch": true
  }
}
"""