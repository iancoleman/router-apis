import base64
import re
import sys
import urllib2

###
# Configures the TPLINK TD-W8950N router with the values set below
###

# Login parameters
gatewayIp = "192.168.1.1"
user = "admin"
password = "admin"

# Router parameters
ssid = "TP-LINK_Custom_SSID" # must be < 32 chars
# TODO there are more values that can be set, just need to figure them out

# Make request to get authorization token
auth = "Authorization=Basic %s" % base64.b64encode(user + ":" + password)
url = "http://%s/main.html" % gatewayIp
data = ""
headers = {
    "Referer": url,
    "Cookie": auth,
}
r = urllib2.Request(url, data, headers)
f = urllib2.urlopen(r)
headers = f.info().items()
for header in headers:
    if header[0] == "set-cookie":
        auth = header[1]
        break

# Get session key
url = "http://%s/wlswitchinterface0.wl" % gatewayIp
data = ""
headers = {
    "Referer": url,
    "Cookie": auth,
}
r = urllib2.Request(url, data, headers)
f = urllib2.urlopen(r)
content = f.read()
sessionKeyRe = re.compile("sessionKey=(\d+)")
sessionKeyMatch = sessionKeyRe.search(content)
if sessionKeyMatch is None:
    sys.exit()
sessionKey = sessionKeyMatch.groups()[0]

# Set new parameters
# TODO figure out what more of these mean and make them configurable
url = "http://%s/wlcfg.wl?" % gatewayIp
url += "wlSsidIdx=0"
url += "&wlEnbl=1"
url += "&wlHide=0"
url += "&wlAPIsolation=0"
url += "&wlSsid=%s" % ssid
url += "&wlCountry=US"
url += "&wlMaxAssoc=50"
url += "&wlDisableWme=0"
url += "&wlEnableWmf=1"
url += "&wlEnbl_wl0v1=0"
url += "&wlSsid_wl0v1=TP-LINK_GuestA4"
url += "&wlHide_wl0v1=0"
url += "&wlAPIsolation_wl0v1=0"
url += "&wlDisableWme_wl0v1=0"
url += "&wlEnableWmf_wl0v1=1"
url += "&wlMaxAssoc_wl0v1=16"
url += "&wlEnbl_wl0v2=0"
url += "&wlSsid_wl0v2=wl0_Guest2"
url += "&wlHide_wl0v2=0"
url += "&wlHide_wl0v2=0"
url += "&wlAPIsolation_wl0v2=0"
url += "&wlDisableWme_wl0v2=0"
url += "&wlEnableWmf_wl0v2=1"
url += "&wlMaxAssoc_wl0v2=16"
url += "&wlEnbl_wl0v3=0"
url += "&wlSsid_wl0v3=wl0_Guest3"
url += "&wlHide_wl0v3=0"
url += "&wlAPIsolation_wl0v3=0"
url += "&wlDisableWme_wl0v3=0"
url += "&wlEnableWmf_wl0v3=1"
url += "&wlMaxAssoc_wl0v3=16"
url += "&wlSyncNvram=1"
url += "&sessionKey=%s" % sessionKey

# Send new parameters to the gateway
data = ""
headers = {
    "Referer": "http://%s/wlswitchinterface0.wl" % gatewayIp,
    "Cookie": auth,
}
r = urllib2.Request(url, data, headers)
f = urllib2.urlopen(r)

# These settings are now being applied, may take about ten seconds to be
# applied and the modem restarted.
