# Example CoAP GET Commands for Wi-SUN Node

Replace `[fd12:3456::0eae:5fff:fe6d:4eca]` with your device's IPv6 address if different.

## Get all info
```
coap-client-notls -m get -N -B 10 -t text coap://[fd12:3456::0eae:5fff:fe6d:4eca]:5683/info/all
```

## Get device type
```
coap-client-notls -m get -N -B 10 -t text coap://[fd12:3456::0eae:5fff:fe6d:4eca]:5683/info/device_type
```

## Get application version
```
coap-client-notls -m get -N -B 10 -t text coap://[fd12:3456::0eae:5fff:fe6d:4eca]:5683/info/version
```

## Get all status
```
coap-client-notls -m get -N -B 10 -t text coap://[fd12:3456::0eae:5fff:fe6d:4eca]:5683/status/all
```

## Get running time
```
coap-client-notls -m get -N -B 10 -t text coap://[fd12:3456::0eae:5fff:fe6d:4eca]:5683/status/running
```

## Get parent info
```
coap-client-notls -m get -N -B 10 -t text coap://[fd12:3456::0eae:5fff:fe6d:4eca]:5683/status/parent
```

## Get all application statistics
```
coap-client-notls -m get -N -B 10 -t text coap://[fd12:3456::0eae:5fff:fe6d:4eca]:5683/statistic/app/all
```

## Set auto_send value (PUT example)
```
coap-client-notls -m put -N -B 10 -t text coap://[fd12:3456::0eae:5fff:fe6d:4eca]:5683/settings/auto_send -e 60
```

## LED ON/OFF control (PUT example)
```
coap-client-notls -m put -N -B 10 -t text coap://[fd12:3456::0eae:5fff:fe6d:4eca]:5683/leds/control -e "LED ON"
coap-client-notls -m put -N -B 10 -t text coap://[fd12:3456::0eae:5fff:fe6d:4eca]:5683/leds/control -e "LED OFF"
```
