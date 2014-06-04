#Compacting PKI Token in keystone

PKI tokens was too fat in big clouds, and it was a real PITA. I've replaced it with Fernets, but here is a story behind it.

## Problem
Let’s see the scenario:

  1. User opens console, sources `openrc` and issues any `nova` (for example) command
  2. novaclient asks for the token via python-keystoneclient
  3. User has got this token, here is `POST /v2.0/tokens` response:

    {
        "access": {
            "token": {
                "issued_at": "2014-05-30T12:16:19.582411", 
                "expires": "2014-05-31T12:16:19Z", 
                "id": "token", 
                "tenant": {
                    "description": "", 
                    "enabled": true, 
                    "id": "659f2aeaea5a43e18abea1a598557f24", 
                    "name": "devel"
                }
            }, 
            "serviceCatalog": [
            ...
            ], 
            "user": {
                "username": "yottatsa", 
                "roles_links": [], 
                "id": "20613f973ead4ecab32ad47a24fddfe6", 
                "roles": [
                    {
                        "name": "admin"
                    }
                ], 
                "name": "yottatsa"
            }, 
            "metadata": {
                "is_admin": 0, 
                "roles": [
                    "54178770527648468a02f1bf1d0cfc09"
                ]
            }
        }
    }

  4. novaclient extracts compute endpoint from supplied serviceCatalog
  5. Let’s pretend we’re using PKI tokens for the large cloud
  6. novaclient builds requests to nova-api
  7. It fails because of header size if you cloud is large enough

<p class="lead">We have <em>no</em> any approach to use OpenStack with more than N regions</p>

Why?

  1. [Token compression][compress-tokens] isn't ready yet, and IMHO it is not worth the effort that had been made for. It's _easier_ to enlarge your `MAX_HEADER_SIZE` instead.
  2. UUID token loads keystone
  3. [Optional catalog][catalog-optional] has been implemented only in [keystoneclient's middleware][include_service_catalog], so we can’t just use it for end user clients.

Plus. Some services like is trying to proxy your requests to another services. Like nova proxying cinder. There are some [tests][tempest] and [bug][1228317] about it.

Nova is relying on `X-Service-Catalog` WSGI header in [nova/api/auth.py][auth.py], which is marked as optional in [keystoneclient's auth_token.py][auth_token.py_catalog]. So we could run into `EndpointNotFound` if we remove service catalog.

## Solution

First idea was: let’s remove service catalog from signed part, so it will be much smaller, which I had done. It made some problems, which exactly the same with [this bug][1228317], so there I’ve got a [hint from Dolph Mathews][dolph], he said:

> the long term goal with removing the service catalog from the token also included a new endpoint on keystone to fetch a catalog, e.g. `GET /v3/catalog` separately from the token. When presented with a catalog-free token, keystoneclient.middleware.auth_token could call GET /v3/catalog and populate the X-Service-Catalog header as usual.

So I did this too. Here it is, [patch for catalog repopulation][gerrit-keystoneclient] and [patch to remove a catalog][gerrit-keystone]. And here is a [blueprint][compact-pki-token].

What’s next:

  * there are quick’n’dirty patches, I plan to rewrite keystoneclient patch completely, removing obsolete parts 
  * keystone is need for _catalog API call_


[designate]: https://wiki.openstack.org/wiki/Designate "Designate provides DNSaaS services for OpenStack"
[pki-token]: http://docs.openstack.org/admin-guide-cloud/content/certificates-for-pki.html "Certificates for PKI - OpenStack Cloud Administrator Guide"
[compress-tokens]: https://blueprints.launchpad.net/keystone/+spec/compress-tokens "Support Compression of the PKI token : Blueprints : Keystone"
[compressed-tokens]: http://adam.younglogic.com/2014/02/compressed-tokens/ "Compressed tokens | Adam Young's Web Log"
[catalog-optional]: https://blueprints.launchpad.net/keystone/+spec/catalog-optional "Allow clients to opt-out of service catalog inclusion: Blueprints : Keystone"
[pki.py]: https://github.com/openstack/keystone/blob/ba1bba8257716c2f5aa668e496173e96a80f0e43/keystone/token/providers/pki.py#L35 "on github"
[common.py]: https://github.com/openstack/keystone/blob/ba1bba8257716c2f5aa668e496173e96a80f0e43/keystone/token/providers/common.py#L414 "on github"
[auth_token.py]: https://github.com/openstack/python-keystoneclient/blob/22db04bb6bee3ab15a90510bb6c1780d2a254300/keystoneclient/middleware/auth_token.py#L368 "on github"
[auth_token.py_catalog]: https://github.com/openstack/python-keystoneclient/blob/22db04bb6bee3ab15a90510bb6c1780d2a254300/keystoneclient/middleware/auth_token.py#L1023 "on github"
[compact-pki-token]: https://blueprints.launchpad.net/keystone/+spec/compact-pki-token "Reducing size of PKI token : Blueprints : Keystone"
[auth.py]: https://github.com/openstack/nova/blob/HEAD/nova/api/auth.py#L129 "on github"
[include_service_catalog]: https://github.com/openstack/python-keystoneclient/commit/a97b293501fa504dd154fc921809a40bc2a34049 "Opt-out of service catalog on GitHub"
[tempest]: http://logs.openstack.org/25/96725/5/check/check-tempest-dsvm-full/08bd499/
[1228317]: https://bugs.launchpad.net/python-keystoneclient/+bug/1228317/comments/6
[gerrit-keystone]: https://review.openstack.org/96725
[gerrit-keystoneclient]: https://review.openstack.org/97854
[dolph]: https://bugs.launchpad.net/python-keystoneclient/+bug/1228317/comments/8
[story]: https://github.com/yottatsa/yottatsa.github.io/blob/c6ea2b73fd1ad171975eda99adc84fe0530d46c9/Papers/Compacting-PKI-Token-in-keystone.txt
