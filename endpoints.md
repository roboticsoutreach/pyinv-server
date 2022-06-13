

- /v1/manufacturers
- /v1/manufacturers/{manufacturerSlug}
- /v1/manufacturers/{manufacturerSlug}/models
- /v1/manufacturers/{manufacturerSlug}/models/{modelId}

- /v1/nodes/
- /v1/nodes/?type=asset
- /v1/nodes/?type=asset&manufacturer={manufacturerSlug}
- /v1/nodes/?type=location
- /v1/nodes/?parent=root
- /v1/nodes/?parent={locationSlug}
- /v1/nodes/{recordId}
- /v1/nodes/by-ref/{reference}
- /v1/nodes/{recordId}/children

- /v1/nodes/{recordId}/move?to={recordId}
- /v1/nodes/{recordId}/dispose
- /v1/nodes/{recordId}/lost