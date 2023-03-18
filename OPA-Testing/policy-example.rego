package envoy.authz

import future.keywords

import input.attributes

default allow = false

allow if {
	path_allowed
	token_match
}

path_allowed if {
	allowed_paths := [
	{paths}
#    	"fs1,fs2,fs3", 
#        "fs1,fs2", 
#        "fs1"
    ] # Append all valid paths into this array

	encoded := attributes.request.http.headers
	encoded.sources in allowed_paths
}

token_match if {
	tokenMap := [
		{"sName": "{name}", "tokVal": "{token}"},
#		{"sName": "fs1", "tokVal": "token1"},
#		{"sName": "fs2", "tokVal": "token2"},
#		{"sName": "fs3", "tokVal": "token3"},
	]		# Append all serviceName + token pairs into this array

	encoded := attributes.request.http.headers
	sourcesList := split(encoded.sources, ",")
	tokensList := split(encoded.tokens, ",")
	every source in sourcesList {
		some i
		source == sourcesList[j]
		tokenMap[i].sName == source
		tokenMap[i].tokVal == tokensList[j]
	}
    
	every token in tokensList {
		some i
		token == tokensList[j]
		tokenMap[i].tokVal == token
		tokenMap[i].sName == sourcesList[j]
	}
}
