package envoy.authz

import future.keywords

import input.attributes
default allow := false

allow if {
	action_allowed
}

action_allowed if {
	attributes.request.http.method == "GET"
	encoded == "token1"
} 
action_allowed if {
	attributes.destination.principal == "spiffe://cluster.local/ns/default/sa/fs2"
	attributes.request.http.method == "GET"
	encoded == "token1,token1"
}



encoded := attributes.request.http.headers.myheader

